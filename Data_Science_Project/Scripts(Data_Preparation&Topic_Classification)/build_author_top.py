from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EDGES_PATH = PROJECT_ROOT / "author_edges.csv"

chunksize = 500000
counts = {}

for chunk in pd.read_csv(EDGES_PATH, chunksize=chunksize):
    for col in ["source", "target"]:
        vals = chunk[col].value_counts()
        for name, c in vals.items():
            counts[name] = counts.get(name, 0) + int(c)

deg_df = pd.DataFrame(
    {"author": list(counts.keys()), "degree": list(counts.values())}
)
deg_df = deg_df.sort_values("degree", ascending=False)

top_n = 100
top_authors = deg_df.head(top_n)["author"].tolist()

print("Top authors:")
print(deg_df.head(20))

EDGES_TOP_PATH = PROJECT_ROOT / "author_top_edges.csv"
NODES_TOP_PATH = PROJECT_ROOT / "author_top_nodes.csv"
DEGREES_PATH = PROJECT_ROOT / "author_degrees.csv"

deg_df.to_csv(DEGREES_PATH, index=False)

edges_top = []

for chunk in pd.read_csv(EDGES_PATH, chunksize=chunksize):
    mask = chunk["source"].isin(top_authors) | chunk["target"].isin(top_authors)
    edges_top.append(chunk.loc[mask])

edges_top_df = pd.concat(edges_top, ignore_index=True)
edges_top_df.to_csv(EDGES_TOP_PATH, index=False)

nodes_top_df = pd.DataFrame({"node": top_authors, "type": "author"})
nodes_top_df.to_csv(NODES_TOP_PATH, index=False)

print("Saved author degrees to", DEGREES_PATH)
print("Saved top edges to", EDGES_TOP_PATH)
print("Saved top nodes to", NODES_TOP_PATH)