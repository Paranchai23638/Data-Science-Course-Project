import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "papers_all_years.csv"

st.title("Overview")

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

st.markdown("### Key Figures")

total_papers = len(df)
years = sorted(df["year"].unique())
year_range = f"{years[0]}–{years[-1]}"
num_journals = df["journal"].nunique()
countries = (
    df["countries_str"]
    .dropna()
    .str.split("; ")
    .explode()
    .unique()
)
num_countries = len(countries)

col1, col2, col3 = st.columns(3)
col1.metric("Total Papers", f"{total_papers:,}", year_range)
col2.metric("Unique Journals", f"{num_journals:,}")
col3.metric("Affiliation Countries", f"{num_countries:,}")

st.markdown("---")

st.markdown("### Publications per Year")

pub_per_year = df["year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(6, 4))
pub_per_year.plot(kind="bar", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
ax.set_title("Number of Publications Per Year")
st.pyplot(fig)

st.markdown("---")
st.markdown("### Publication Share by Subject Area")

subjects = (
    df["subject_areas_str"]
    .dropna()
    .str.split("; ")
    .explode()
)

subject_counts = subjects.value_counts().head(10)
labels = subject_counts.index
sizes = subject_counts.values

fig2, ax2 = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax2.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.8,
)

centre_circle = plt.Circle((0, 0), 0.60, fc="white")
fig2.gca().add_artist(centre_circle)

ax2.set_title("Top Subject Areas (Share of Publications)")
ax2.axis("equal")
st.pyplot(fig2)

st.markdown("---")
st.markdown("### Top 10 Journals")

top_journals = df["journal"].value_counts().head(10)

fig3, ax3 = plt.subplots(figsize=(6, 4))
top_journals.sort_values().plot(kind="barh", ax=ax3)
ax3.set_xlabel("Number of Papers")
ax3.set_ylabel("Journal")
ax3.set_title("Top 10 Journals")
st.pyplot(fig3)

st.markdown("---")
st.markdown("### Top 15 Affiliation Countries")

countries_series = (
    df["countries_str"]
    .dropna()
    .str.split("; ")
    .explode()
)

country_counts = countries_series.value_counts().head(15)

fig4, ax4 = plt.subplots(figsize=(6, 5))
country_counts.sort_values().plot(kind="barh", ax=ax4)
ax4.set_xlabel("Number of Papers")
ax4.set_ylabel("Country")
ax4.set_title("Top 15 Countries")
st.pyplot(fig4)

st.markdown("---")