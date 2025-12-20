from pathlib import Path

import streamlit as st
import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from pyvis.network import Network

st.title("Global Co-author Network (Top 100 Authors)")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EDGES_PATH = PROJECT_ROOT / "author_top_edges.csv"
DEG_PATH = PROJECT_ROOT / "author_degrees.csv"


@st.cache_data
def load_data():
    deg = pd.read_csv(DEG_PATH)
    edges = pd.read_csv(EDGES_PATH)
    return deg, edges


deg_df, edges_df = load_data()

if "weight" not in edges_df.columns:
    edges_df["weight"] = 1

deg_df = deg_df.sort_values("degree", ascending=False)
top_authors = deg_df["author"].head(100).tolist()
top_author_set = set(top_authors)

edges_small = edges_df[
    edges_df["source"].isin(top_author_set)
    & edges_df["target"].isin(top_author_set)
]

top_edges_list = []
for author in top_authors:
    sub = edges_small[
        (edges_small["source"] == author)
        | (edges_small["target"] == author)
    ]
    sub = sub.sort_values("weight", ascending=False).head(3)
    top_edges_list.append(sub)

top_edges = pd.concat(top_edges_list).drop_duplicates()

G = nx.Graph()
for _, row in top_edges.iterrows():
    G.add_edge(row["source"], row["target"], weight=row["weight"])

communities = list(greedy_modularity_communities(G))
palette = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
    "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"
]
node_comm = {}
for i, comm in enumerate(communities):
    for n in comm:
        node_comm[n] = palette[i % len(palette)]

deg_df_top = deg_df[deg_df["author"].isin(top_authors)].reset_index(drop=True)
deg_df_top["rank"] = deg_df_top["degree"].rank(ascending=False, method="dense")
rank_map = dict(zip(deg_df_top["author"], deg_df_top["rank"]))
deg_map = dict(zip(deg_df_top["author"], deg_df_top["degree"]))
max_rank = int(deg_df_top["rank"].max())


def node_size(author: str) -> float:
    r = int(rank_map.get(author, max_rank + 1))
    return 10 + (max_rank + 1 - r) * 0.6


net = Network(
    height="800px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#111111"
)

net.set_options(
    """
{
  "nodes": {
    "font": {
      "size": 24,
      "face": "arial",
      "color": "#222222"
    },
    "labelHighlightBold": true
  },
  "edges": {
    "color": {
      "color": "#cccccc",
      "highlight": "#888888"
    },
    "smooth": false
  },
  "physics": {
    "enabled": true,
    "solver": "forceAtlas2Based",
    "forceAtlas2Based": {
      "gravitationalConstant": -120,
      "centralGravity": 0.008,
      "springLength": 260,
      "springConstant": 0.05,
      "avoidOverlap": 1
    },
    "minVelocity": 0.75,
    "stabilization": { "iterations": 200 }
  }
}
"""
)

for node in G.nodes():
    size = node_size(node)
    color = node_comm.get(node, "#bbbbbb")
    degree = int(deg_map.get(node, 0))
    title = f"{node}<br>Co-authors: {degree}"

    net.add_node(
        node,
        label=node,
        color=color,
        size=size,
        title=title
    )

for u, v, data in G.edges(data=True):
    w = int(data.get("weight", 1))
    width = 1 + min(w, 4)
    net.add_edge(u, v, width=width, title=f"{w} shared paper(s)")

html = net.generate_html()

st.write(
    "Nodes are sized by number of collaborators. "
    "Colors represent collaboration communities. "
    "Edges represent co-authorship, thickness = number of shared papers."
)

st.components.v1.html(html, height=800, scrolling=False)

st.markdown("---")