📊 Chula Research Intelligence Platform
Final Project for Data Science Course (2024) Faculty of Engineering, Chulalongkorn University

🎓 About This Project
This project establishes a Comprehensive Research Intelligence Platform focused on transforming academic data into strategic assets. Utilizing Scopus data (2018–2023), the system integrates three distinct research topics, each utilizing a specialized pipeline consisting of a Data Module, AI Module, and Streamlit Visualization to transform raw academic history into strategic insights.

The platform bridges the gap between raw metadata and decision-making, empowering Chulalongkorn University to monitor research landscapes, optimize publication quality, and align academic output with global sustainability goals.

🚀 Key Features & Modules
The dashboard is divided into three main research analytical pillars:

1. Sustainable Development Goals (SDG) Classification
Objective: To monitor the university's social impact by tracking alignment with the 17 UN SDGs.

AI Tech: Sentence-BERT (S-BERT) for semantic search and zero-shot classification.

Functionality:

Automatically maps research titles to specific SDGs (e.g., Climate Action, Good Health).

Drill-down explorer to find top papers in each category.

2. Q1 Publication Quality Prediction
Objective: To assist researchers in assessing the potential of their work appearing in top-tier (Q1) journals before submission.

AI Tech: Random Forest Classifier (Supervised Learning).

Data Integration: Merged internal records with SCImago Journal Rank (SJR) data.

Functionality:

Real-time Predictor: Users input a draft title and collaboration status to get a success probability score.

Magic Keywords: Visualizes high-impact keywords that correlate with Q1 success.

3. Research Trends & Network Analysis
Objective: To uncover hidden research themes and map structural relationships between researchers.

AI Tech: Unsupervised Learning (Topic Modeling) & Graph Algorithms.

Functionality:

Topic Modeling: Clusters research into themes (e.g., COVID-19, Machine Learning) to track emerging trends.

Collaboration Network: Interactive force-directed graph showing co-authorship clusters and key influencers.

AI Trends: Tracks the exponential growth of AI-related papers across all faculties.

🛠️ Technology Stack
Language: Python

Web Framework: Streamlit

Data Manipulation: Pandas, NumPy

Machine Learning: Scikit-Learn (Random Forest), Sentence-Transformers (BERT)

Network Analysis: NetworkX, PyVis

Visualization: Plotly, Matplotlib
