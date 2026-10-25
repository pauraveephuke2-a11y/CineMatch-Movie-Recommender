"""
CineMatch — Premium Mobile-First Movie Discovery & Recommendation App
"""

import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from streamlit_option_menu import option_menu

# ═════════════════════════════════════════════════════════════════
# CONFIG & VIEWPORT
# ═════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CineMatch 🎬 Discover What To Watch",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"  # Mobile friendly: collapsed by default on phones
)

# ═════════════════════════════════════════════════════════════════
# ULTRA-RESPONSIVE MOBILE FIRST CSS
# ═════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background & Global Colors */
    .stApp {
        background-color: #0b0b12;
        color: #f1f1f6;
    }

    /* Header & Navigation Fixes for Mobile */
    header[data-testid="stHeader"] {
        background-color: rgba(11, 11, 18, 0.85);
        backdrop-filter: blur(12px);
    }

    /* Hide standard Streamlit footer & menu clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Top Brand Bar */
    .mobile-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        background: linear-gradient(180deg, rgba(229, 9, 20, 0.15) 0%, rgba(11, 11, 18, 0) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        margin-bottom: 16px;
    }

    .brand-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 900;
        font-size: clamp(1.2rem, 4vw, 1.6rem);
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .brand-title span {
        color: #E50914;
    }

    /* WhatsApp Button - Mobile Optimized */
    .btn-whatsapp {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background-color: #25D366;
        color: #ffffff !important;
        font-weight: 700;
        font-size: clamp(0.8rem, 2.5vw, 0.95rem);
        padding: 10px 18px;
        border-radius: 9999px;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35);
        transition: all 0.2s ease-in-out;
        white-space: nowrap;
    }

    .btn-whatsapp:hover, .btn-whatsapp:active {
        background-color: #1eb956;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 211, 102, 0.5);
    }

    /* Trailer YouTube Button */
    .btn-trailer {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 8px;
        text-decoration: none !important;
        transition: all 0.2s;
    }

    .btn-trailer:hover {
        background: #E50914;
        border-color: #E50914;
        color: #ffffff !important;
    }

    /* Movie Card Layout */
    .movie-card-container {
        background: #141422;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 16px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    .movie-card-container:hover {
        transform: translateY(-3px);
        border-color: rgba(229, 9, 20, 0.5);
        box-shadow: 0 12px 28px rgba(229, 9, 20, 0.2);
    }

    .poster-wrapper {
        position: relative;
        width: 100%;
        padding-top: 145%; /* 2:3 aspect ratio */
        background-color: #1e1e30;
        overflow: hidden;
    }

    .poster-img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
    }

    .movie-card-container:hover .poster-img {
        transform: scale(1.04);
    }

    .rating-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(11, 11, 18, 0.85);
        backdrop-filter: blur(8px);
        color: #FFD700;
        font-weight: 800;
        font-size: 0.82rem;
        padding: 4px 8px;
        border-radius: 8px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }

    .card-body {
        padding: 14px 14px 16px;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 6px 0;
        line-height: 1.3;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .card-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 8px;
    }

    .chip {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.08);
        color: #d1d1e0;
    }

    .chip-accent {
        background: rgba(229, 9, 20, 0.2);
        color: #ff6b6b;
        border: 1px solid rgba(229, 9, 20, 0.3);
    }

    .card-overview {
        font-size: 0.8rem;
        color: #9e9ea7;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        margin-bottom: 12px;
    }

    /* Carousel Row for Phones */
    .horizontal-scroll-container {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding: 6px 2px 16px 2px;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
    }

    .horizontal-scroll-container::-webkit-scrollbar {
        height: 6px;
    }

    .horizontal-scroll-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 6px;
    }

    .carousel-item {
        flex: 0 0 clamp(160px, 42vw, 220px);
        scroll-snap-align: start;
    }

    /* Surprise Me Hero Banner */
    .surprise-hero {
        background: radial-gradient(circle at top right, rgba(229, 9, 20, 0.35), rgba(11, 11, 18, 0.95)), #141422;
        border: 1px solid rgba(229, 9, 20, 0.3);
        border-radius: 18px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .surprise-hero h2 {
        font-size: clamp(1.4rem, 4.5vw, 2rem);
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .surprise-hero p {
        font-size: clamp(0.85rem, 3vw, 1rem);
        color: #b5b5c3;
        margin-bottom: 18px;
    }

    /* Streamlit Button Overrides for Mobile Touch */
    .stButton > button {
        width: 100%;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        font-size: 0.95rem !important;
        min-height: 44px;
        touch-action: manipulation;
    }

    /* Primary Accent button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #E50914 0%, #b80610 100%) !important;
        box-shadow: 0 4px 14px rgba(229, 9, 20, 0.4) !important;
        border: none !important;
    }

    /* Responsive Adjustments for Mobile screens */
    @media screen and (max-width: 768px) {
        .stApp {
            padding-left: 0.2rem;
            padding-right: 0.2rem;
        }
        .surprise-hero {
            padding: 18px 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# DATA LAYER (CACHED)
# ═════════════════════════════════════════════════════════════════
@st.cache_data
def get_movie_dataset():
    df = pd.read_csv("movies.csv")
    ratings = pd.read_csv("user_ratings.csv")
    # Rich feature combination for TF-IDF: genre + language + mood + overview + stars
    df["features"] = (
        df["genre"] + " " +
        df["language"] + " " +
        df["mood"] + " " +
        df["stars"].fillna("") + " " +
        df["overview"].fillna("")
    )
    return df, ratings

@st.cache_data
def get_similarity_model(movies_df):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(movies_df["features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

movies_df, ratings_df = get_movie_dataset()
cosine_sim = get_similarity_model(movies_df)

# Session State for Watchlist & Ratings
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "user_ratings" not in st.session_state:
    st.session_state.user_ratings = {}

# ═════════════════════════════════════════════════════════════════
# DYNAMIC SHARE URL CONFIG
# ═════════════════════════════════════════════════════════════════
# Check query parameters for share link or fallback to app URL
# We will inject the active public tunnel URL so WhatsApp shares work out-of-the-box
SHARE_URL = "https://garbage-call-combo-apart.trycloudflare.com"
try:
    if "tunnel_url" in st.query_params:
        SHARE_URL = st.query_params["tunnel_url"]
except Exception:
    pass

wa_share_text = urllib.parse.quote(
    f"Hey! 🍿 Check out CineMatch — an awesome movie recommendation app:\n\n"
    f"👉 {SHARE_URL}\n\n"
    f"Find your next favorite film in seconds!"
)
wa_link = f"https://wa.me/?text={wa_share_text}"

# ═════════════════════════════════════════════════════════════════
# TOP APP BAR (MOBILE FRIENDLY)
# ═════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="mobile-nav-bar">
    <div class="brand-title">
        🍿 Cine<span>Match</span>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
        <a href="{wa_link}" target="_blank" class="btn-whatsapp">
            💬 Share with Friends
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# NAVIGATION BAR (MOBILE RESPONSIVE TABS)
# ═════════════════════════════════════════════════════════════════
selected_nav = option_menu(
    menu_title=None,
    options=["Discover", "Smart Match", "Surprise Me 🎲", "Movie Quiz ⚡", "My Watchlist"],
    icons=["compass", "magic", "dice-5", "lightning-charge", "bookmark-heart"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#141422",
            "border-radius": "12px",
            "margin-bottom": "18px",
            "border": "1px solid rgba(255,255,255,0.06)"
        },
        "icon": {"color": "#E50914", "font-size": "14px"},
        "nav-link": {
            "font-size": "13px",
            "font-weight": "600",
            "text-align": "center",
            "margin": "2px",
            "padding": "8px 12px",
            "border-radius": "8px",
            "color": "#a0a0b2",
        },
        "nav-link-selected": {
            "background-color": "#E50914",
            "color": "#ffffff",
            "font-weight": "700"
        },
    }
)

# ═════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════
def get_trailer_url(title):
    query = urllib.parse.quote(f"{title} official movie trailer")
    return f"https://www.youtube.com/results?search_query={query}"

def toggle_watchlist(title):
    if title in st.session_state.watchlist:
        st.session_state.watchlist.remove(title)
    else:
        st.session_state.watchlist.append(title)

def render_movie_card(movie, match_pct=None):
    title = movie["title"]
    genre = movie["genre"]
    rating = movie["rating"]
    year = int(movie["year"])
    runtime = movie.get("runtime", "2h")
    mood = movie.get("mood", "")
    overview = movie.get("overview", "")
    poster = movie.get("poster", "https://placehold.co/300x450/1a1a2e/e50914?text=Poster")
    trailer_url = get_trailer_url(title)
    is_saved = title in st.session_state.watchlist

    match_badge = ""
    if match_pct is not None:
        match_badge = f'<div class="chip chip-accent" style="margin-left:auto;">🔥 {int(match_pct)}% Match</div>'

    st.markdown(f"""
    <div class="movie-card-container">
        <div class="poster-wrapper">
            <img class="poster-img" src="{poster}" loading="lazy" alt="{title}" onerror="this.src='https://placehold.co/300x450/1a1a2e/e50914?text={urllib.parse.quote(title)}'" />
            <div class="rating-badge">★ {rating:.1f}</div>
        </div>
        <div class="card-body">
            <div class="card-title" title="{title}">{title}</div>
            <div class="card-meta">
                <span class="chip">{genre}</span>
                <span class="chip">{year}</span>
                <span class="chip">{runtime}</span>
                {match_badge}
            </div>
            <div class="card-overview">{overview}</div>
            <div style="display:flex; gap:8px; align-items:center; margin-top:8px;">
                <a class="btn-trailer" href="{trailer_url}" target="_blank" style="flex:1;">
                    ▶ Trailer
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bookmark action button below card
    btn_label = "❤️ Saved" if is_saved else "🤍 Add to Watchlist"
    if st.button(btn_label, key=f"wl_btn_{title}_{random.randint(1, 999999)}"):
        toggle_watchlist(title)
        st.rerun()

# ═════════════════════════════════════════════════════════════════
# TAB 1: DISCOVER
# ═════════════════════════════════════════════════════════════════
if selected_nav == "Discover":
    # Search bar & Quick Filters
    col_search, col_mood = st.columns([1.6, 1])
    with col_search:
        search_query = st.text_input("🔍 Search movies or actors...", placeholder="e.g. Inception, Dark Knight, Tom Hanks")
    with col_mood:
        selected_mood = st.selectbox(
            "🎭 Filter by Mood",
            ["All Moods", "Adrenaline 💥", "Mind-Bending 🧠", "Laugh Out Loud 😂", "Dark & Gritty 🦇", "Heartwarming 🥺", "Feel-Good ✨"]
        )

    # Genre pills
    genre_list = ["All"] + sorted(movies_df["genre"].unique().tolist())
    selected_genre = st.pills("Genre", genre_list, default="All") if hasattr(st, "pills") else st.selectbox("Genre", genre_list)

    # Filter dataset
    filtered = movies_df.copy()
    if search_query:
        matches = process.extract(search_query, movies_df["title"].tolist(), limit=12)
        matched_titles = [m[0] for m in matches if m[1] > 50]
        # Also search stars and overview
        stars_matches = movies_df[movies_df["stars"].str.contains(search_query, case=False, na=False)]["title"].tolist()
        filtered = filtered[filtered["title"].isin(set(matched_titles + stars_matches))]

    if selected_mood != "All Moods":
        filtered = filtered[filtered["mood"] == selected_mood]

    if selected_genre != "All":
        filtered = filtered[filtered["genre"] == selected_genre]

    # Trending Carousel Row (Horizontal Scroll on Mobile)
    if not search_query and selected_mood == "All Moods" and selected_genre == "All":
        st.markdown("### 🔥 Trending Hits")
        top_trending = movies_df.nlargest(6, "votes")
        
        # Grid layout that responds nicely across phones and laptops
        cols = st.columns(3)
        for idx, (_, m) in enumerate(top_trending.iterrows()):
            with cols[idx % 3]:
                render_movie_card(m)

        st.markdown("---")
        st.markdown("### 🍿 Full Catalog")

    # Render catalog in a clean 2 to 3 column grid for mobile/tablet/desktop
    if filtered.empty:
        st.info("No movies found matching your filters. Try a different search!")
    else:
        grid_cols = st.columns(3)
        for idx, (_, movie) in enumerate(filtered.iterrows()):
            with grid_cols[idx % 3]:
                render_movie_card(movie)

# ═════════════════════════════════════════════════════════════════
# TAB 2: SMART MATCH (CONTENT-BASED & AI RECOMMENDATION)
# ═════════════════════════════════════════════════════════════════
elif selected_nav == "Smart Match":
    st.markdown("""
    <div style="background:#141422; border-radius:14px; padding:18px; border:1px solid rgba(229,9,20,0.2); margin-bottom:18px;">
        <h3 style="margin:0 0 6px 0; color:#fff;">🤖 AI Smart Match</h3>
        <p style="margin:0; color:#a0a0b2; font-size:0.9rem;">
            Pick a movie you love, and our algorithm will analyze the storyline, mood, theme, and genre to find your perfect matches.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        chosen_movie = st.selectbox("🎬 Select a movie you enjoyed:", sorted(movies_df["title"].tolist()))
    with col2:
        num_recs = st.slider("Number of recommendations", 2, 8, 4)

    if st.button("✨ Generate My Recommendations", type="primary"):
        target_idx = movies_df[movies_df["title"] == chosen_movie].index[0]
        sim_scores = list(enumerate(cosine_sim[target_idx]))
        # Sort desc, skip the movie itself
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]

        st.markdown(f"#### 🎯 Because you enjoyed **{chosen_movie}**:")
        rec_cols = st.columns(2)
        for i, (idx, score) in enumerate(sim_scores):
            rec_movie = movies_df.iloc[idx]
            match_percentage = score * 100
            with rec_cols[i % 2]:
                render_movie_card(rec_movie, match_pct=match_percentage)

# ═════════════════════════════════════════════════════════════════
# TAB 3: SURPRISE ME (ROULETTE / RANDOM PICKER)
# ═════════════════════════════════════════════════════════════════
elif selected_nav == "Surprise Me 🎲":
    st.markdown("""
    <div class="surprise-hero">
        <h2>🎲 Movie Roulette</h2>
        <p>Can't decide what to watch? Spin the wheel and let CineMatch pick your next movie night adventure!</p>
    </div>
    """, unsafe_allow_html=True)

    col_btn, col_pref = st.columns([1.5, 1])
    with col_pref:
        vibe = st.selectbox("Preferred Vibe", ["Any Vibe 🌟", "Adrenaline 💥", "Mind-Bending 🧠", "Laugh Out Loud 😂", "Dark & Gritty 🦇", "Feel-Good ✨"])
    with col_btn:
        st.write("")
        spin_clicked = st.button("🎰 Spin & Pick a Movie!", type="primary")

    if spin_clicked:
        st.balloons()
        pool = movies_df.copy()
        if vibe != "Any Vibe 🌟":
            pool = pool[pool["mood"] == vibe]
            if pool.empty:
                pool = movies_df.copy()

        picked = pool.sample(1).iloc[0]
        st.markdown("### 🏆 Your Movie For Tonight:")
        c1, c2 = st.columns([1, 1.2])
        with c1:
            render_movie_card(picked)
        with c2:
            st.markdown(f"""
            <div style="background:#141422; border-radius:16px; padding:20px; border:1px solid rgba(255,255,255,0.08);">
                <h3 style="color:#FFD700; margin-top:0;">🌟 Why You'll Love It:</h3>
                <p style="font-size:0.95rem; line-height:1.6; color:#d1d1e0;">
                    <strong>{picked['title']}</strong> boasts an impressive <strong>{picked['rating']}/10</strong> rating from over {int(picked['votes']/1000):,}k film lovers. 
                    Starring <em>{picked['stars']}</em>, it delivers the ultimate <strong>{picked['mood']}</strong> experience.
                </p>
                <div style="margin-top:16px;">
                    <a href="{get_trailer_url(picked['title'])}" target="_blank" class="btn-trailer" style="background:#E50914; border:none; padding:10px 18px; font-size:0.9rem;">
                        ▶ Watch Official Trailer on YouTube
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# TAB 4: 3-QUESTION MOVIE QUIZ
# ═════════════════════════════════════════════════════════════════
elif selected_nav == "Movie Quiz ⚡":
    st.markdown("""
    <div style="background:#141422; border-radius:14px; padding:18px; border:1px solid rgba(255,255,255,0.08); margin-bottom:18px;">
        <h3 style="margin:0 0 6px 0; color:#fff;">⚡ 30-Second Movie Quiz</h3>
        <p style="margin:0; color:#a0a0b2; font-size:0.9rem;">
            Answer 3 quick questions and get an instant custom recommendation tailored to your mood right now.
        </p>
    </div>
    """, unsafe_allow_html=True)

    q1 = st.radio("1️⃣ What is your ideal weekend vibe tonight?", [
        "Mind-Blowing & Cerebral 🧠",
        "High Octane Action & Adrenaline 💥",
        "Tears & Deep Emotion 🥺",
        "Pure Comedy & Good Times 😂"
    ])

    q2 = st.radio("2️⃣ Who are you watching with?", [
        "Solo Night In 🛋️",
        "Friends or Family 👨‍👩‍👧‍👦",
        "Movie Date Night 🍷"
    ])

    q3 = st.radio("3️⃣ Runtime preference?", [
        "Keep it quick (< 2 hours) ⚡",
        "I'm ready for an epic (2.5+ hours) 🎬",
        "Doesn't matter as long as it's great! 🍿"
    ])

    if st.button("🔮 Calculate My Match", type="primary"):
        # Map answers to filters
        filtered_quiz = movies_df.copy()
        if "Mind-Blowing" in q1:
            filtered_quiz = filtered_quiz[filtered_quiz["mood"] == "Mind-Bending 🧠"]
        elif "Action" in q1:
            filtered_quiz = filtered_quiz[filtered_quiz["genre"] == "Action"]
        elif "Comedy" in q1:
            filtered_quiz = filtered_quiz[filtered_quiz["genre"] == "Comedy"]
        elif "Emotion" in q1:
            filtered_quiz = filtered_quiz[filtered_quiz["mood"].isin(["Heartwarming 🥺", "Feel-Good ✨"])]

        if filtered_quiz.empty:
            filtered_quiz = movies_df.nlargest(5, "rating")

        match = filtered_quiz.nlargest(1, "rating").iloc[0]
        st.success("🎉 We found your perfect movie match!")
        c_quiz1, c_quiz2 = st.columns([1, 1.2])
        with c_quiz1:
            render_movie_card(match, match_pct=98)
        with c_quiz2:
            st.markdown(f"""
            <div style="background:#141422; border-radius:14px; padding:18px;">
                <h4 style="color:#fff; margin-top:0;">Why this matches your answers:</h4>
                <p style="color:#b5b5c3; font-size:0.9rem;">
                    Matches your preference for <strong>{q1.split(' ')[0]}</strong> cinema with a stellar IMDb score of <strong>{match['rating']}</strong>.
                </p>
                <a href="{get_trailer_url(match['title'])}" target="_blank" class="btn-whatsapp" style="background:#E50914;">
                    ▶ Play Trailer Now
                </a>
            </div>
            """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# TAB 5: MY WATCHLIST
# ═════════════════════════════════════════════════════════════════
elif selected_nav == "My Watchlist":
    st.markdown("### 🔖 My Saved Watchlist")

    if not st.session_state.watchlist:
        st.info("Your watchlist is empty! Browse the 'Discover' tab and click '🤍 Add to Watchlist' on any film.")
    else:
        st.write(f"You have **{len(st.session_state.watchlist)}** movies saved.")

        # WhatsApp share of watchlist
        saved_titles_str = ", ".join(st.session_state.watchlist)
        wl_share_msg = urllib.parse.quote(
            f"Here is my CineMatch Watchlist 🎬:\n{saved_titles_str}\n\nCheck out the app: {SHARE_URL}"
        )
        st.markdown(f"""
        <div style="margin-bottom:16px;">
            <a href="https://wa.me/?text={wl_share_msg}" target="_blank" class="btn-whatsapp">
                💬 Share My Watchlist on WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        saved_df = movies_df[movies_df["title"].isin(st.session_state.watchlist)]
        for idx, (_, m) in enumerate(saved_df.iterrows()):
            with cols[idx % 3]:
                render_movie_card(m)

        if st.button("🗑️ Clear Entire Watchlist"):
            st.session_state.watchlist = []
            st.rerun()
