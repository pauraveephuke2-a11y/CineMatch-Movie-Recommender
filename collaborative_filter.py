"""
collaborative_filter.py
-----------------------
Step 3: Collaborative Filtering — "Users Like You Also Liked..."
        This recommends based on what similar USERS rated highly.

Concepts covered:
  - Pivot tables (matrix of users × movies)
  - Pearson / Cosine similarity between users
  - Handling missing data with fillna
  - User-based collaborative filtering
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
movies  = pd.read_csv("movies.csv")
ratings = pd.read_csv("user_ratings.csv")

# Merge to get movie titles in ratings
ratings = ratings.merge(movies[["movie_id", "title"]], on="movie_id")

print("=" * 55)
print("👥  COLLABORATIVE FILTERING RECOMMENDER  👥")
print("=" * 55)
print("\nSample user ratings:")
print(ratings.head(10).to_string(index=False))

# ─────────────────────────────────────────────
# 2. CREATE USER-MOVIE MATRIX (Pivot Table)
# ─────────────────────────────────────────────
# Rows = Users, Columns = Movies, Values = Rating
# Missing ratings filled with 0
user_movie_matrix = ratings.pivot_table(
    index="user",
    columns="title",
    values="user_rating"
).fillna(0)

print(f"\n📊 User-Movie Matrix Shape: {user_movie_matrix.shape}")
print("   (Rows = Users, Columns = Movies)")
print(user_movie_matrix.iloc[:5, :5])

# ─────────────────────────────────────────────
# 3. COMPUTE USER-USER SIMILARITY
# ─────────────────────────────────────────────
user_similarity = cosine_similarity(user_movie_matrix)
user_sim_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)

print("\n🤝 User Similarity Matrix (first 5 users):")
print(user_sim_df.iloc[:5, :5].round(2))

# ─────────────────────────────────────────────
# 4. COLLABORATIVE RECOMMENDATION FUNCTION
# ─────────────────────────────────────────────
def collaborative_recommend(target_user, top_n=5):
    """
    Find users similar to target_user and recommend
    movies they loved that target_user hasn't seen yet.
    """
    if target_user not in user_sim_df.index:
        print(f"❌ User '{target_user}' not found!")
        return

    # Find top 3 most similar users (exclude self)
    similar_users = (
        user_sim_df[target_user]
        .drop(target_user)
        .sort_values(ascending=False)
        .head(3)
    )

    print(f"\n🔍 Target User: {target_user}")
    print(f"   Most Similar Users: {list(similar_users.index)}")

    # Movies already seen by target user
    seen_movies = set(
        ratings[ratings["user"] == target_user]["title"]
    )

    # Collect high-rated movies from similar users (not yet seen)
    recommendations = {}
    for sim_user, sim_score in similar_users.items():
        sim_user_ratings = ratings[
            (ratings["user"] == sim_user) &
            (~ratings["title"].isin(seen_movies)) &
            (ratings["user_rating"] >= 8.0)  # only high-rated picks
        ]
        for _, row in sim_user_ratings.iterrows():
            movie = row["title"]
            if movie not in recommendations:
                recommendations[movie] = 0
            recommendations[movie] += sim_score * row["user_rating"]

    if not recommendations:
        print("   No new recommendations found (try adjusting the rating threshold)")
        return

    # Sort by weighted score
    rec_df = pd.DataFrame(
        list(recommendations.items()),
        columns=["Movie", "Score"]
    ).sort_values("Score", ascending=False).head(top_n)
    rec_df["Score"] = rec_df["Score"].round(2)

    print(f"\n🎬 Movies {target_user} would probably love:\n")
    print(rec_df.to_string(index=False))
    return rec_df

# ─────────────────────────────────────────────
# 5. TEST IT
# ─────────────────────────────────────────────
for user in ["User_1", "User_3", "User_7"]:
    collaborative_recommend(user)
    print()

print("=" * 55)
print("✅ Both recommenders are working! Check recommender.py")
print("   for Content-Based filtering too.")
print("=" * 55)
