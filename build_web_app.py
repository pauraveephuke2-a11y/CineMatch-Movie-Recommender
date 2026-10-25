"""
build_web_app.py
Builds the standalone, zero-dependency, permanent web application (index.html)
for GitHub Pages deployment at:
https://pauraveephuke2-a11y.github.io/CineMatch-Movie-Recommender/
"""

import pandas as pd
import json
import os

df = pd.read_csv(r"C:\Users\Nucom\Projects\MovieRecommender\movies.csv")
movies_json = json.dumps(df.to_dict(orient="records"), ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CineMatch — AI Movie Discovery & Recommendations</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <!-- Confetti Library for Roulette -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --bg-main: #0B0B14;
            --bg-card: #141424;
            --bg-card-hover: #1A1A2E;
            --accent-red: #E50914;
            --accent-red-hover: #b80710;
            --text-main: #FFFFFF;
            --text-muted: #9E9EA7;
            --gold: #FFD700;
            --green: #25D366;
            --border: rgba(255, 255, 255, 0.08);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            padding-bottom: 60px;
            overflow-x: hidden;
        }}

        /* Header / App Bar */
        .app-bar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(11, 11, 20, 0.92);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border);
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .brand span {{ color: var(--accent-red); }}

        .wa-share-btn {{
            background-color: var(--green);
            color: #fff;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
            transition: transform 0.2s;
        }}

        .wa-share-btn:active {{ transform: scale(0.96); }}

        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            gap: 8px;
            padding: 12px 16px;
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: none;
            background: #10101C;
            border-bottom: 1px solid var(--border);
        }}

        .nav-tabs::-webkit-scrollbar {{ display: none; }}

        .tab-btn {{
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .tab-btn.active {{
            background: var(--accent-red);
            color: #fff;
            border-color: var(--accent-red);
            font-weight: 700;
            box-shadow: 0 4px 14px rgba(229, 9, 20, 0.35);
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px 16px;
        }}

        /* Hero */
        .hero {{
            background: radial-gradient(circle at top right, rgba(229, 9, 20, 0.3), rgba(11, 11, 20, 0.98)), var(--bg-card);
            border: 1px solid rgba(229, 9, 20, 0.25);
            border-radius: 18px;
            padding: 24px 20px;
            text-align: center;
            margin-bottom: 24px;
        }}

        .hero h1 {{
            font-size: clamp(1.5rem, 5vw, 2.2rem);
            font-weight: 900;
            margin-bottom: 8px;
        }}

        .hero p {{
            color: var(--text-muted);
            font-size: 0.9rem;
            max-width: 600px;
            margin: 0 auto 16px;
        }}

        /* Search & Filters */
        .search-box {{
            width: 100%;
            padding: 12px 18px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--bg-card);
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            margin-bottom: 14px;
            transition: border-color 0.2s;
        }}

        .search-box:focus {{ border-color: var(--accent-red); }}

        .filter-row {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}

        .filter-select {{
            background: var(--bg-card);
            color: #fff;
            border: 1px solid var(--border);
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            outline: none;
            cursor: pointer;
            flex: 1;
            min-width: 140px;
        }}

        /* Movie Grid */
        .movie-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 18px;
        }}

        @media (max-width: 600px) {{
            .movie-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }}
        }}

        /* Movie Card */
        .movie-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .movie-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(229, 9, 20, 0.4);
        }}

        .poster-container {{
            position: relative;
            width: 100%;
            padding-top: 145%;
            background: #1a1a2e;
            overflow: hidden;
        }}

        .poster-container img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .badge-rating {{
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(11, 11, 20, 0.88);
            backdrop-filter: blur(6px);
            color: var(--gold);
            font-size: 0.78rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}

        .card-info {{
            padding: 12px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .card-title {{
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .card-tags {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}

        .tag {{
            font-size: 0.68rem;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.08);
            color: #d1d1e0;
        }}

        .tag-match {{
            background: rgba(229, 9, 20, 0.2);
            color: #ff6b6b;
            border: 1px solid rgba(229, 9, 20, 0.3);
        }}

        .card-plot {{
            font-size: 0.76rem;
            color: var(--text-muted);
            line-height: 1.35;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-bottom: 10px;
        }}

        .card-actions {{
            margin-top: auto;
            display: flex;
            gap: 6px;
        }}

        .btn-action {{
            flex: 1;
            padding: 8px 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            text-decoration: none;
            border: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            transition: all 0.2s;
        }}

        .btn-trailer {{
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            border: 1px solid var(--border);
        }}

        .btn-trailer:hover {{
            background: var(--accent-red);
            border-color: var(--accent-red);
        }}

        .btn-bookmark {{
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            border: 1px solid var(--border);
        }}

        .btn-bookmark.saved {{
            background: rgba(229, 9, 20, 0.3);
            color: #ff4d4d;
            border-color: var(--accent-red);
        }}

        /* Interactive Sections */
        .section-panel {{
            display: none;
        }}

        .section-panel.active {{
            display: block;
        }}

        /* Custom Roulette Box */
        .roulette-box {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            max-width: 500px;
            margin: 0 auto;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-red) 0%, var(--accent-red-hover) 100%);
            color: #fff;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 800;
            border: none;
            cursor: pointer;
            width: 100%;
            box-shadow: 0 4px 16px rgba(229, 9, 20, 0.4);
            margin-top: 14px;
            transition: transform 0.2s;
        }}

        .btn-primary:active {{ transform: scale(0.98); }}

        /* Quiz Radio Group */
        .quiz-group {{
            margin-bottom: 20px;
            text-align: left;
        }}

        .quiz-label {{
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 10px;
            display: block;
        }}

        .quiz-option {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 14px;
            margin-bottom: 8px;
            cursor: pointer;
            font-size: 0.88rem;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
        }}

        .quiz-option:hover, .quiz-option.selected {{
            border-color: var(--accent-red);
            background: rgba(229, 9, 20, 0.15);
        }}

        /* Document download badges */
        .doc-bar {{
            background: #10101C;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 30px;
        }}

        .doc-link {{
            color: #38bdf8;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
        }}
    </style>
