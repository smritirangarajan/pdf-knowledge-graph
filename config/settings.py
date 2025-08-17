"""
Configuration settings for the PDF Knowledge Graph Generator
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Application settings
APP_NAME = "PDF Knowledge Graph Generator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Extract text from PDFs and generate interactive knowledge graphs"

# Streamlit configuration
STREAMLIT_CONFIG = {
    "server": {
        "port": int(os.getenv("STREAMLIT_SERVER_PORT", 8501)),
        "address": os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0"),
        "headless": os.getenv("STREAMLIT_SERVER_HEADLESS", "true").lower() == "true",
        "enableCORS": os.getenv("STREAMLIT_SERVER_ENABLE_CORS", "false").lower() == "true",
        "enableXsrfProtection": os.getenv("STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION", "false").lower() == "true",
        "maxUploadSize": int(os.getenv("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", 200))
    },
    "browser": {
        "gatherUsageStats": False
    },
    "theme": {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730",
        "font": "sans serif"
    }
}

# File upload settings
UPLOAD_CONFIG = {
    "max_file_size": 200 * 1024 * 1024,  # 200MB
    "allowed_extensions": [".pdf"],
    "upload_dir": BASE_DIR / "uploads"
}

# NLP settings
NLP_CONFIG = {
    "spacy_model": "en_core_web_sm",
    "entity_types": [
        "PERSON",      # People
        "ORG",         # Organizations
        "GPE",         # Countries, cities, etc.
        "PRODUCT",     # Products
        "EVENT",       # Named events
        "WORK_OF_ART", # Titles of books, songs, etc.
        "FAC",         # Buildings, airports, highways, etc.
        "LAW",         # Named documents made into laws
        "LANGUAGE",    # Named languages
        "DATE",        # Absolute or relative dates or periods
        "TIME",        # Times smaller than a day
        "PERCENT",     # Percentage
        "MONEY",       # Monetary values
        "QUANTITY",    # Measurements
        "ORDINAL",     # Ordinal numbers
        "CARDINAL"     # Cardinal numbers
    ],
    "min_entity_length": 2,
    "max_entity_length": 50
}

# Graph settings
GRAPH_CONFIG = {
    "max_nodes": 1000,
    "max_edges": 5000,
    "node_size_range": (10, 50),
    "edge_color": "#666666",
    "physics_enabled": True,
    "hierarchical": False,
    "directed": False
}

# Visualization settings
VISUALIZATION_CONFIG = {
    "chart_height": 400,
    "chart_width": 800,
    "wordcloud_width": 800,
    "wordcloud_height": 400,
    "network_layout": "spring",  # spring, circular, random, shell
    "color_scheme": {
        "PERSON": "#ff7f0e",
        "ORG": "#2ca02c",
        "GPE": "#d62728",
        "PRODUCT": "#9467bd",
        "EVENT": "#8c564b",
        "WORK_OF_ART": "#e377c2",
        "FAC": "#17becf",
        "LAW": "#bcbd22",
        "LANGUAGE": "#7f7f7f",
        "DATE": "#e377c2",
        "TIME": "#8c564b",
        "PERCENT": "#9467bd",
        "MONEY": "#d62728",
        "QUANTITY": "#2ca02c",
        "ORDINAL": "#ff7f0e",
        "CARDINAL": "#1f77b4",
        "default": "#1f77b4"
    }
}

# Export settings
EXPORT_CONFIG = {
    "formats": ["csv", "json", "xlsx"],
    "default_format": "csv",
    "include_metadata": True,
    "compression": False
}

# Performance settings
PERFORMANCE_CONFIG = {
    "cache_ttl": 3600,  # 1 hour
    "max_text_length": 1000000,  # 1MB of text
    "batch_size": 1000,
    "enable_caching": True
}

# Logging settings
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": BASE_DIR / "logs" / "app.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# Security settings
SECURITY_CONFIG = {
    "enable_authentication": False,
    "allowed_ips": [],
    "rate_limit": 100,  # requests per minute
    "session_timeout": 3600  # 1 hour
}

# Development settings
DEV_CONFIG = {
    "debug": os.getenv("DEBUG", "false").lower() == "true",
    "reload": os.getenv("RELOAD", "false").lower() == "true",
    "profiling": os.getenv("PROFILING", "false").lower() == "true"
}

def get_config():
    """Get the complete configuration dictionary"""
    return {
        "app": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION
        },
        "streamlit": STREAMLIT_CONFIG,
        "upload": UPLOAD_CONFIG,
        "nlp": NLP_CONFIG,
        "graph": GRAPH_CONFIG,
        "visualization": VISUALIZATION_CONFIG,
        "export": EXPORT_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "logging": LOGGING_CONFIG,
        "security": SECURITY_CONFIG,
        "development": DEV_CONFIG
    }

def validate_config():
    """Validate the configuration settings"""
    errors = []
    
    # Check if spaCy model exists
    try:
        import spacy
        nlp = spacy.load(NLP_CONFIG["spacy_model"])
    except OSError:
        errors.append(f"spaCy model '{NLP_CONFIG['spacy_model']}' not found")
    
    # Check directories
    for dir_path in [UPLOAD_CONFIG["upload_dir"], BASE_DIR / "logs"]:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # Check file size limits
    if UPLOAD_CONFIG["max_file_size"] > 500 * 1024 * 1024:  # 500MB
        errors.append("File size limit too high")
    
    return errors
