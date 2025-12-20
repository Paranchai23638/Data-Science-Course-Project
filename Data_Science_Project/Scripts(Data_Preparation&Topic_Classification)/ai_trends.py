from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "topic_clustered.csv"

df = pd.read_csv(CSV_PATH)

df["year"] = df["year"].astype(str)

df["title"] = df["title"].fillna("")
df["abstract"] = df["abstract"].fillna("")
df["text"] = (df["title"] + " " + df["abstract"]).str.lower()

ai_keywords = [
    "machine learning",
    "deep learning",
    "neural network",
    "neural networks",
    "artificial intelligence",
    "convolutional neural network",
    "cnn ",
    " cnn",
    "lstm",
    "rnn",
    "transformer",
    "bert",
    "svm",
    "support vector machine",
    "random forest",
    "xgboost",
    "classification model",
    "regression model",
    "predictive model",
    "data mining"
]

patterns = [re.compile(re.escape(k)) for k in ai_keywords]

def is_ai(text):
    return any(p.search(text) for p in patterns)

df["is_ai"] = df["text"].apply(is_ai)

ai_by_year = (
    df.groupby("year")["is_ai"]
    .agg(ai_papers="sum", total_papers="count")
    .reset_index()
)
ai_by_year["ai_ratio"] = ai_by_year["ai_papers"] / ai_by_year["total_papers"]

print("AI papers per year:")
print(ai_by_year)

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

df["topic_name"] = df["cluster"].map(topic_names)

ai_by_topic = (
    df.groupby("topic_name")["is_ai"]
    .agg(ai_papers="sum", total_papers="count")
    .reset_index()
)
ai_by_topic["ai_ratio"] = ai_by_topic["ai_papers"] / ai_by_topic["total_papers"]

print("\nAI papers by topic:")
print(ai_by_topic.sort_values("ai_ratio", ascending=False))

ai_year_path = PROJECT_ROOT / "ai_trends_year.csv"
ai_topic_path = PROJECT_ROOT / "ai_trends_topic.csv"

ai_by_year.to_csv(ai_year_path, index=False)
ai_by_topic.to_csv(ai_topic_path, index=False)

print("\nSaved AI trends by year to", ai_year_path)
print("Saved AI trends by topic to", ai_topic_path)

plt.figure(figsize=(8, 5))
plt.plot(ai_by_year["year"], ai_by_year["ai_papers"], marker="o")
plt.title("Number of AI-related Papers per Year")
plt.xlabel("Year")
plt.ylabel("AI-related Papers")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
ai_by_topic_sorted = ai_by_topic.sort_values("ai_papers", ascending=False)
plt.barh(ai_by_topic_sorted["topic_name"], ai_by_topic_sorted["ai_papers"])
plt.title("AI-related Papers by Topic")
plt.xlabel("AI-related Papers")
plt.tight_layout()
plt.show()