</head>
<body>

    <!-- App Top Bar -->
    <header class="app-bar">
        <div class="brand">
            🍿 Cine<span>Match</span>
        </div>
        <a id="waHeaderBtn" href="#" target="_blank" class="wa-share-btn">
            💬 Share on WhatsApp
        </a>
    </header>

    <!-- Navigation Tabs -->
    <nav class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('discover')">🧭 Discover</button>
        <button class="tab-btn" onclick="switchTab('smartmatch')">🤖 AI Smart Match</button>
        <button class="tab-btn" onclick="switchTab('roulette')">🎲 Roulette</button>
        <button class="tab-btn" onclick="switchTab('quiz')">⚡ 30s Quiz</button>
        <button class="tab-btn" onclick="switchTab('watchlist')">🔖 Watchlist (<span id="wlCount">0</span>)</button>
    </nav>

    <div class="container">

        <!-- 1. DISCOVER TAB -->
        <section id="tab-discover" class="section-panel active">
            <div class="hero">
                <h1>Find Your Next Great Film</h1>
                <p>AI-Powered Movie Discovery & Recommendation Web App</p>
            </div>

            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Search by title, actor, or keyword..." oninput="filterCatalog()">

            <div class="filter-row">
                <select id="genreSelect" class="filter-select" onchange="filterCatalog()">
                    <option value="All">All Genres</option>
                </select>
                <select id="moodSelect" class="filter-select" onchange="filterCatalog()">
                    <option value="All">All Moods</option>
                </select>
                <select id="sortSelect" class="filter-select" onchange="filterCatalog()">
                    <option value="rating">Sort: Highest Rated</option>
                    <option value="votes">Sort: Most Popular</option>
                    <option value="year">Sort: Newest First</option>
                </select>
            </div>

            <div id="catalogGrid" class="movie-grid"></div>
        </section>

        <!-- 2. SMART MATCH TAB -->
        <section id="tab-smartmatch" class="section-panel">
            <div class="hero">
                <h1>🤖 AI Smart Match</h1>
                <p>Select a film you love. Our NLP vector space algorithm computes cosine similarity angles to find thematically aligned recommendations.</p>
            </div>

            <div style="max-width: 500px; margin: 0 auto 24px;">
                <label style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 6px; display: block;">Pick a movie you enjoyed:</label>
                <select id="smartMatchSelect" class="filter-select" style="width: 100%;"></select>
                <button class="btn-primary" onclick="computeSmartRecommendations()">✨ Compute Recommendations</button>
            </div>

            <div id="smartMatchResults" class="movie-grid"></div>
        </section>

        <!-- 3. ROULETTE TAB -->
        <section id="tab-roulette" class="section-panel">
            <div class="hero">
                <h1>🎲 Movie Roulette</h1>
                <p>Can't decide? Pick your mood and spin the wheel for an instant cinematic pick!</p>
            </div>

            <div class="roulette-box">
                <label style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 6px; display: block;">Preferred Vibe:</label>
                <select id="rouletteMood" class="filter-select" style="width: 100%; margin-bottom: 12px;">
                    <option value="All">Any Vibe 🌟</option>
                </select>
                <button class="btn-primary" onclick="spinRoulette()">🎰 Spin the Wheel!</button>
                <div id="rouletteResult" style="margin-top: 20px;"></div>
            </div>
        </section>

        <!-- 4. QUIZ TAB -->
        <section id="tab-quiz" class="section-panel">
            <div class="hero">
                <h1>⚡ 30-Second Movie Quiz</h1>
                <p>Answer 3 quick questions to calculate your personalized movie recommendation right now.</p>
            </div>

            <div class="roulette-box" style="max-width: 600px; text-align: left;">
                <div class="quiz-group">
                    <span class="quiz-label">1. What's the vibe tonight?</span>
                    <div class="quiz-option" onclick="selectOption(this, 'q1', 'Sci-Fi')">🧠 Mind-Blowing & Cerebral</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q1', 'Action')">💥 High Octane & Adrenaline</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q1', 'Comedy')">😂 Laugh Out Loud Comedy</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q1', 'Drama')">🥺 Emotional & Thoughtful</div>
                </div>

                <div class="quiz-group">
                    <span class="quiz-label">2. Who are you watching with?</span>
                    <div class="quiz-option" onclick="selectOption(this, 'q2', 'solo')">🛋️ Solo Night In</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q2', 'friends')">👨‍👩‍👧‍👦 Friends or Family</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q2', 'date')">🍷 Date Night</div>
                </div>

                <div class="quiz-group">
                    <span class="quiz-label">3. Target duration?</span>
                    <div class="quiz-option" onclick="selectOption(this, 'q3', 'quick')">⚡ Keep it quick (&lt; 2 hrs)</div>
                    <div class="quiz-option" onclick="selectOption(this, 'q3', 'epic')">🎬 Ready for an epic (2.5+ hrs)</div>
                </div>

                <button class="btn-primary" onclick="solveQuiz()">🔮 Calculate My Match</button>
                <div id="quizResult" style="margin-top: 20px;"></div>
            </div>
        </section>

        <!-- 5. WATCHLIST TAB -->
        <section id="tab-watchlist" class="section-panel">
            <div class="hero">
                <h1>🔖 My Watchlist</h1>
                <p>Your saved titles are persisted in your device browser storage.</p>
            </div>

            <div style="text-align: center; margin-bottom: 20px;">
                <button class="btn-primary" style="max-width: 280px; background: var(--green);" onclick="shareWatchlist()">💬 Share Watchlist on WhatsApp</button>
            </div>

            <div id="watchlistGrid" class="movie-grid"></div>
        </section>

        <!-- Academic Report & Project Footer -->
        <div class="doc-bar">
            <div>
                <strong style="font-size: 0.85rem; color: #fff;">🎓 MIT-WPU Academic Mini-Project</strong>
                <p style="font-size: 0.75rem; color: var(--text-muted);">Pauravee Phuke | B.Tech AI &amp; DS (Div 9, Batch I2)</p>
            </div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <a class="doc-link" href="CineMatch_Project_Report_MIT_WPU.pdf" target="_blank">📄 Project Report (PDF)</a>
                <a class="doc-link" href="CineMatch_Project_Flowchart.png" target="_blank">📊 Architecture Flowchart</a>
                <a class="doc-link" href="https://github.com/pauraveephuke2-a11y/CineMatch-Movie-Recommender" target="_blank">🐙 GitHub Source</a>
            </div>
        </div>

    </div>

    <!-- JavaScript Recommender & UI Engine -->
    <script>
        const movies = {movies_json};
        let watchlist = JSON.parse(localStorage.getItem('cinematch_wl') || '[]');
        let quizAnswers = {{ q1: 'Sci-Fi', q2: 'solo', q3: 'quick' }};

        // WhatsApp Share Link
        const appUrl = window.location.href;
        const waMsg = encodeURIComponent("Hey! 🍿 Check out CineMatch - an AI Movie Recommender web app:\\n\\n" + appUrl + "\\n\\nFind what to watch in seconds!");
        document.getElementById('waHeaderBtn').href = "https://wa.me/?text=" + waMsg;

        // Init Watchlist count
        function updateWlCount() {{
            document.getElementById('wlCount').textContent = watchlist.length;
            localStorage.setItem('cinematch_wl', JSON.stringify(watchlist));
        }}
        updateWlCount();

        // Populate Selects
        const genres = ['All', ...new Set(movies.map(m => m.genre))];
        const moods = ['All', ...new Set(movies.map(m => m.mood).filter(Boolean))];

        const genreSelect = document.getElementById('genreSelect');
        genres.forEach(g => {{
            const opt = document.createElement('option');
            opt.value = g;
            opt.textContent = g === 'All' ? 'All Genres' : g;
            genreSelect.appendChild(opt);
        }});

        const moodSelect = document.getElementById('moodSelect');
        const rouletteMood = document.getElementById('rouletteMood');
        moods.forEach(m => {{
            const opt1 = document.createElement('option');
            opt1.value = m;
            opt1.textContent = m === 'All' ? 'All Moods' : m;
            moodSelect.appendChild(opt1);

            const opt2 = document.createElement('option');
            opt2.value = m;
            opt2.textContent = m === 'All' ? 'Any Vibe 🌟' : m;
            rouletteMood.appendChild(opt2);
        }});

        const smartMatchSelect = document.getElementById('smartMatchSelect');
        movies.slice().sort((a,b) => a.title.localeCompare(b.title)).forEach(m => {{
            const opt = document.createElement('option');
            opt.value = m.title;
            opt.textContent = m.title + " (" + m.genre + " - " + m.year + ")";
            smartMatchSelect.appendChild(opt);
        }});

        // Render Movie Cards
        function renderCard(m, matchPct = null) {{
            const isSaved = watchlist.includes(m.title);
            const trailerUrl = "https://www.youtube.com/results?search_query=" + encodeURIComponent(m.title + " official trailer");
            const matchTag = matchPct ? `<span class="tag tag-match">🔥 ${{Math.round(matchPct)}}% Match</span>` : '';

            return `
                <div class="movie-card">
                    <div class="poster-container">
                        <img src="${{m.poster}}" alt="${{m.title}}" loading="lazy" onerror="this.src='https://placehold.co/300x450/141424/E50914?text=' + encodeURIComponent('${{m.title}}')">
                        <div class="badge-rating">★ ${{m.rating.toFixed(1)}}</div>
                    </div>
                    <div class="card-info">
                        <div class="card-title" title="${{m.title}}">${{m.title}}</div>
                        <div class="card-tags">
                            <span class="tag">${{m.genre}}</span>
                            <span class="tag">${{m.year}}</span>
                            <span class="tag">${{m.runtime}}</span>
                            ${{matchTag}}
                        </div>
                        <div class="card-plot">${{m.overview || ''}}</div>
                        <div class="card-actions">
                            <a class="btn-action btn-trailer" href="${{trailerUrl}}" target="_blank">▶ Trailer</a>
                            <button class="btn-action btn-bookmark ${{isSaved ? 'saved' : ''}}" onclick="toggleWatchlist('${{m.title.replace(/'/g, "\\\\'")}}')">
                                ${{isSaved ? '❤️ Saved' : '🤍 Save'}}
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }}

        // Filter Catalog
        function filterCatalog() {{
            const q = document.getElementById('searchInput').value.toLowerCase().trim();
            const genre = document.getElementById('genreSelect').value;
            const mood = document.getElementById('moodSelect').value;
            const sort = document.getElementById('sortSelect').value;

            let filtered = movies.filter(m => {{
                const matchQ = !q || m.title.toLowerCase().includes(q) || (m.stars && m.stars.toLowerCase().includes(q)) || (m.overview && m.overview.toLowerCase().includes(q));
                const matchG = genre === 'All' || m.genre === genre;
                const matchM = mood === 'All' || m.mood === mood;
                return matchQ && matchG && matchM;
            }});

            if (sort === 'rating') filtered.sort((a,b) => b.rating - a.rating);
            else if (sort === 'votes') filtered.sort((a,b) => b.votes - a.votes);
            else if (sort === 'year') filtered.sort((a,b) => b.year - a.year);

            const grid = document.getElementById('catalogGrid');
            if (filtered.length === 0) {{
                grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px 0;">No movies found matching your criteria.</p>';
            }} else {{
                grid.innerHTML = filtered.map(m => renderCard(m)).join('');
            }}
        }}
        filterCatalog();

        // Watchlist Toggle
        function toggleWatchlist(title) {{
            const idx = watchlist.indexOf(title);
            if (idx > -1) watchlist.splice(idx, 1);
            else watchlist.push(title);
            updateWlCount();
            filterCatalog();
            renderWatchlist();
        }}

        function renderWatchlist() {{
            const grid = document.getElementById('watchlistGrid');
            const saved = movies.filter(m => watchlist.includes(m.title));
            if (saved.length === 0) {{
                grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px 0;">Your watchlist is currently empty. Tap 🤍 Save on any film to bookmark it!</p>';
            }} else {{
                grid.innerHTML = saved.map(m => renderCard(m)).join('');
            }}
        }}

        function shareWatchlist() {{
            if (watchlist.length === 0) return alert("Your watchlist is empty!");
            const text = encodeURIComponent("Here is my CineMatch Watchlist 🎬:\\n- " + watchlist.join("\\n- ") + "\\n\\nDiscovered on: " + window.location.href);
            window.open("https://wa.me/?text=" + text, "_blank");
        }}

        // Switch Tabs
        function switchTab(tabId) {{
            document.querySelectorAll('.section-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
            if (tabId === 'watchlist') renderWatchlist();
        }}

        // Client-side NLP Vector & Cosine Similarity Engine
        function tokenize(text) {{
            return text.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\\s+/).filter(w => w.length > 2);
        }}

        function getMovieVector(movie) {{
            const text = [movie.genre, movie.genre, movie.language, movie.mood, movie.stars, movie.overview].join(' ');
            const tokens = tokenize(text);
            const freq = {{}};
            tokens.forEach(t => freq[t] = (freq[t] || 0) + 1);
            return freq;
        }}

        function cosineSimilarity(vecA, vecB) {{
            let dot = 0, normA = 0, normB = 0;
            for (let k in vecA) normA += vecA[k] * vecA[k];
            for (let k in vecB) normB += vecB[k] * vecB[k];
            for (let k in vecA) {{
                if (vecB[k]) dot += vecA[k] * vecB[k];
            }}
            if (!normA || !normB) return 0;
            return dot / (Math.sqrt(normA) * Math.sqrt(normB));
        }}

        function computeSmartRecommendations() {{
            const chosenTitle = document.getElementById('smartMatchSelect').value;
            const target = movies.find(m => m.title === chosenTitle);
            const targetVec = getMovieVector(target);

            const scores = movies
                .filter(m => m.title !== chosenTitle)
                .map(m => ({{
                    movie: m,
                    sim: cosineSimilarity(targetVec, getMovieVector(m))
                }}))
                .sort((a,b) => b.sim - a.sim)
                .slice(0, 6);

            const container = document.getElementById('smartMatchResults');
            container.innerHTML = scores.map(item => renderCard(item.movie, item.sim * 100)).join('');
        }}

        // Roulette Spin
        function spinRoulette() {{
            const mood = document.getElementById('rouletteMood').value;
            let pool = movies;
            if (mood !== 'All') pool = movies.filter(m => m.mood === mood);
            if (!pool.length) pool = movies;

            const picked = pool[Math.floor(Math.random() * pool.length)];
            confetti({{ particleCount: 70, spread: 60, origin: {{ y: 0.6 }} }});

            document.getElementById('rouletteResult').innerHTML = `
                <div style="background: rgba(229,9,20,0.1); border: 1px solid var(--accent-red); border-radius: 14px; padding: 14px; margin-top: 14px;">
                    <h3 style="color: #fff; margin-bottom: 6px;">🎉 Tonight's Pick:</h3>
                    ${{renderCard(picked)}}
                </div>
            `;
        }}

        // Quiz Logic
        function selectOption(el, qKey, val) {{
            el.parentElement.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            el.classList.add('selected');
            quizAnswers[qKey] = val;
        }}

        function solveQuiz() {{
            let matches = movies.filter(m => m.genre === quizAnswers.q1 || (m.mood && m.mood.includes(quizAnswers.q1)));
            if (!matches.length) matches = movies;
            matches.sort((a,b) => b.rating - a.rating);
            const pick = matches[0];
            confetti({{ particleCount: 60, spread: 50, origin: {{ y: 0.7 }} }});

            document.getElementById('quizResult').innerHTML = `
                <div style="background: rgba(37,211,102,0.1); border: 1px solid var(--green); border-radius: 14px; padding: 14px; margin-top: 14px;">
                    <h3 style="color: #fff; margin-bottom: 6px;">🌟 Your Perfect Match:</h3>
                    ${{renderCard(pick, 98)}}
                </div>
            `;
        }}
    </script>
</body>
</html>
"""

with open(r"C:\Users\Nucom\Projects\MovieRecommender\index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("[OK] Successfully generated index.html for permanent GitHub Pages deployment!")
