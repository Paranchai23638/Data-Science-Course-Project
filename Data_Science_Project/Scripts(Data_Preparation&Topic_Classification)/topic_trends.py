from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "topic_clustered.csv"

df = pd.read_csv(CSV_PATH)

df["year"] = df["year"].astype(str)
df["cluster"] = df["cluster"].astype(int)

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

grouped = df.groupby(["year", "topic_name"])["eid"].count().reset_index()
pivot = grouped.pivot(index="year", columns="topic_name", values="eid").fillna(0).astype(int)

print("Papers per year per topic:")
print(pivot)

out_csv = PROJECT_ROOT / "topic_trends.csv"
pivot.to_csv(out_csv)
print("\nSaved topic trends to", out_csv)

plt.figure(figsize=(10, 6))
for col in pivot.columns:
    plt.plot(pivot.index, pivot[col], marker="o", label=col)

plt.title("Number of Papers per Topic (2018–2023)")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()