"""
visualize_similarity.py
-----------------------
Step 4: Visualize Movie Similarities using a Heatmap
        See which movies are most alike!

Concepts covered:
  - Heatmaps with seaborn
  - Annotated charts
  - Subplots & figure customization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

# ─────────────────────────────────────────────
# LOAD & PREPARE
# ─────────────────────────────────────────────
movies = pd.read_csv("movies.csv")
movies["tags"] = movies["genre"] + " " + movies["language"]

tfidf   = TfidfVectorizer()
tfidf_m = tfidf.fit_transform(movies["tags"])
sim_mat = cosine_similarity(tfidf_m)

# Use short titles for readability
short_titles = [t[:15] for t in movies["title"]]

# ─────────────────────────────────────────────
# FIGURE 1: Similarity Heatmap
# ─────────────────────────────────────────────
plt.figure(figsize=(16, 12))
sns.heatmap(
    sim_mat,
    xticklabels=short_titles,
    yticklabels=short_titles,
    cmap="YlOrRd",
    linewidths=0.3,
    annot=False
)
plt.title("🎬 Movie Similarity Heatmap\n(Brighter = More Similar)", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig("similarity_heatmap.png", dpi=150)
plt.show()
print("✅ Saved: similarity_heatmap.png")

# ─────────────────────────────────────────────
# FIGURE 2: PCA — Movies in 2D Space
# ─────────────────────────────────────────────
# PCA reduces high-dimensional vectors to 2D for visualization
pca = PCA(n_components=2)
coords = pca.fit_transform(tfidf_m.toarray())

pca_df = pd.DataFrame(coords, columns=["x", "y"])
pca_df["title"] = movies["title"]
pca_df["genre"] = movies["genre"]

plt.figure(figsize=(12, 8))
genres = movies["genre"].unique()
colors = plt.cm.Set1(np.linspace(0, 1, len(genres)))

for genre, color in zip(genres, colors):
    subset = pca_df[pca_df["genre"] == genre]
    plt.scatter(subset["x"], subset["y"], label=genre, color=color, s=120, alpha=0.8)
    for _, row in subset.iterrows():
        plt.annotate(row["title"], (row["x"], row["y"]),
                     fontsize=7, alpha=0.85,
                     xytext=(4, 4), textcoords="offset points")

plt.title("🎬 Movies in 2D Space (PCA)\nSimilar movies cluster together!", fontsize=13)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(loc="upper right", fontsize=9)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("pca_clusters.png", dpi=150)
plt.show()
print("✅ Saved: pca_clusters.png")

# ─────────────────────────────────────────────
# FIGURE 3: Top 5 Similar Movies for a Pick
# ─────────────────────────────────────────────
TARGET = "Inception"
idx = movies[movies["title"] == TARGET].index[0]
scores = list(enumerate(sim_mat[idx]))
scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

similar_movies = [movies.iloc[i]["title"] for i, _ in scores]
similar_scores = [round(s, 3) for _, s in scores]

plt.figure(figsize=(8, 5))
bars = plt.barh(similar_movies, similar_scores, color="steelblue", edgecolor="black")
plt.xlabel("Cosine Similarity Score")
plt.title(f"🎬 Movies Most Similar to '{TARGET}'")
plt.xlim(0, 1.1)
for bar, score in zip(bars, similar_scores):
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
             str(score), va="center", fontsize=10)
plt.tight_layout()
plt.savefig("top_similar.png", dpi=150)
plt.show()
print("✅ Saved: top_similar.png")
