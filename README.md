# PDF Knowledge Graph Generator

A comprehensive Streamlit application that extracts text from PDFs and generates interactive knowledge graphs using advanced NLP techniques.

## Features

- **PDF Processing**: Extract text from PDF files using multiple extraction methods
- **NLP Analysis**: Named Entity Recognition (NER), keyword extraction, and relationship mapping
- **Knowledge Graph Generation**: Create interactive network graphs from extracted entities and relationships
- **Text Analysis**: Sentiment analysis, readability metrics, and comprehensive text statistics
- **Interactive Visualizations**: Multiple visualization types including interactive graphs, charts, and word clouds
- **Export Capabilities**: Export data in multiple formats (CSV, JSON)
- **Streamlit Interface**: Responsive web interface

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/smritirangarajan/pdf-knowledge-graph.git
   cd pdf-knowledge-graph
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

## Usage

### 1. Upload & Process
- Upload a PDF file using the file uploader
- The application will extract and process the text
- View basic statistics and text preview

### 2. Text Analysis
- Analyze extracted text for entities, keywords, and relationships
- View sentiment analysis and readability metrics
- Explore named entities and their classifications

### 3. Knowledge Graph
- Generate interactive knowledge graphs from extracted data
- View graph statistics and network properties
- Explore node and edge details

### 4. Visualizations
- Entity type distribution charts
- Node degree distribution analysis
- Keyword word clouds
- Network layout visualizations

### 5. Export & Deploy
- Export data in multiple formats (CSV, JSON)
- Download requirements and deployment files
- Access deployment instructions

## 🏗️ Architecture

The application is built with a modular architecture:

```
app.py                          # Main Streamlit application
├── KnowledgeGraphGenerator     # Core knowledge graph logic
├── PDF Processing             # Text extraction and preprocessing
├── NLP Analysis               # Entity extraction and relationship mapping
├── Graph Generation           # NetworkX graph construction
├── Visualization              # Interactive charts and graphs
└── Export/Deploy             # Data export and deployment tools
```

## Configuration

### Environment Variables

Create a `.env` file for custom configurations:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Customization

- Modify entity types in `extract_entities()` method
- Adjust graph visualization parameters in `generate_graph_visualization()`
- Customize color schemes in `get_node_color()`

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py --server.port 8501
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t pdf-knowledge-graph .

# Run the container
docker run -p 8501:8501 pdf-knowledge-graph
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **PyPDF2/pdfplumber**: PDF text extraction
- **spaCy**: Natural language processing
- **NetworkX**: Graph theory and network analysis
- **Plotly**: Interactive visualizations
- **Matplotlib**: Static visualizations

### NLP & Analysis
- **NLTK**: Natural language toolkit
- **TextBlob**: Sentiment analysis
- **scikit-learn**: Machine learning utilities
- **WordCloud**: Keyword visualization

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Streamlit Extras**: Additional Streamlit components

### KnowledgeGraphGenerator Class

#### Methods

- `extract_text_from_pdf(pdf_file)`: Extract text from PDF
- `preprocess_text()`: Clean and normalize text
- `extract_entities()`: Extract named entities
- `extract_keywords()`: Extract keywords using TF-IDF
- `extract_relationships()`: Extract subject-verb-object relationships
- `build_graph()`: Construct NetworkX graph
- `analyze_text()`: Perform comprehensive text analysis

#### Properties

- `text`: Extracted text content
- `entities`: List of named entities
- `relationships`: List of extracted relationships
- `graph`: NetworkX graph object

## Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=app tests/
```

### Test Files

- `tests/test_pdf_processing.py`: PDF extraction tests
- `tests/test_nlp.py`: NLP analysis tests
- `tests/test_graph.py`: Graph generation tests
