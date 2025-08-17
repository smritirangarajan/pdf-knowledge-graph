# app.py
import io
import json
import re
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import nltk
import numpy as np
import pandas as pd
import pdfplumber
import PyPDF2
import spacy
import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
import plotly.express as px

# Optional visual libs
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config
from pyvis.network import Network
import tempfile
import os

# -------------------------------------------------
# App config
# -------------------------------------------------
st.set_page_config(
    page_title="PDF Knowledge Graph Generator",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .main-header { font-size: 2.0rem; text-align:center; margin: 0.5rem 0 1rem; }
      .sub-header { font-size: 1.2rem; margin: 0.25rem 0 0.75rem; }
      .metric-card { background:#f6f8fb; padding:0.8rem; border-radius:8px; border-left:4px solid #1f77b4; }
      .stButton > button { width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Dependencies (cached) 
# -------------------------------------------------
@st.cache_resource
def ensure_nltk_data():
    needed = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),  # present on newer NLTK
        ("corpora/stopwords", "stopwords"),
    ]
    for path, pkg in needed:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg)

ensure_nltk_data()
from nltk.tokenize import sent_tokenize

@st.cache_resource
def load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        return spacy.load("en_core_web_sm")

# -------------------------------------------------
# Core class
# -------------------------------------------------
class KnowledgeGraphGenerator:
    def __init__(self):
        self.text = ""
        self.entities = []
        self.relationships = []
        self.keywords = []
        self.graph = nx.Graph()
        self.nlp = load_spacy()

    def extract_text_from_pdf(self, file_like):
        """Extract text from uploaded PDF (prefers pdfplumber, falls back to PyPDF2)."""
        try:
            with pdfplumber.open(file_like) as pdf:
                text = "".join([(p.extract_text() or "") for p in pdf.pages])
        except Exception:
            try:
                file_like.seek(0)
                reader = PyPDF2.PdfReader(file_like)
                text = "".join([page.extract_text() or "" for page in reader.pages])
            except Exception as e:
                st.error(f"Error extracting text: {e}")
                return None
        self.text = text
        return text

    def preprocess_text(self):
        if not self.text:
            return ""
        txt = re.sub(r"\s+", " ", self.text)
        txt = re.sub(r"[^\w\s\.\,\!\?\;\:]", "", txt)
        self.text = " ".join(txt.split())
        return self.text

    def extract_entities(self):
        if not self.text:
            return []
        doc = self.nlp(self.text)
        ents = []
        keep = {"PERSON", "ORG", "GPE", "PRODUCT", "EVENT", "WORK_OF_ART"}
        for ent in doc.ents:
            if ent.label_ in keep:
                ents.append(
                    {
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                    }
                )
        self.entities = ents
        return ents

    def extract_keywords(self, top_k=50):
        if not self.text:
            return []
        stop = set(nltk.corpus.stopwords.words("english"))
        tokens = nltk.word_tokenize(self.text.lower())
        words = [w for w in tokens if w.isalnum() and w not in stop and len(w) > 3]
        counts = Counter(words)
        self.keywords = [w for w, _ in counts.most_common(top_k)]
        return self.keywords

    def extract_relationships(self):
        if not self.text:
            return []
        doc = self.nlp(self.text)
        rels = []
        # simple SVO pattern (extend as needed)
        for token in doc:
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                subj = token.text
                verb = token.head.text
                for child in token.head.children:
                    if child.dep_ in {"dobj", "pobj"}:
                        obj = child.text
                        if subj and obj and subj != obj:
                            rels.append(
                                {"subject": subj, "predicate": verb, "object": obj, "type": "SVO"}
                            )
        self.relationships = rels
        return rels

    def build_graph(self):
        G = nx.Graph()
        for e in self.entities:
            G.add_node(e["text"], label=e["label"], type="entity", size=20)
        for r in self.relationships:
            G.add_edge(r["subject"], r["object"], label=r["predicate"], type="relationship")
        self.graph = G
        return G

    # ---------- Visualization helpers ----------
    def _safe_id(self, x, maxlen=60):
        s = str(x).strip() or "unknown"
        return s[:maxlen]

    def _safe_label(self, x, maxlen=30):
        s = str(x).strip()
        return s if len(s) <= maxlen else (s[:maxlen - 1] + "…")

    def _node_color(self, label):
        colors = {
            "PERSON": "#ff7f0e",
            "ORG": "#2ca02c",
            "GPE": "#d62728",
            "PRODUCT": "#9467bd",
            "EVENT": "#8c564b",
            "WORK_OF_ART": "#e377c2",
            "default": "#1f77b4",
        }
        return colors.get(label, colors["default"])

    def make_agraph_payload(self):
        """Return sanitized nodes/edges + Config for streamlit-agraph."""
        if self.graph.number_of_nodes() == 0:
            return [], [], None

        nodes, edges = [], []
        seen_ids = set()

        # Map original node -> safe id
        for n, data in self.graph.nodes(data=True):
            nid = self._safe_id(n)
            if nid in seen_ids:
                nid = f"{nid}_{hash((nid, len(seen_ids))) & 0xffff}"
            seen_ids.add(nid)
            self.graph.nodes[n]["__safe_id__"] = nid

            nodes.append(
                Node(
                    id=nid,
                    label=self._safe_label(n),
                    size=int(data.get("size", 18)),
                    color=self._node_color(data.get("label", "default")),
                )
            )

        # Edges (no self-loops, no missing nodes)
        for u, v, data in self.graph.edges(data=True):
            su = self.graph.nodes[u].get("__safe_id__")
            sv = self.graph.nodes[v].get("__safe_id__")
            if not su or not sv or su == sv:
                continue
            edges.append(
                Edge(
                    source=su,
                    target=sv,
                    label=self._safe_label(data.get("label", "")),
                    color="#666666",
                )
            )

        cfg = Config(
            height=600,
            width=1000,
            directed=False,
            physics=True,
            hierarchical=False,
        )
        
        return nodes, edges, cfg

    def analyze_text(self):
        if not self.text:
            return {}
        blob = TextBlob(self.text)
        return {
            "word_count": len(self.text.split()),
            "char_count": len(self.text),
            "sentence_count": len(sent_tokenize(self.text)),
            "avg_word_length": float(np.mean([len(w) for w in self.text.split()])),
            "sentiment": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity,
        }


