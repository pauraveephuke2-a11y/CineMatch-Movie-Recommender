# 🎬 Movie Recommendation System
### A Beginner-Friendly AI & Data Science Project

---

## 📁 Project Structure
```
MovieRecommender/
│
├── data_generator.py         ← Step 0: Creates the dataset
├── explore_data.py           ← Step 1: Explore & visualize data
├── recommender.py            ← Step 2: Content-Based Filtering
├── collaborative_filter.py   ← Step 3: Collaborative Filtering
├── visualize_similarity.py   ← Step 4: Heatmaps & PCA plots
└── README.md                 ← This file!
```

---

## 🚀 How to Run (Step by Step)

```bash
# Step 0 — Generate the dataset
python data_generator.py

# Step 1 — Explore the data
python explore_data.py

# Step 2 — Content-based recommendations
python recommender.py

# Step 3 — Collaborative filtering
python collaborative_filter.py

# Step 4 — Visualize similarity
python visualize_similarity.py
```

---

## 🧠 What You Will Learn

| Concept | File | Library |
|---------|------|---------|
| DataFrames, CSV loading | All files | `pandas` |
| Descriptive statistics | `explore_data.py` | `pandas` |
| Bar, scatter, histogram plots | `explore_data.py` | `matplotlib`, `seaborn` |
| TF-IDF Vectorization | `recommender.py` | `sklearn` |
| Cosine Similarity | `recommender.py` | `sklearn` |
| Pivot Tables | `collaborative_filter.py` | `pandas` |
| User-User Similarity | `collaborative_filter.py` | `sklearn` |
| Heatmaps | `visualize_similarity.py` | `seaborn` |
| PCA (Dimensionality Reduction) | `visualize_similarity.py` | `sklearn` |

---

## 💡 Two Types of Recommendation Systems

### 1. Content-Based Filtering
> "If you liked Movie A, here are movies **similar to A**"
- Looks at movie features (genre, language)
- Uses TF-IDF + Cosine Similarity
- Does NOT need other users' data

### 2. Collaborative Filtering
> "Users who liked Movie A also liked Movie B"
- Looks at what **similar users** rated highly
- Uses User-Movie matrix + Cosine Similarity
- Requires user ratings data

---

## 📈 Output Files Generated

| File | Description |
|------|-------------|
| `movies.csv` | 30 popular movies with ratings |
| `user_ratings.csv` | Simulated ratings from 10 users |
| `exploration.png` | 4-panel EDA dashboard |
| `similarity_heatmap.png` | Movie-to-movie similarity heatmap |
| `pca_clusters.png` | Movies plotted in 2D space by genre |
| `top_similar.png` | Bar chart of most similar movies |

---

## 🎯 Challenge: Extend the Project!

- [ ] Add more movies to `data_generator.py`
- [ ] Add a `description` column and use it in TF-IDF
- [ ] Build a **Streamlit web app** as the front-end
- [ ] Connect to the **TMDB API** for real movie data
- [ ] Add a **rating predictor** using Linear Regression
