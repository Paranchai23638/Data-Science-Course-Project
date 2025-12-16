# 📊 Chula Research Intelligence Platform

**Final Project for Data Science Course (2024)**  
Faculty of Engineering, Chulalongkorn University

---

## 🎓 About This Project

This project establishes a **Comprehensive Research Intelligence Platform** focused on transforming academic data into strategic assets. Utilizing **Scopus publication data (2018–2023)**, the system integrates three distinct research topics, each implemented through a specialized pipeline consisting of:

- Data Module  
- AI Module  
- Streamlit Visualization  

These pipelines transform raw academic history into actionable strategic insights.

The platform bridges the gap between raw metadata and decision-making, empowering **Chulalongkorn University** to monitor research landscapes, optimize publication quality, and align academic output with global sustainability goals.

---

## 🚀 Key Features & Modules

The dashboard is divided into **three main research analytical pillars**:

---

### 1. Sustainable Development Goals (SDG) Classification

**Objective**  
Monitor the university's social impact by tracking alignment with the **17 United Nations Sustainable Development Goals (SDGs)**.

**AI Technology**
- Sentence-BERT (S-BERT)
- Semantic search and zero-shot classification

**Functionality**
- Automatically maps research titles to specific SDGs  
  (e.g., Climate Action, Good Health and Well-being)
- Drill-down explorer to identify top papers within each SDG category

---

### 2. Q1 Publication Quality Prediction

**Objective**  
Assist researchers in assessing the likelihood of their work being published in **top-tier (Q1) journals** prior to submission.

**AI Technology**
- Random Forest Classifier (Supervised Learning)

**Data Integration**
- Internal publication records
- SCImago Journal Rank (SJR) dataset

**Functionality**
- **Real-time Predictor**  
  Users input a draft paper title and collaboration status to receive a Q1 success probability score
- **Magic Keywords**  
  Visualization of high-impact keywords correlated with Q1 publication success

---

### 3. Research Trends & Network Analysis

**Objective**  
Uncover hidden research themes and map structural relationships between researchers.

**AI Technology**
- Unsupervised Learning (Topic Modeling)
- Graph Algorithms

**Functionality**
- **Topic Modeling**  
  Clusters publications into thematic areas (e.g., COVID-19, Machine Learning) to track emerging trends
- **Collaboration Network**  
  Interactive force-directed graph displaying co-authorship clusters and key influencers
- **AI Trends Analysis**  
  Tracks the exponential growth of AI-related publications across all faculties

---

## 🛠️ Technology Stack

**Programming Language**
- Python

**Web Framework**
- Streamlit

**Data Manipulation**
- Pandas
- NumPy

**Machine Learning & NLP**
- Scikit-Learn (Random Forest)
- Sentence-Transformers (BERT / S-BERT)

**Network Analysis**
- NetworkX
- PyVis

**Visualization**
- Plotly
- Matplotlib
