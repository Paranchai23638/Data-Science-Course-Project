import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLUSTER_PATH = PROJECT_ROOT / "topic_clustered.csv"
TRENDS_PATH = PROJECT_ROOT / "topic_trends.csv"

st.title("Topics")


@st.cache_data
def load_cluster():
    df = pd.read_csv(CLUSTER_PATH)
    df["year"] = df["year"].astype(str)
    topic_names = {
        0: "Biodiversity & Species Discovery",
        1: "Catalysis & CO2 Conversion",
        2: "Education & Social/Public Health",
        3: "Materials Science & Adsorption",
        4: "Cancer Biology & Drug Discovery",
        5: "Biomedical Experiments & Genetics",
        6: "Clinical Patient Studies",
        7: "COVID-19 & Vaccine Research",
        8: "Particle Physics (LHC)",
        9: "Machine Learning & Modeling",
    }
    if "topic_name" not in df.columns:
        df["topic_name"] = df["cluster"].map(topic_names)
    return df


@st.cache_data
def load_trends():
    return pd.read_csv(TRENDS_PATH, index_col="year")


df = load_cluster()
trends = load_trends()

st.subheader("Topic Sizes")
topic_counts = df["topic_name"].value_counts()

fig, ax = plt.subplots(figsize=(8, 5))
topic_counts.sort_values().plot(kind="barh", ax=ax)
ax.set_xlabel("Number of Papers")
st.pyplot(fig)

st.markdown("---")
st.subheader("Topic Trends (2018-2023)")

fig, ax = plt.subplots(figsize=(8, 5))
for col in trends.columns:
    ax.plot(trends.index, trends[col], marker="o", label=col)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
ax.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)

st.markdown("---")
st.subheader("Topic Explorer")

topic_list = sorted(df["topic_name"].dropna().unique())
selected_topic = st.selectbox("Select topic", topic_list)

topic_df = df[df["topic_name"] == selected_topic][["year", "title"]]

year_options = ["All years"] + sorted(topic_df["year"].unique(), reverse=True)
selected_year = st.selectbox("Filter by year", year_options)

if selected_year != "All years":
    topic_df = topic_df[topic_df["year"] == selected_year]

topic_df = topic_df.sort_values(["year", "title"], ascending=[False, True]).reset_index(drop=True)

st.dataframe(topic_df, width="stretch", height=400)

st.markdown("---")