# Quick Start Guide

Get your PDF Knowledge Graph Generator up and running in minutes!

## ⚡ Super Quick Start (5 minutes)

### 1. Clone and Setup
```bash
git clone https://github.com/smritirangarajan/pdf-knowledge-graph.git
cd pdf-knowledge-graph
```

### 2. Run Setup Script
```bash
./scripts/setup.sh
```

### 3. Start the App
```bash
./scripts/run.sh
```

### 4. Open Your Browser
Navigate to `http://localhost:8501`

🎉 **That's it! You're ready to create knowledge graphs!**

---

## Manual Setup (if scripts don't work)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run the Application
```bash
streamlit run app.py
```

---

## Using the Application

### 1. Upload a PDF
- Click "Choose a PDF file" in the upload section
- Select any PDF document
- Wait for processing to complete

### 2. Generate Knowledge Graph
- Click "Generate Knowledge Graph" button
- Wait for analysis to complete

### 3. Explore Results
- **Text Analysis**: View statistics and entities
- **Knowledge Graph**: Interactive graph visualization
- **Visualizations**: Charts, word clouds, and network layouts
- **Export**: Download results in various formats

---

## 🐳 Docker Quick Start

### 1. Build and Run
```bash
docker-compose up --build -d
```

### 2. Access the App
Open `http://localhost:8501` in your browser

### 3. Stop the App
```bash
docker-compose down
```

---

## 🚨 Common Issues & Solutions

### Issue: "spaCy model not found"
**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Find the process
lsof -i :8501

# Kill it
kill -9 <PID>
```

### Issue: "Permission denied" on scripts
**Solution:**
```bash
chmod +x scripts/*.sh
```

### Issue: Dependencies not installing
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## What You Can Do

- **Extract text** from PDF documents
- **Identify entities** (people, organizations, locations, etc.)
- **Find relationships** between entities
- **Create interactive graphs** of knowledge
- **Analyze sentiment** and readability
- **Generate visualizations** (charts, word clouds, networks)
- **Export data** in multiple formats (CSV, JSON)

---

## 🆘 Need Help?

1. **Check the logs** in the terminal
2. **Review the README.md** for detailed documentation
3. **Check DEPLOYMENT.md** for deployment options
4. **Open an issue** on GitHub if problems persist

---

**Happy Knowledge Graphing!**
