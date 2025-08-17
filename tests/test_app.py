import pytest
import streamlit as st
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import KnowledgeGraphGenerator

class TestKnowledgeGraphGenerator:
    """Test class for KnowledgeGraphGenerator"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.kg_generator = KnowledgeGraphGenerator()
    
    def test_initialization(self):
        """Test that the generator initializes correctly"""
        assert self.kg_generator.text == ""
        assert self.kg_generator.entities == []
        assert self.kg_generator.relationships == []
        assert self.kg_generator.graph is not None
        assert self.kg_generator.nlp is None
    
    def test_preprocess_text_empty(self):
        """Test preprocessing with empty text"""
        result = self.kg_generator.preprocess_text()
        assert result is None
    
    def test_preprocess_text_with_content(self):
        """Test preprocessing with actual text content"""
        self.kg_generator.text = "  Hello   World!  "
        result = self.kg_generator.preprocess_text()
        assert result == "Hello World!"
    
    def test_extract_keywords_empty(self):
        """Test keyword extraction with empty text"""
        result = self.kg_generator.extract_keywords()
        assert result == []
    
    def test_extract_keywords_with_content(self):
        """Test keyword extraction with actual text"""
        self.kg_generator.text = "This is a test document with some important keywords."
        result = self.kg_generator.extract_keywords()
        assert len(result) > 0
        assert "test" in result
        assert "document" in result
    
    def test_analyze_text_empty(self):
        """Test text analysis with empty text"""
        result = self.kg_generator.analyze_text()
        assert result == {}
    
    def test_analyze_text_with_content(self):
        """Test text analysis with actual text"""
        self.kg_generator.text = "This is a test sentence. It has multiple words."
        result = self.kg_generator.analyze_text()
        assert 'word_count' in result
        assert 'char_count' in result
        assert 'sentence_count' in result
        assert result['sentence_count'] == 2
    
    def test_build_graph_empty(self):
        """Test graph building with no entities or relationships"""
        result = self.kg_generator.build_graph()
        assert result is None
    
    def test_get_node_color(self):
        """Test node color assignment"""
        colors = {
            'PERSON': '#ff7f0e',
            'ORG': '#2ca02c',
            'GPE': '#d62728',
            'PRODUCT': '#9467bd',
            'EVENT': '#8c564b',
            'WORK_OF_ART': '#e377c2',
            'default': '#1f77b4'
        }
        
        for label, expected_color in colors.items():
            color = self.kg_generator.get_node_color(label)
            assert color == expected_color
        
        # Test unknown label
        unknown_color = self.kg_generator.get_node_color('UNKNOWN')
        assert unknown_color == colors['default']

class TestAppIntegration:
    """Test class for app integration"""
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.success')
    def test_file_upload_flow(self, mock_success, mock_uploader):
        """Test the file upload flow"""
        # Mock file upload
        mock_file = Mock()
        mock_file.type = "application/pdf"
        mock_file.size = 1024
        mock_uploader.return_value = mock_file
        
        # This is a basic test - in a real scenario, you'd need to mock more components
        assert mock_uploader.called

if __name__ == "__main__":
    pytest.main([__file__])
