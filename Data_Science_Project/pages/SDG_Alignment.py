from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Config
st.set_page_config(page_title="Chula SDG Tracker", layout="wide", page_icon="🌍")

# Colors for SDGs (สีมาตรฐาน UN)
sdg_colors = {
    'SDG 1': '#E5243B', 'SDG 2': '#DDA63A', 'SDG 3': '#4C9F38', 'SDG 4': '#C5192D',
    'SDG 5': '#FF3A21', 'SDG 6': '#26BDE2', 'SDG 7': '#FCC30B', 'SDG 8': '#A21942',
    'SDG 9': '#FD6925', 'SDG 10': '#DD1367', 'SDG 11': '#FD9D24', 'SDG 12': '#BF8B2E',
    'SDG 13': '#3F7E44', 'SDG 14': '#0A97D9', 'SDG 15': '#56C02B', 'SDG 16': '#00689D',
    'SDG 17': '#19486A', 'General / Non-SDG': '#CCCCCC'
}

# SDG Descriptions (English)
sdg_descriptions = {
    "SDG 1": "No Poverty: End poverty in all its forms everywhere.",
    "SDG 2": "Zero Hunger: End hunger, achieve food security and improved nutrition, and promote sustainable agriculture.",
    "SDG 3": "Good Health and Well-being: Ensure healthy lives and promote well-being for all at all ages.",
    "SDG 4": "Quality Education: Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.",
    "SDG 5": "Gender Equality: Achieve gender equality and empower all women and girls.",
    "SDG 6": "Clean Water and Sanitation: Ensure availability and sustainable management of water and sanitation for all.",
    "SDG 7": "Affordable and Clean Energy: Ensure access to affordable, reliable, sustainable and modern energy for all.",
    "SDG 8": "Decent Work and Economic Growth: Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all.",
    "SDG 9": "Industry, Innovation and Infrastructure: Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation.",
    "SDG 10": "Reduced Inequalities: Reduce inequality within and among countries.",
    "SDG 11": "Sustainable Cities and Communities: Make cities and human settlements inclusive, safe, resilient and sustainable.",
    "SDG 12": "Responsible Consumption and Production: Ensure sustainable consumption and production patterns.",
    "SDG 13": "Climate Action: Take urgent action to combat climate change and its impacts.",
    "SDG 14": "Life Below Water: Conserve and sustainably use the oceans, seas and marine resources.",
    "SDG 15": "Life on Land: Protect, restore and promote sustainable use of terrestrial ecosystems.",
    "SDG 16": "Peace, Justice and Strong Institutions: Promote peaceful and inclusive societies, provide access to justice for all and build effective, accountable institutions.",
    "SDG 17": "Partnerships for the Goals: Strengthen the means of implementation and revitalize the global partnership for sustainable development."
}


st.title("🌍 Chula Research for Sustainability (SDGs)")
st.markdown("Classification of research studies according to the United Nations Sustainable Development Goals (SDGs) using AI (Semantic Analysis).")
st.markdown("""
**Research Question:** Which SDG area receives the greatest research focus at Chulalongkorn University (e.g., health, clean energy, or inequality)?
""")
st.markdown("---")
# 1. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('chula_sdg_classified.csv')

try:
    df = load_data()
except:
    st.error("ไม่พบไฟล์ chula_sdg_classified.csv กรุณารัน train_sdg.py ก่อน")
    st.stop()

# ตัด General ออก เพื่อดูเฉพาะงาน SDG (หรือจะเก็บไว้ก็ได้แล้วแต่ชอบ)
sdf = df[df['Predicted SDG'] != 'General / Non-SDG']

# ==========================================
# 2. KPI Section
# ==========================================
total_papers = len(df)
sdg_papers = len(sdf)
top_sdg = sdf['Predicted SDG'].mode()[0]

col1, col2, col3 = st.columns(3)
col1.metric("📚 Total Papers Analyzed", f"{total_papers:,}")
col2.metric("🌱 SDG-Related Papers", f"{sdg_papers:,} ({sdg_papers/total_papers*100:.1f}%)")
col3.metric("🥇 Top Focus Area", top_sdg)

st.markdown("---")

# ==========================================
# 3. Visualization
# ==========================================
col_chart, col_details = st.columns([2, 1])

with col_chart:
    st.subheader("📊 SDG Distribution") 
    
    # นับจำนวน
    sdg_counts = sdf['Predicted SDG'].value_counts().reset_index()
    sdg_counts.columns = ['SDG', 'Count']
    
    # Sort ตามเลข SDG (เช่น SDG 1, SDG 2...)
    sdg_counts['SortKey'] = sdg_counts['SDG'].apply(lambda x: int(x.split(' ')[1]) if 'SDG' in x else 99)
    sdg_counts = sdg_counts.sort_values('SortKey')

    fig = px.bar(sdg_counts, x='SDG', y='Count', 
                 color='SDG', text='Count',
                 color_discrete_map=sdg_colors,
                 title="Number of Papers per SDG Goal")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col_details:
    st.subheader("💡 Highlight")
    st.write("The primary research focus of Chulalongkorn University is on: ")
    
    top_3 = sdf['Predicted SDG'].value_counts().head(3)
    for i, (name, count) in enumerate(top_3.items()):
        st.info(f"**{i+1}. {name}**: {count} papers")
        
    st.caption("AI performs the analysis by comparing research titles with the official UN definitions.")

# ==========================================
# 4. Interactive Explorer
# ==========================================
st.markdown("---")
st.subheader("🔍 Search Research by SDG")

selected_sdg = st.selectbox("Select the SDG you want to explore:", sorted(sdf['Predicted SDG'].unique(), key=lambda x: int(x.split(' ')[1])))

# Show SDG Description
if selected_sdg in sdg_descriptions:
    st.info(f"📘 **{selected_sdg} Description:**\n\n{sdg_descriptions[selected_sdg]}")


filtered_df = sdf[sdf['Predicted SDG'] == selected_sdg].sort_values('SDG Score', ascending=False)

st.write(f"Found **{len(filtered_df)}** articles in the category {selected_sdg}")
st.dataframe(
    filtered_df[['title', 'year', 'journal', 'SDG Score']].head(50),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.caption("Note: Classification is based on Unsupervised Semantic Similarity (Sentence-BERT). Threshold > 0.25")