# -------------------------------------------------
# App state
# -------------------------------------------------
st.markdown('<h1 class="main-header">PDF Knowledge Graph Generator</h1>', unsafe_allow_html=True)

if "kg" not in st.session_state:
    st.session_state.kg = KnowledgeGraphGenerator()
if "graph_ready" not in st.session_state:
    st.session_state.graph_ready = False

kg = st.session_state.kg

# -------------------------------------------------
# Sidebar Navigation (names must match below)
# -------------------------------------------------
with st.sidebar:
    st.markdown("## Navigation")
    page = option_menu(
        None,
        ["Upload & Process", "Text Analysis", "Knowledge Graph", "Visualizations", "Export"],
        icons=["upload", "search", "diagram-3", "bar-chart", "cloud-download"],
        default_index=0,
    )

# -------------------------------------------------
# Upload & Process
# -------------------------------------------------
if page == "Upload & Process":
    st.markdown('<h2 class="sub-header">Upload & Process PDF</h2>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded:
        data_bytes = uploaded.read()
        buf_for_plumber = io.BytesIO(data_bytes)

        with st.spinner("Extracting text..."):
            text = kg.extract_text_from_pdf(buf_for_plumber)

        if text:
            kg.preprocess_text()
            st.success("PDF processed successfully.")

            c1, c2 = st.columns(2)
            c1.metric("Characters", f"{len(text):,}")
            c1.metric("Words", f"{len(text.split()):,}")
            c2.metric("Sentences", f"{len(sent_tokenize(text)):,}")
            c2.metric("File Size (KB)", f"{len(data_bytes)/1024:.1f}")

            with st.expander("Text Preview (first 500 chars)"):
                st.text(text[:500] + ("..." if len(text) > 500 else ""))

            if st.button("Generate Knowledge Graph", type="primary"):
                with st.spinner("Building knowledge graph..."):
                    kg.extract_entities()
                    kg.extract_keywords()
                    kg.extract_relationships()
                    kg.build_graph()
                st.session_state.graph_ready = True
                st.success("Knowledge graph generated.")

# -------------------------------------------------
# Text Analysis
# -------------------------------------------------
elif page == "Text Analysis":
    st.markdown('<h2 class="sub-header">Text Analysis</h2>', unsafe_allow_html=True)

    if not kg.text:
        st.info("Please upload and process a PDF first.")
        st.stop()

    analysis = kg.analyze_text()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Word Count", f"{analysis['word_count']:,}")
    c2.metric("Character Count", f"{analysis['char_count']:,}")
    c3.metric("Sentence Count", f"{analysis['sentence_count']:,}")
    c4.metric("Avg Word Length", f"{analysis['avg_word_length']:.1f}")

    c1, c2 = st.columns(2)
    c1.metric("Sentiment", f"{analysis['sentiment']:.3f}")
    c2.metric("Subjectivity", f"{analysis['subjectivity']:.3f}")

    if kg.entities:
        st.subheader("Named Entities")
        st.dataframe(pd.DataFrame(kg.entities), use_container_width=True)

    if kg.keywords:
        st.subheader("Top Keywords")
        st.dataframe(
            pd.DataFrame({"Keyword": kg.keywords[:20], "Rank": range(1, 21)}),
            use_container_width=True,
        )

# -------------------------------------------------
# Knowledge Graph
# -------------------------------------------------
elif page == "Knowledge Graph":
    st.markdown('<h2 class="sub-header">Knowledge Graph</h2>', unsafe_allow_html=True)

    if not st.session_state.graph_ready or kg.graph.number_of_nodes() == 0:
        st.info("Generate a knowledge graph on the Upload & Process page.")
        st.stop()

    c1, c2, c3 = st.columns(3)
    c1.metric("Nodes", kg.graph.number_of_nodes())
    c2.metric("Edges", kg.graph.number_of_edges())
    c3.metric("Density", f"{nx.density(kg.graph):.3f}")

    # Try streamlit-agraph; if it fails, fall back to PyVis
    rendered = False
    try:
        nodes, edges, cfg = kg.make_agraph_payload()
        if nodes and edges and cfg:
            agraph(nodes=nodes, edges=edges, config=cfg)
            rendered = True
    except Exception as e:
        st.warning(f"streamlit-agraph failed: {e}. Falling back to PyVis.")

    if not rendered:
        with tempfile.TemporaryDirectory() as td:
            html_path = os.path.join(td, "graph.html")
            net = Network(height="620px", width="100%", directed=False, notebook=False)
            for n, d in kg.graph.nodes(data=True):
                net.add_node(str(n), label=str(n), title=d.get("label", "entity"))
            for u, v, d in kg.graph.edges(data=True):
                net.add_edge(str(u), str(v), title=str(d.get("label", "")))
            net.repulsion(node_distance=160, spring_length=160)
            net.show(html_path)
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
            st.components.v1.html(html, height=650, scrolling=True)

    with st.expander("Graph Details"):
        node_rows = [
            {"Node": n, "Type": d.get("label", "Unknown"), "Degree": kg.graph.degree(n)}
            for n, d in kg.graph.nodes(data=True)
        ]
        if node_rows:
            st.subheader("Nodes")
            st.dataframe(
                pd.DataFrame(node_rows).sort_values("Degree", ascending=False),
                use_container_width=True,
            )

        edge_rows = [
            {"Source": s, "Target": t, "Relationship": d.get("label", "Unknown")}
            for s, t, d in kg.graph.edges(data=True)
        ]
        if edge_rows:
            st.subheader("Edges")
            st.dataframe(pd.DataFrame(edge_rows), use_container_width=True)

# -------------------------------------------------
# Visualizations
# -------------------------------------------------
elif page == "Visualizations":
    st.markdown('<h2 class="sub-header">Visualizations</h2>', unsafe_allow_html=True)

    if not st.session_state.graph_ready or kg.graph.number_of_nodes() == 0:
        st.info("Generate a knowledge graph first.")
        st.stop()

    if kg.entities:
        types = [e["label"] for e in kg.entities]
        counts = Counter(types)
        fig = px.pie(values=list(counts.values()), names=list(counts.keys()), title="Entity Type Distribution")
        st.plotly_chart(fig, use_container_width=True)

    degrees = [kg.graph.degree(n) for n in kg.graph.nodes()]
    deg_counts = Counter(degrees)
    fig = px.bar(
        x=list(deg_counts.keys()),
        y=list(deg_counts.values()),
        labels={"x": "Degree", "y": "Count"},
        title="Node Degree Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Keyword Word Cloud")
    if kg.keywords:
        text_wc = " ".join(kg.keywords[:50])
        wc = WordCloud(width=800, height=400, background_color="white").generate(text_wc)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    st.subheader("Static Network Layout")
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(kg.graph, k=1, iterations=50)
    nx.draw_networkx_nodes(kg.graph, pos, node_color="lightblue", node_size=500, ax=ax)
    nx.draw_networkx_edges(kg.graph, pos, edge_color="gray", alpha=0.6, ax=ax)
    nx.draw_networkx_labels(kg.graph, pos, font_size=8, ax=ax)
    ax.set_title("Knowledge Graph Network Layout")
    ax.axis("off")
    st.pyplot(fig)

# -------------------------------------------------
# Export
# -------------------------------------------------
elif page == "Export":
    st.markdown('<h2 class="sub-header">Export</h2>', unsafe_allow_html=True)

    if not st.session_state.graph_ready or kg.graph.number_of_nodes() == 0:
        st.info("Generate a knowledge graph first.")
        st.stop()

    c1, c2 = st.columns(2)

    with c1:
        if kg.entities:
            st.download_button(
                "Download Entities (CSV)",
                pd.DataFrame(kg.entities).to_csv(index=False),
                file_name="entities.csv",
                mime="text/csv",
            )
        if kg.relationships:
            st.download_button(
                "Download Relationships (CSV)",
                pd.DataFrame(kg.relationships).to_csv(index=False),
                file_name="relationships.csv",
                mime="text/csv",
            )

    with c2:
        graph_json = json.dumps(nx.node_link_data(kg.graph), indent=2)
        st.download_button(
            "Download Graph (JSON)", data=graph_json, file_name="knowledge_graph.json", mime="application/json"
        )
        if kg.text:
            st.download_button(
                "Download Text Analysis (JSON)",
                data=json.dumps(kg.analyze_text(), indent=2),
                file_name="text_analysis.json",
                mime="application/json",
            )
