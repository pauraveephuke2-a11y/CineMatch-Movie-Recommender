"""
data_generator.py
-----------------
Generates a sample movies dataset so we don't need to download anything.
Run this first! It creates movies.csv in the same folder.
"""

import pandas as pd
import numpy as np
import random

# ---- Sample movie data ----
movies_data = {
    "movie_id": list(range(1, 31)),
    "title": [
        "Inception", "The Dark Knight", "Interstellar", "The Matrix",
        "Avengers: Endgame", "Parasite", "3 Idiots", "Dangal",
        "PK", "Taare Zameen Par", "Baahubali", "KGF Chapter 2",
        "RRR", "Pushpa", "Jawan", "The Shawshank Redemption",
        "Forrest Gump", "The Godfather", "Pulp Fiction", "Fight Club",
        "Joker", "Spider-Man: No Way Home", "Doctor Strange",
        "Iron Man", "Black Panther", "Deadpool", "Thor: Ragnarok",
        "Coco", "Soul", "Up"
    ],
    "genre": [
        "Sci-Fi", "Action", "Sci-Fi", "Sci-Fi",
        "Action", "Thriller", "Comedy", "Sports",
        "Comedy", "Drama", "Action", "Action",
        "Action", "Action", "Action", "Drama",
        "Drama", "Crime", "Crime", "Thriller",
        "Thriller", "Action", "Sci-Fi",
        "Action", "Action", "Comedy", "Comedy",
        "Animation", "Animation", "Animation"
    ],
    "language": [
        "English", "English", "English", "English",
        "English", "Korean", "Hindi", "Hindi",
        "Hindi", "Hindi", "Telugu", "Kannada",
        "Telugu", "Telugu", "Hindi", "English",
        "English", "English", "English", "English",
        "English", "English", "English",
        "English", "English", "English", "English",
        "English", "English", "English"
    ],
    "rating": [
        8.8, 9.0, 8.6, 8.7,
        8.4, 8.5, 8.4, 8.4,
        8.1, 8.5, 8.0, 8.3,
        7.9, 7.5, 7.2, 9.3,
        8.8, 9.2, 8.9, 8.8,
        8.4, 8.3, 7.4,
        7.9, 7.3, 7.6, 7.9,
        8.4, 8.1, 8.2
    ],
    "votes": [
        2300000, 2800000, 2100000, 1900000,
        1200000, 800000, 450000, 380000,
        320000, 290000, 210000, 195000,
        185000, 150000, 130000, 2700000,
        2000000, 1900000, 2100000, 2000000,
        1400000, 950000, 780000,
        950000, 720000, 890000, 810000,
        480000, 420000, 560000
    ],
    "year": [
        2010, 2008, 2014, 1999,
        2019, 2019, 2009, 2016,
        2014, 2007, 2015, 2022,
        2022, 2021, 2023, 1994,
        1994, 1972, 1994, 1999,
        2019, 2021, 2022,
        2008, 2018, 2016, 2017,
        2017, 2020, 2009
    ]
}

# ---- Generate random user ratings (simulating 10 users) ----
np.random.seed(42)
random.seed(42)

users = [f"User_{i}" for i in range(1, 11)]
movie_ids = movies_data["movie_id"]

ratings_rows = []
for user in users:
    # Each user rates a random subset of movies
    rated_movies = random.sample(movie_ids, k=random.randint(10, 20))
    for mid in rated_movies:
        base = movies_data["rating"][mid - 1]
        user_rating = round(min(10, max(1, base + np.random.normal(0, 0.8))), 1)
        ratings_rows.append({"user": user, "movie_id": mid, "user_rating": user_rating})

# Save files
movies_df = pd.DataFrame(movies_data)
movies_df.to_csv("movies.csv", index=False)

ratings_df = pd.DataFrame(ratings_rows)
ratings_df.to_csv("user_ratings.csv", index=False)

print("[OK] movies.csv created with", len(movies_df), "movies")
print("[OK] user_ratings.csv created with", len(ratings_df), "ratings")
print("\nSample Movies:")
print(movies_df[["title", "genre", "rating"]].head(10).to_string(index=False))
