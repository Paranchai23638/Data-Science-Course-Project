from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "topic_data.csv"

df = pd.read_csv(CSV_PATH)
df = df.dropna(subset=["abstract"])
df["abstract"] = df["abstract"].astype(str)
df["year"] = df["year"].astype(str)

vectorizer = TfidfVectorizer(max_features=20000, stop_words="english")
X = vectorizer.fit_transform(df["abstract"])

k = 10
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X)

df["cluster"] = cluster_labels

feature_names = vectorizer.get_feature_names_out()
top_n = 15
topics = []

for i in range(k):
    center = kmeans.cluster_centers_[i]
    top_indices = center.argsort()[::-1][:top_n]
    top_words = [feature_names[j] for j in top_indices]
    topics.append(top_words)
    print(f"Cluster {i}: {', '.join(top_words)}")

cluster_counts = df["cluster"].value_counts().sort_index()
print("\nCluster sizes:")
print(cluster_counts)

plt.figure()
cluster_counts.plot(kind="bar")
plt.title("Number of Papers per Cluster")
plt.xlabel("Cluster")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

topic_by_year = df.groupby(["year", "cluster"])["eid"].count().unstack(fill_value=0)
print("\nPapers per year per cluster:")
print(topic_by_year)

output_csv = PROJECT_ROOT / "topic_clustered.csv"
df.to_csv(output_csv, index=False)
print("\nSaved clustered data to", output_csv)