import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "papers_all_years.csv"

print("Loading:", CSV_PATH)

df = pd.read_csv(CSV_PATH)
df["year"] = df["year"].astype(str)

print("Number of papers:", len(df))
print(df.head())

pub_per_year = df["year"].value_counts().sort_index()
print("\nPublications per year:")
print(pub_per_year)

pub_per_year.plot(kind="bar")
plt.title("Number of Publications Per Year (2018–2023)")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.show()

top_journals = df["journal"].value_counts().head(15)
print("\nTop 15 Journals:")
print(top_journals)

top_journals.plot(kind="barh")
plt.title("Top 15 Journals (All Years)")
plt.xlabel("Count")
plt.tight_layout()
plt.show()

df["citedby_count"].plot(kind="hist", bins=60)
plt.title("Citation Distribution (All Years)")
plt.xlabel("Citations")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

subjects = (
    df["subject_areas_str"]
    .dropna()
    .str.split("; ")
    .explode()
)

subject_counts = subjects.value_counts().head(20)
print("\nTop 20 Subject Areas:")
print(subject_counts)

subject_counts.plot(kind="barh")
plt.title("Top 20 Subject Areas (All Years)")
plt.xlabel("Count")
plt.tight_layout()
plt.show()

countries = (
    df["countries_str"]
    .dropna()
    .str.split("; ")
    .explode()
)

country_counts = countries.value_counts().head(15)
print("\nTop 15 Countries:")
print(country_counts)

country_counts.plot(kind="barh")
plt.title("Top 15 Affiliation Countries")
plt.xlabel("Count")
plt.tight_layout()
plt.show()
