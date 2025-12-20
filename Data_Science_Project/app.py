import streamlit as st

st.set_page_config(
    page_title="Thai Research Analytics",
    layout="wide",
    page_icon="📊",
)

st.title("📊 Thai Research Analytics Dashboard")
st.markdown("### Scopus Publications from Thai Institutions (2018-2023)")

st.markdown(
    """
This dashboard explores Thai research output from Scopus:

- **Overview** - publications by year, journals, subject areas, countries  
- **Topics** - research themes discovered with TF-IDF + K-Means  
- **Collaboration Network** - co-author relationships among the most active authors  
- **AI Trends** - where and how AI-related methods are being used  
- **Publication Quality (Q1)** - Analyzing success factors for Top-Tier Journal (Q1) publications and predicting potential quality using Random Forest Classifier with TF-IDF vectorization.
- **SDG Alignment** - Mapping research contributions to the UN Sustainable Development Goals (SDGs) using Sentence-BERT (all-MiniLM-L6-v2) for semantic similarity matching.

Use the menu on the left to navigate between pages.
"""
)