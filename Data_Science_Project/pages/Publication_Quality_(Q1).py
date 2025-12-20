import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==========================================
# 0. Page Config
# ==========================================
st.set_page_config(
    page_title="Chula Research Quality AI",
    layout="wide",
    page_icon="🏆",
    initial_sidebar_state="expanded"
)

st.title("🏆 Chula Research Quality Analytics & Prediction")
st.markdown("""Success Factor Analysis and Development of a Q1 Publication Prediction System for Chulalongkorn University Research using Machine Learning Techniques""")
st.markdown("""On SCImago, journals are ranked into four quartiles (Q1–Q4) based on their impact and prestige within each subject category, where Q1 represents the top 25% of journals and Q4 represents the lowest 25%.""")
st.markdown("""
**Research Question:** What factors (e.g., specific keywords in titles, international collaboration, subject choice) significantly impact the probability of a paper being accepted into a high-impact (Q1) journal, and can we predict this outcome using AI?
""")
st.markdown("---")

# ==========================================
# 1. Load Data & Model
# ==========================================
@st.cache_resource
def load_resources():
    try:
        # โหลดข้อมูล
        df = pd.read_csv('chula_papers_with_quality.csv')
        df = df.dropna(subset=['SJR Best Quartile']) # กรองให้สะอาด
        
        # โหลดโมเดล
        model = joblib.load('q1_predictor_model.joblib')
        
        return df, model
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return None, None

df, model = load_resources()

if df is None or model is None:
    st.stop()

# --- Data Preparation (เตรียมข้อมูลให้พร้อมใช้สำหรับทุกกราฟ) ---
# 1. สร้างตัวแปร Collaboration Type
def check_inter(country_str):
    country_str = str(country_str)
    if ';' in country_str: return 'International'
    if 'Thailand' not in country_str: return 'International'
    return 'Local (Thai Only)'

df['Collaboration Type'] = df['countries_str'].apply(check_inter)

# 2. แยก Subject ตัวแรกออกมา (ใช้สำหรับกราฟ Subject ทั้งหมด)
df['main_subject'] = df['subject_areas_str'].apply(lambda x: str(x).split(';')[0].strip())

# ==========================================
# 2. Key Metrics (KPIs)
# ==========================================
total_papers = len(df)
q1_papers = len(df[df['is_Q1'] == 1])
q1_ratio = (q1_papers / total_papers) * 100
inter_ratio = (len(df[df['Collaboration Type'] == 'International']) / total_papers) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("📄 Total Papers matched SCImago", f"{total_papers:,}")
col2.metric("🏆 Q1 Publications", f"{q1_papers:,}")
col3.metric("📈 Q1 Ratio", f"{q1_ratio:.1f}%") # <--- ส่วนที่คุณต้องการ
col4.metric("🌍 Int. Collab Rate", f"{inter_ratio:.1f}%")

st.markdown("---")

# ==========================================
# 3. Quality Trends Analysis (ส่วนที่คุณเพิ่มเข้ามา)
# ==========================================
st.header("📊 1. Quality Trends Analysis ")

tab_trend1, tab_trend2 = st.tabs(["📅 Trend by Year", "🎓 Performance by Subject"])

with tab_trend1:
    # กราฟเส้นแสดงจำนวน Q1 เทียบกับ Non-Q1 รายปี
    trend_data = df.groupby(['year', 'SJR Best Quartile']).size().reset_index(name='count')
    # กรองเฉพาะปีที่มีข้อมูลสมบูรณ์ (2018-2023)
    trend_data = trend_data[(trend_data['year'] >= 2018) & (trend_data['year'] <= 2023)]
    
    fig_trend = px.line(trend_data, x='year', y='count', color='SJR Best Quartile', 
                        title='Publication Growth by Journal Quartile (2018-2023)', markers=True,
                        category_orders={"SJR Best Quartile": ["Q1", "Q2", "Q3", "Q4", "-"]})
    st.plotly_chart(fig_trend, use_container_width=True)

with tab_trend2:
    # กราฟแท่งแสดงสัดส่วน Q1 แยกตามสาขาวิชา (เอาเฉพาะสาขาใหญ่ๆ)
    top_subjects = df['main_subject'].value_counts().nlargest(10).index
    subject_data = df[df['main_subject'].isin(top_subjects)]
    
    fig_bar = px.histogram(subject_data, y='main_subject', color='SJR Best Quartile', 
                           barmode='group', title='Journal Quartile Distribution by Top 10 Subjects',
                           category_orders={"SJR Best Quartile": ["Q1", "Q2", "Q3", "Q4"]},
                           orientation='h')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. Deep Dive Analysis (เจาะลึกปัจจัย)
