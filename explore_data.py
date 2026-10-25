"""
explore_data.py
---------------
Step 1: Explore and understand the dataset.
        Learn: pandas basics, data visualization

Concepts covered:
  - Loading CSV with pandas
  - df.head(), df.info(), df.describe()
  - Groupby & aggregations
  - Matplotlib & Seaborn plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
movies = pd.read_csv("movies.csv")

print("=" * 50)
print("📋 DATASET OVERVIEW")
print("=" * 50)
print(f"\n🎬 Total Movies: {len(movies)}")
print("\nFirst 5 rows:")
print(movies.head())

print("\nColumn info:")
print(movies.info())

print("\nBasic statistics:")
print(movies.describe())

# ─────────────────────────────────────────────
# 2. TOP RATED MOVIES
# ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("⭐ TOP 10 RATED MOVIES")
print("=" * 50)
top_movies = movies.sort_values("rating", ascending=False).head(10)
print(top_movies[["title", "genre", "rating", "year"]].to_string(index=False))

# ─────────────────────────────────────────────
# 3. GENRE DISTRIBUTION
# ─────────────────────────────────────────────
genre_counts = movies["genre"].value_counts()
print("\n🎭 Genre Distribution:")
print(genre_counts)

# ─────────────────────────────────────────────
# 4. VISUALIZATIONS
# ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("🎬 Movie Dataset - Exploratory Analysis", fontsize=16, fontweight="bold")

# Plot 1: Genre count
sns.countplot(data=movies, x="genre", ax=axes[0, 0],
              palette="Set2", order=movies["genre"].value_counts().index)
axes[0, 0].set_title("Movies per Genre")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].set_xlabel("")

# Plot 2: Rating distribution
sns.histplot(movies["rating"], bins=10, kde=True, ax=axes[0, 1], color="steelblue")
axes[0, 1].set_title("Rating Distribution")
axes[0, 1].set_xlabel("IMDb Rating")

# Plot 3: Average rating by genre
avg_rating = movies.groupby("genre")["rating"].mean().sort_values(ascending=False)
avg_rating.plot(kind="bar", ax=axes[1, 0], color="coral", edgecolor="black")
axes[1, 0].set_title("Average Rating by Genre")
axes[1, 0].tick_params(axis="x", rotation=45)
axes[1, 0].set_xlabel("")

# Plot 4: Rating vs Votes scatter
sns.scatterplot(data=movies, x="votes", y="rating", hue="genre",
                ax=axes[1, 1], s=100, alpha=0.8)
axes[1, 1].set_title("Rating vs Popularity (Votes)")
axes[1, 1].set_xlabel("Number of Votes")
axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)

plt.tight_layout()
plt.savefig("exploration.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as exploration.png")
