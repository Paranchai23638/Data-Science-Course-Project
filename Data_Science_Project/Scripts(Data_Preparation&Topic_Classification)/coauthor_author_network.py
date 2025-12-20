from pathlib import Path

import pandas as pd
import networkx as nx
# import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "papers_all_years.csv"

df = pd.read_csv(CSV_PATH, usecols=["authors_str"])
df = df.dropna(subset=["authors_str"])

edges_set = set()

for authors_str in df["authors_str"]:
    authors = [a.strip() for a in str(authors_str).split(";") if a.strip()]
    n = len(authors)
    for i in range(n):
        for j in range(i + 1, n):
            a = authors[i]
            b = authors[j]
            if a < b:
                edges_set.add((a, b))
            else:
                edges_set.add((b, a))

edges = list(edges_set)
print("Total unique co-author pairs (edges):", len(edges))

G = nx.Graph()
G.add_edges_from(edges)

deg = dict(G.degree())
top_authors = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:50]

print("\nTop 20 authors by degree (number of co-authors):")
for name, d in top_authors[:20]:
    print(f"{name}: {d}")

nodes = list(G.nodes())
nodes_df = pd.DataFrame({"node": nodes})
nodes_df["type"] = "author"

edges_df = pd.DataFrame(edges, columns=["source", "target"])

nodes_path = PROJECT_ROOT / "author_nodes.csv"
edges_path = PROJECT_ROOT / "author_edges.csv"

nodes_df.to_csv(nodes_path, index=False)
edges_df.to_csv(edges_path, index=False)

print("\nSaved author nodes to", nodes_path)
print("Saved author edges to", edges_path)

# top_author_names = [name for name, _ in top_authors]
# sub_nodes = set(top_author_names)
# for a in top_author_names:
#     sub_nodes.update(G.neighbors(a))
# 
# H = G.subgraph(sub_nodes).copy()
# 
# pos = nx.spring_layout(H, k=0.3, iterations=50)
# plt.figure(figsize=(10, 8))
# 
# nx.draw_networkx_nodes(H, pos, nodelist=top_author_names, node_size=120)
# other_nodes = [n for n in H.nodes if n not in top_author_names]
# nx.draw_networkx_nodes(H, pos, nodelist=other_nodes, node_size=40)
# nx.draw_networkx_edges(H, pos, alpha=0.3)
# 
# labels = {n: n[:15] for n in top_author_names}
# nx.draw_networkx_labels(H, pos, labels=labels, font_size=6)
# 
# plt.title("Co-author Network (Top Authors)")
# plt.axis("off")
# plt.tight_layout()
# plt.show()