# ==========================================
st.header("🔍 2. Insight Analysis")
st.write("What has the AI discovered from the data? Which factors have the greatest impact on achieving Q1 status?")

tab1, tab2, tab3 = st.tabs(["🌍 Collaboration Impact", "🔑 Magic Keywords", "📚 Subject Success Rate"])

# --- Tab 1: Collaboration ---
with tab1:
    st.subheader("Do we need support from an international co-author for the writing?")
    
    collab_stats = df.groupby('Collaboration Type')['is_Q1'].mean().reset_index()
    collab_stats['is_Q1'] = collab_stats['is_Q1'] * 100
    collab_stats.columns = ['Collaboration Type', 'Q1 Success Rate (%)']
    
    fig_collab = px.bar(collab_stats, x='Collaboration Type', y='Q1 Success Rate (%)',
                        color='Collaboration Type', text_auto='.1f',
                        color_discrete_map={'International': '#00CC96', 'Local (Thai Only)': '#EF553B'})
    st.plotly_chart(fig_collab, use_container_width=True)

# --- Tab 2: Keywords ---
with tab2:
    st.subheader("Feature Importance (Influential Keywords)")
    try:
        vectorizer = model.named_steps['preprocessor'].transformers_[0][1]
        feature_names = vectorizer.get_feature_names_out()
        rf_model = model.named_steps['classifier']
        importances = rf_model.feature_importances_
        text_importances = importances[:len(feature_names)]
        
        kw_df = pd.DataFrame({'Keyword': feature_names, 'Importance': text_importances})
        kw_df = kw_df.sort_values(by='Importance', ascending=False).head(15)
        
        fig_kw = px.bar(kw_df, x='Importance', y='Keyword', orientation='h',
                        title="Top 15 Keywords Signaling High Quality (Q1)",
                        color='Importance', color_continuous_scale='Viridis')
        fig_kw.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_kw, use_container_width=True)
    except:
        st.warning("Feature Importance unavailable.")

# --- Tab 3: Subject Success Rate ---
with tab3:
    st.subheader("Success Rate by Research Field")
    # อันนี้ต่างจากกราฟข้างบนคือกราฟนี้ดู % ความสำเร็จ ไม่ใช่จำนวนเล่ม
    subject_counts = df['main_subject'].value_counts()
    valid_subjects = subject_counts[subject_counts > 30].index
    
    sub_df = df[df['main_subject'].isin(valid_subjects)]
    sub_stats = sub_df.groupby('main_subject')['is_Q1'].mean().reset_index()
    sub_stats['is_Q1'] = sub_stats['is_Q1'] * 100
    sub_stats = sub_stats.sort_values('is_Q1', ascending=False).head(10)
    
    fig_sub = px.bar(sub_stats, x='is_Q1', y='main_subject', orientation='h',
                     title="Top Subject Areas by Q1 Success Rate (%)",
                     labels={'is_Q1': '% Success Rate'}, text_auto='.1f')
    fig_sub.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_sub, use_container_width=True)

# ==========================================
# 5. AI Prediction Section
# ==========================================
st.markdown("---")
st.header("🤖 3. AI Predictor: Try Predicting Your Research Performance")

col_input, col_result = st.columns([1, 1])

with col_input:
    st.markdown("#### Input Details")
    user_title = st.text_input("1. Research Title:", 
                              "Deep Learning Approaches for Early Detection of Lung Cancer")
    
    user_collab = st.radio("2. Collaboration:", 
                           ["Local (Thai Only)", "International"], horizontal=True)
    
    subjects_list = sorted(df['main_subject'].unique())
    default_idx = subjects_list.index('Medicine') if 'Medicine' in subjects_list else 0
    user_subject = st.selectbox("3. Subject Area:", subjects_list, index=default_idx)

with col_result:
    st.markdown("#### Prediction Result")
    if st.button("🚀 Analyze Quality Potential", type="primary"):
        input_data = pd.DataFrame({
            'title': [user_title],
            'is_inter': ['Yes' if user_collab == "International" else 'No'],
            'primary_subject': [user_subject]
        })
        
        prediction = model.predict(input_data)[0]
        probs = model.predict_proba(input_data)[0]
        q1_prob = probs[1]
        
        st.write("---")
        if prediction == 1:
            st.success(f"### 🎉 High Potential (Q1)")
            st.metric("Probability", f"{q1_prob:.1%}")
            st.write("The model predicts that this work has a high probability of being published in a Q1 journal.")
        else:
            st.warning(f"### 📝 Standard Potential (Q2-Q4)")
            st.metric("Probability of Q1", f"{q1_prob:.1%}")
            st.write("This research shows a tendency to be at the level of Q2-Q4")

# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.caption("Developed for Data Science Project | Data Source: Chulalongkorn University (2018-2023) & Scimago Journal Rank 2023")