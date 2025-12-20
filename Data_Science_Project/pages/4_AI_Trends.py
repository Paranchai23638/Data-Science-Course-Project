import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
YEAR_PATH = PROJECT_ROOT / "ai_trends_year.csv"
TOPIC_PATH = PROJECT_ROOT / "ai_trends_topic.csv"

st.title("AI-related Research Trends")

@st.cache_data
def load_year():
    return pd.read_csv(YEAR_PATH)

@st.cache_data
def load_topic():
    return pd.read_csv(TOPIC_PATH)

df_year = load_year()
df_topic = load_topic()

st.subheader("AI Papers per Year")
fig1, ax1 = plt.subplots()
ax1.plot(df_year["year"], df_year["ai_papers"], marker="o")
ax1.set_xlabel("Year")
ax1.set_ylabel("AI-related Papers")
st.pyplot(fig1)

st.markdown("---")
st.subheader("Share of AI Papers per Year")
fig2, ax2 = plt.subplots()
ax2.plot(df_year["year"], df_year["ai_ratio"], marker="o")
ax2.set_xlabel("Year")
ax2.set_ylabel("AI Ratio")
st.pyplot(fig2)

st.markdown("---")
st.subheader("AI Papers by Topic")
df_topic_sorted = df_topic.sort_values("ai_papers", ascending=False)
fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.barh(df_topic_sorted["topic_name"], df_topic_sorted["ai_papers"])
ax3.set_xlabel("AI-related Papers")
st.pyplot(fig3)

st.markdown("---")
st.subheader("Summary Tables")
col1, col2 = st.columns(2)
with col1:
    st.write("AI trends by year")
    st.dataframe(df_year)
with col2:
    st.write("AI trends by topic")
    st.dataframe(df_topic_sorted)

st.markdown("---")