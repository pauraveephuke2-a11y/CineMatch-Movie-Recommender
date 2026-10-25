"""
recommender.py
--------------
Step 2: Build a Movie Recommendation System
        Uses Content-Based Filtering (Genre + Rating similarity)

Concepts covered:
  - TF-IDF Vectorizer (converts text → numbers)
  - Cosine Similarity (measures how similar two movies are)
  - pandas merge & filtering
  - Simple recommendation function
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
movies = pd.read_csv("movies.csv")

print("=" * 55)
print("🎬  MOVIE RECOMMENDATION SYSTEM  🎬")
print("=" * 55)

# ─────────────────────────────────────────────
# 2. FEATURE ENGINEERING
# ─────────────────────────────────────────────
# Combine genre + language into a single "tags" column
# This is what makes movies similar to each other!
movies["tags"] = movies["genre"] + " " + movies["language"]

print("\n📌 Sample tags created:")
print(movies[["title", "genre", "language", "tags"]].head(8).to_string(index=False))

# ─────────────────────────────────────────────
# 3. TF-IDF VECTORIZATION
# ─────────────────────────────────────────────
# TF-IDF converts text tags into numerical vectors
# Each movie becomes a vector of numbers
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies["tags"])

print(f"\n🔢 TF-IDF Matrix Shape: {tfidf_matrix.shape}")
print("   (Each row = 1 movie, Each column = 1 unique word)")

# ─────────────────────────────────────────────
# 4. COSINE SIMILARITY
# ─────────────────────────────────────────────
# Measures angle between two movie vectors
# Score closer to 1.0 = More similar!
similarity_matrix = cosine_similarity(tfidf_matrix)
print(f"\n📐 Similarity Matrix Shape: {similarity_matrix.shape}")
print("   (30×30 table: similarity score between every pair of movies)")

# ─────────────────────────────────────────────
# 5. RECOMMENDATION FUNCTION
# ─────────────────────────────────────────────
def recommend_movies(movie_title, top_n=5):
    """
    Given a movie title, return top N similar movies.
    """
    # Find the movie's index in our DataFrame
    movie_title = movie_title.strip()
    matches = movies[movies["title"].str.lower() == movie_title.lower()]
    
    if matches.empty:
        print(f"\n❌ Movie '{movie_title}' not found!")
        print("   Available movies:", list(movies["title"]))
        return
    
    movie_idx = matches.index[0]
    
    # Get similarity scores for this movie vs all others
    similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
    
    # Sort by similarity score (descending), skip the movie itself (idx 0)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:top_n + 1]  # skip index 0 (itself)
    
    # Get movie details
    recommended_indices = [i[0] for i in similarity_scores]
    recommended_scores  = [round(i[1], 3) for i in similarity_scores]
    
    result = movies.iloc[recommended_indices][["title", "genre", "language", "rating"]].copy()
    result["similarity"] = recommended_scores
    
    print(f"\n🎯 Because you liked: '{movies.iloc[movie_idx]['title']}'")
    print(f"   Genre: {movies.iloc[movie_idx]['genre']} | Rating: {movies.iloc[movie_idx]['rating']}")
    print(f"\n✨ Top {top_n} Recommendations:\n")
    print(result.to_string(index=False))
    print()
    return result

# ─────────────────────────────────────────────
# 6. TRY IT OUT!
# ─────────────────────────────────────────────
recommend_movies("Inception")
recommend_movies("3 Idiots")
recommend_movies("Avengers: Endgame")
recommend_movies("Coco")

# ─────────────────────────────────────────────
# 7. INTERACTIVE MODE
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("🕹️  INTERACTIVE MODE — Enter a movie to get recs!")
print("=" * 55)
print("Available movies:", list(movies["title"]))

while True:
    user_input = input("\n🎬 Enter a movie name (or 'quit' to exit): ").strip()
    if user_input.lower() in ["quit", "exit", "q"]:
        print("👋 Goodbye!")
        break
    recommend_movies(user_input)
