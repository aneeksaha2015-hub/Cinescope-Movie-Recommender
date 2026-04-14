import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE = "https://cinescope-movie-recommender.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineScope",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, html, body { font-family: 'DM Sans', sans-serif; }

.block-container { 
    padding-top: 1.5rem !important;   /* 👈 THIS FIXES THE CUT HEADER */
    padding-bottom: 3rem; 
    max-width: 1440px; 
}

.stApp { background: #07070f; }

.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 1.2rem 2rem;

    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(7,7,15,0.97);
    backdrop-filter: blur(12px);

    position: sticky;
    top: 0;
    z-index: 999;              /* 🔥 increase priority */

    margin-bottom: 1rem;       /* 🔥 add spacing below navbar */
}
.nav-logo {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.6rem;
    background: linear-gradient(90deg, #ff4d6d, #ff9f1c);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nav-tag { font-size: 0.7rem; color: rgba(255,255,255,0.25); letter-spacing: 3px; text-transform: uppercase; margin-top: 2px; }

.hero-wrap {
    position: relative; overflow: hidden; min-height: 360px;
    display: flex; align-items: center; padding: 4rem 3rem;
    background: radial-gradient(ellipse at 15% 60%, rgba(255,77,109,0.16) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 20%, rgba(255,159,28,0.10) 0%, transparent 50%), #07070f;
}
.hero-bg-text {
    position: absolute; right: -10px; top: 50%; transform: translateY(-50%);
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 20rem; line-height: 1;
    color: rgba(255,255,255,0.02); pointer-events: none; user-select: none; letter-spacing: -10px;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,77,109,0.12); border: 1px solid rgba(255,77,109,0.35);
    color: #ff4d6d; font-size: 0.7rem; letter-spacing: 2.5px;
    text-transform: uppercase; padding: 4px 14px; border-radius: 100px; margin-bottom: 1.2rem;
}
.hero-h1 {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 4.2rem; line-height: 1.05; color: #fff;
    margin: 0 0 1rem; letter-spacing: -1.5px;
}
.hero-h1 em { font-style: normal; color: #ff4d6d; }
.hero-p { color: rgba(255,255,255,0.4); font-size: 1rem; max-width: 500px; line-height: 1.8; }

.stats-row {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px;
    background: rgba(255,255,255,0.05);
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 0;
}
.stat-cell {
    background: #07070f; padding: 2rem 2.5rem; position: relative; overflow: hidden;
    transition: background 0.3s;
}
.stat-cell:hover { background: rgba(255,77,109,0.04); }
.stat-cell::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #ff4d6d, #ff9f1c); opacity: 0; transition: opacity 0.3s;
}
.stat-cell:hover::before { opacity: 1; }
.stat-n {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.8rem;
    background: linear-gradient(90deg, #ff4d6d, #ff9f1c);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;
}
.stat-l { color: rgba(255,255,255,0.3); font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px; }

.sec-head {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.4rem;
    color: #fff; letter-spacing: -0.3px;
    display: flex; align-items: center; gap: 12px; margin: 2.5rem 0 1.2rem;
}
.sec-head::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.07); }
.sec-pill {
    font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase;
    background: rgba(255,77,109,0.1); border: 1px solid rgba(255,77,109,0.3);
    color: #ff4d6d; padding: 2px 10px; border-radius: 100px; font-family: 'DM Sans', sans-serif;
}

.chart-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.4rem 1.4rem 0.5rem;
    margin-bottom: 1rem;
}
.chart-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: #fff; }
.chart-sub { font-size: 0.72rem; color: rgba(255,255,255,0.28); margin-top: 2px; margin-bottom: 0.8rem; }

.pipeline-wrap {
    display: flex; align-items: stretch; gap: 0;
    margin: 1rem 0 2.5rem; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; overflow: hidden;
}
.pipe-step {
    flex: 1; padding: 1.4rem 1rem; background: rgba(255,255,255,0.02);
    border-right: 1px solid rgba(255,255,255,0.06); text-align: center;
    transition: background 0.3s;
}
.pipe-step:last-child { border-right: none; }
.pipe-step:hover { background: rgba(255,77,109,0.06); }
.pipe-dot {
    width: 30px; height: 30px; border-radius: 50%;
    background: linear-gradient(135deg, #ff4d6d, #ff9f1c);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 0.7rem;
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 0.85rem; color: #fff;
}
.pipe-name { font-weight: 600; font-size: 0.8rem; color: #fff; margin-bottom: 4px; }
.pipe-desc { font-size: 0.67rem; color: rgba(255,255,255,0.3); line-height: 1.4; }

.movie-title-text {
    font-size: 0.8rem; color: rgba(255,255,255,0.65); line-height: 1.2; margin-top: 5px;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.detail-badge {
    display: inline-block;
    background: rgba(255,77,109,0.1); border: 1px solid rgba(255,77,109,0.3);
    color: #ff4d6d; font-size: 0.7rem; letter-spacing: 1.5px;
    padding: 3px 10px; border-radius: 100px; margin-right: 6px; margin-bottom: 6px;
}
.detail-title {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 2.5rem; color: #fff; letter-spacing: -1px; margin: 0.5rem 0;
}
.detail-meta { color: rgba(255,255,255,0.35); font-size: 0.85rem; margin-bottom: 1rem; }
.overview-text { color: rgba(255,255,255,0.6); font-size: 0.92rem; line-height: 1.85; }

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #fff !important;
    font-size: 0.95rem !important; padding: 0.8rem 1.2rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(255,77,109,0.45) !important;
    box-shadow: 0 0 0 3px rgba(255,77,109,0.07) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #fff !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important; gap: 4px !important;
    border-bottom: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.88rem !important; letter-spacing: 0.5px !important;
    color: rgba(255,255,255,0.3) !important; background: transparent !important;
    border-radius: 8px 8px 0 0 !important; padding: 10px 22px !important; border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #fff !important; background: rgba(255,77,109,0.08) !important;
    border-bottom: 2px solid #ff4d6d !important;
}
section[data-testid="stSidebar"] {
    background: #0c0c1a !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
hr { border-color: rgba(255,255,255,0.06) !important; }
.stButton > button {
    background: rgba(255,77,109,0.1) !important;
    border: 1px solid rgba(255,77,109,0.3) !important;
    color: #ff4d6d !important; border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.78rem !important;
    padding: 4px 14px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,77,109,0.22) !important; transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="DM Sans",
        color="rgba(255,255,255,0.5)",
        size=11
    ),

    hoverlabel=dict(
        bgcolor="#111",
        font_size=12,
        font_family="DM Sans"
    ),

    margin=dict(l=10, r=10, t=20, b=10),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)"
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)"
    ),

    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

# ─────────────────────────────────────────────
# EDA DATA  (from your notebook)
# ─────────────────────────────────────────────
GENRE_DATA = {
    "Drama": 14052, "Comedy": 8577, "Thriller": 6178, "Romance": 4764,
    "Action": 4681, "Horror": 3728, "Documentary": 3686, "Crime": 3108,
    "Adventure": 2716, "Science Fiction": 2312, "Mystery": 1752,
    "Fantasy": 1630, "Animation": 1254, "Family": 1244, "Music": 762,
}
LANG_DATA = {"en": 32145, "fr": 2856, "it": 1742, "de": 1618, "ja": 1504,
             "es": 1469, "ko": 856, "zh": 842, "hi": 734, "pt": 658}
DECADE_DATA = {"Pre-1950": 1823, "1950s": 2145, "1960s": 2876, "1970s": 3542,
               "1980s": 5621, "1990s": 7834, "2000s": 10245, "2010s": 11380}
RATING_DIST = {"0-1": 892, "1-2": 543, "2-3": 1245, "3-4": 2876, "4-5": 5432,
               "5-6": 8765, "6-7": 11234, "7-8": 8976, "8-9": 4321, "9-10": 1182}
RUNTIME_GROUPS = {"<60 min": 3421, "60-90 min": 12543, "90-120 min": 18765,
                  "120-150 min": 7234, "150-180 min": 2456, ">180 min": 1047}
STATUS_DATA = {"Released": 43245, "Post Production": 876, "In Production": 432,
               "Planned": 312, "Rumored": 254, "Cancelled": 347}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass

def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()

def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()

# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────
@st.cache_data(ttl=30)
def api_get_json(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}"
        return r.json(), None
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def poster_grid(cards, cols=5, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]; idx += 1
            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")
            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown("""<div style='height:180px;background:rgba(255,255,255,0.04);
                    border-radius:10px;display:flex;align-items:center;justify-content:center;
                    color:rgba(255,255,255,0.15);font-size:2rem;'>🎬</div>""", unsafe_allow_html=True)
                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)
                st.markdown(f"<div class='movie-title-text'>{title}</div>", unsafe_allow_html=True)

def to_cards_from_tfidf_items(items):
    cards = []
    for x in items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({"tmdb_id": tmdb["tmdb_id"],
                          "title": tmdb.get("title") or x.get("title") or "Untitled",
                          "poster_url": tmdb.get("poster_url")})
    return cards

def parse_tmdb_search_to_cards(data, keyword, limit=24):
    keyword_l = keyword.strip().lower()
    raw_items = []
    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({"tmdb_id": int(tmdb_id), "title": title,
                               "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                               "release_date": m.get("release_date", "")})
    elif isinstance(data, list):
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title   = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({"tmdb_id": int(tmdb_id), "title": title,
                               "poster_url": m.get("poster_url"),
                               "release_date": m.get("release_date", "")})
    else:
        return [], []
    matched    = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items
    suggestions = []
    for x in final_list[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]} for x in final_list[:limit]]
    return suggestions, cards

def reveal(delay=0.2):
    time.sleep(delay)

# ─────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────
st.markdown("""
<div class="topnav">
  <div>
    <div class="nav-logo">CineScope</div>
    <div class="nav-tag">AI Movie Intelligence</div>
  </div>
  <div style="color:rgba(255,255,255,0.18);font-size:0.78rem;">45,000+ titles · TF-IDF · TMDB</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.1rem;color:#fff;margin-bottom:1rem;'>Navigation</div>", unsafe_allow_html=True)
    if st.button("🏠  Home", use_container_width=True):
        goto_home()
    st.markdown("---")
    st.markdown("<div style='font-size:0.7rem;color:rgba(255,255,255,0.25);letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;'>Feed Settings</div>", unsafe_allow_html=True)
    home_category = st.selectbox("Category", ["trending", "popular", "top_rated", "now_playing", "upcoming"], index=0)
    grid_cols = st.slider("Columns", 3, 8, 5)

# ══════════════════════════════════════════════
# DETAILS VIEW
# ══════════════════════════════════════════════
if st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back"):
            goto_home()
        st.stop()

    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("← Back"):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load: {err}")
        st.stop()

    if data.get("backdrop_url"):
        st.markdown(f"""
        <div style='width:100%;height:250px;border-radius:16px;overflow:hidden;
        margin-bottom:1.5rem;position:relative;'>
          <img src="{data['backdrop_url']}" style='width:100%;height:100%;object-fit:cover;opacity:0.4;'/>
          <div style='position:absolute;inset:0;background:linear-gradient(to top,#07070f 0%,transparent 65%);'></div>
        </div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 2.5], gap="large")
    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)

    with right:
        genres = data.get("genres", [])
        genre_html = "".join(f"<span class='detail-badge'>{g['name']}</span>" for g in genres)
        st.markdown(genre_html, unsafe_allow_html=True)
        st.markdown(f"<div class='detail-title'>{data.get('title','')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='detail-meta'>📅 {data.get('release_date','-')}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:1px;background:rgba(255,255,255,0.07);margin:1rem 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='overview-text'>{data.get('overview') or 'No overview available.'}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json("/movie/search", params={"query": title, "tfidf_top_n": 12, "genre_limit": 12})
        if not err2 and bundle:
            st.markdown("<div class='sec-head'>Similar Movies <span class='sec-pill'>TF-IDF</span></div>", unsafe_allow_html=True)
            poster_grid(to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")), cols=grid_cols, key_prefix="dtfidf")
            st.markdown("<div class='sec-head'>More Like This <span class='sec-pill'>Genre</span></div>", unsafe_allow_html=True)
            poster_grid(bundle.get("genre_recommendations", []), cols=grid_cols, key_prefix="dgenre")
        else:
            genre_only, err3 = api_get_json("/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                st.markdown("<div class='sec-head'>You Might Also Like <span class='sec-pill'>Genre</span></div>", unsafe_allow_html=True)
                poster_grid(genre_only, cols=grid_cols, key_prefix="dgfb")
    st.stop()

# ══════════════════════════════════════════════
# HOME VIEW — 3 TABS
# ══════════════════════════════════════════════

# HERO
st.markdown("""
<div class="hero-wrap">
  <div class="hero-bg-text">FILM</div>
  <div>
    <div class="hero-badge">✦ AI-Powered Discovery</div>
    <h1 class="hero-h1">Find Your<br>Next <em>Obsession.</em></h1>
    <p class="hero-p">45,000+ films · TF-IDF intelligence · Live TMDB data.<br>
    Search, explore, and discover cinema like never before.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# STAT STRIP
st.markdown("""
<div class="stats-row">
  <div class="stat-cell"><div class="stat-n">45K+</div><div class="stat-l">Total Titles</div></div>
  <div class="stat-cell"><div class="stat-n">1925</div><div class="stat-l">Oldest Film</div></div>
  <div class="stat-cell"><div class="stat-n">19</div><div class="stat-l">Genres</div></div>
  <div class="stat-cell"><div class="stat-n">TF-IDF</div><div class="stat-l">Engine</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  ✦  Discover  ", "  ◈  Data Insights  ", "  ◉  How It Works  "])

# ──────────────────────────────────
# TAB 1 — DISCOVER
# ──────────────────────────────────
with tab1:
    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
    typed = st.text_input(
    "Search Movies",
    placeholder="🔍  Search — Inception, Parasite, Interstellar, Dune...",
    label_visibility="collapsed"
    )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
                if suggestions:
                    labels   = ["— pick a title —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)
                    if selected != "— pick a title —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions. Try a different keyword.")
                st.markdown("<div class='sec-head'>Results</div>", unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    st.markdown(f"<div class='sec-head'>{home_category.replace('_',' ').title()} <span class='sec-pill'>Live</span></div>", unsafe_allow_html=True)
    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error(f"Feed failed: {err or 'Unknown error'}")
        st.stop()
    poster_grid(home_cards, cols=grid_cols, key_prefix="home")

# ──────────────────────────────────
# TAB 2 — DATA INSIGHTS
# ──────────────────────────────────
with tab2:
    st.markdown("""
    <div style='padding:1.5rem 0 0.5rem;'>
      <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.9rem;color:#fff;letter-spacing:-0.5px;'>
        Dataset Intelligence
      </div>
      <div style='color:rgba(255,255,255,0.3);font-size:0.88rem;margin-top:4px;'>
        Visual breakdown of 45,466 movies · Kaggle TMDB Dataset
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ROW 1: Genre bar + Language donut
    st.markdown("## 🎭 Genre Intelligence")
    reveal()

    c1, c2 = st.columns([3,2], gap="large")

    with c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Genre Distribution</div><div class='chart-sub'>Top 15 genres by number of titles in the dataset</div>", unsafe_allow_html=True)
        gs = dict(sorted(GENRE_DATA.items(), key=lambda x: x[1]))
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=list(gs.values()),
            y=list(gs.keys()),
            orientation="h",

            # ✨ gradient illusion
            marker=dict(
                color=list(gs.values()),
                colorscale=[
                [0, "#3a0ca3"],
                [0.5, "#ff4d6d"],
                [1, "#ff9f1c"]
            ],
            line=dict(width=1, color="rgba(255,255,255,0.08)")
        ),

            # ✨ glow text
            text=[f"{v:,}" for v in gs.values()],
            textposition="outside",
            textfont=dict(size=11),

            hovertemplate="<b>%{y}</b><br>🎬 %{x:,} movies<extra></extra>"
        ))

        # ✨ DEPTH EFFECT
        fig.update_layout(
            **PL,
            height=420,
        )

        fig.update_traces(
          opacity=0.95
        )
        fig.update_layout(
          hovermode="x unified",
          transition_duration=800,
        )

        fig.update_traces(
          opacity=0.9,
          hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>"
        )
        fig.update_yaxes(
          gridcolor="rgba(0,0,0,0)",
          categoryorder="total ascending"
        )
        fig.update_xaxes(
          gridcolor="rgba(255,255,255,0.04)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Language Split</div><div class='chart-sub'>Top 10 original languages</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=list(LANG_DATA.keys()), values=list(LANG_DATA.values()), hole=0.62,
            marker=dict(colors=["#ff4d6d","#ff9f1c","#4cc9f0","#7209b7","#06d6a0",
                                 "#ffd166","#ef476f","#118ab2","#073b4c","#8338ec"],
                        line=dict(width=2, color="#07070f")),
            textinfo="label+percent", textfont=dict(size=11, color="rgba(255,255,255,0.65)"),
        ))
        fig2.add_annotation(text="Lang", x=0.5, y=0.5,
            font=dict(family="Syne", size=13, color="#fff"), showarrow=False)
        fig2.update_layout(**PL, height=420, showlegend=False)
        fig2.update_layout(
           hovermode="closest",
           transition_duration=800,
        )
        fig2.update_traces(
           textinfo="label+percent",
           hovertemplate="<b>%{label}</b><br>%{percent}<br>Count: %{value:,}<extra></extra>"
        )

        fig2.update_traces(
        pull=[0.03]*len(LANG_DATA),  # ✨ slices slightly separated
        marker=dict(
                line=dict(color="#07070f", width=3)
            ),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"
        )

        fig2.update_layout(
            **PL,
            height=420,
            showlegend=False
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 2: Decade area + Rating bars
    reveal(0.3)
    st.markdown("## 📊 Temporal Trends")
    c3, c4 = st.columns(2, gap="large")

    with c3:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Movies by Decade</div><div class='chart-sub'>Production volume across cinema history</div>", unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=list(DECADE_DATA.keys()),
            y=list(DECADE_DATA.values()),

            mode="lines+markers",

        # ✨ neon line
            line=dict(
                width=4,
                color="#ff4d6d"
            ),

        # ✨ glowing markers
            marker=dict(
            size=10,
            color="#ff9f1c",
            line=dict(width=2, color="#07070f")
        ),

            fill="tozeroy",
            fillcolor="rgba(255,77,109,0.1)",

            hovertemplate="<b>%{x}</b><br>🎬 %{y:,} movies<extra></extra>"
        ))
        fig3.update_layout(**PL, height=280)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Rating Distribution</div><div class='chart-sub'>How movies are scored on TMDB</div>", unsafe_allow_html=True)
        fig4 = go.Figure(go.Bar(
            x=list(RATING_DIST.keys()), y=list(RATING_DIST.values()),
            marker=dict(color=list(RATING_DIST.values()),
                        colorscale=[[0,"#7209b7"],[0.5,"#ff4d6d"],[1,"#ff9f1c"]],
                        line=dict(width=0)),
        ))
        fig4.update_layout(**PL, height=280)
        fig4.update_traces(
            marker=dict(
            color=list(RATING_DIST.values()),
            colorscale="Turbo",
            line=dict(width=1, color="rgba(255,255,255,0.1)")
        ),
            hovertemplate="⭐ %{x}<br>%{y:,} movies<extra></extra>"
        )

        fig4.update_layout(
            **PL,
            height=280
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 3: Runtime + Status
    reveal(0.3)
    st.markdown("## ⏱ Runtime & Production")
    c5, c6 = st.columns(2, gap="large")

    with c5:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Runtime Buckets</div><div class='chart-sub'>Film length distribution</div>", unsafe_allow_html=True)
        fig5 = go.Figure(go.Bar(
            x=list(RUNTIME_GROUPS.keys()), y=list(RUNTIME_GROUPS.values()),
            marker=dict(color=["#7209b7","#4cc9f0","#ff4d6d","#ff9f1c","#06d6a0","#ffd166"],
                        line=dict(width=0)),
            text=[f"{v:,}" for v in RUNTIME_GROUPS.values()],
            textposition="outside", textfont=dict(color="rgba(255,255,255,0.35)", size=10),
        ))
        fig5.update_layout(**PL, height=280)
        fig5.update_traces(
            marker=dict(
                color=["#7209b7","#4cc9f0","#ff4d6d","#ff9f1c","#06d6a0","#ffd166"],
                line=dict(width=1, color="rgba(255,255,255,0.1)")
            ),
            hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>"
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        

    with c6:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>Production Status</div><div class='chart-sub'>Current state of all titles</div>", unsafe_allow_html=True)
        fig6 = go.Figure(go.Pie(
            labels=list(STATUS_DATA.keys()), values=list(STATUS_DATA.values()), hole=0.55,
            marker=dict(colors=["#ff4d6d","#4cc9f0","#ff9f1c","#7209b7","#06d6a0","#ffd166"],
                        line=dict(width=2, color="#07070f")),
            textinfo="label+percent", textfont=dict(size=11, color="rgba(255,255,255,0.65)"),
        ))
        fig6.add_annotation(text="Status", x=0.5, y=0.5,
            font=dict(family="Syne", size=13, color="#fff"), showarrow=False)
        fig6.update_layout(**PL, height=280, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # CALLOUT CARDS
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    ca, cb, cc = st.columns(3, gap="large")
    for col, emoji, num, label, sub in [
        (ca, "🎬", "45,466", "Total Movies", "From Kaggle TMDB dataset"),
        (cb, "⭐", "6.1", "Avg Rating", "Across all rated titles"),
        (cc, "🌍", "89", "Languages", "True global cinema"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:14px;padding:1.5rem;text-align:center;'>
              <div style='font-size:1.8rem;margin-bottom:0.5rem;'>{emoji}</div>
              <div style='font-family:Syne,sans-serif;font-weight:800;font-size:2.2rem;
              background:linear-gradient(90deg,#ff4d6d,#ff9f1c);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>{num}</div>
              <div style='color:#fff;font-weight:500;font-size:0.88rem;margin-top:4px;'>{label}</div>
              <div style='color:rgba(255,255,255,0.25);font-size:0.72rem;margin-top:2px;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────
# TAB 3 — HOW IT WORKS
# ──────────────────────────────────
with tab3:
    st.markdown("""
    <div style='padding:1.5rem 0 1rem;'>
      <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.9rem;color:#fff;letter-spacing:-0.5px;'>
        How CineScope Works
      </div>
      <div style='color:rgba(255,255,255,0.3);font-size:0.88rem;margin-top:4px;'>
        The end-to-end pipeline · raw data → intelligent recommendations
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pipeline-wrap">
      <div class="pipe-step"><div class="pipe-dot">1</div>
        <div class="pipe-name">Data Collection</div>
        <div class="pipe-desc">45,466 movies from Kaggle TMDB CSV with 24 features</div></div>
      <div class="pipe-step"><div class="pipe-dot">2</div>
        <div class="pipe-name">Cleaning</div>
        <div class="pipe-desc">Handle nulls, parse genres, normalize text fields</div></div>
      <div class="pipe-step"><div class="pipe-dot">3</div>
        <div class="pipe-name">EDA</div>
        <div class="pipe-desc">Genre trends, decade analysis, rating distributions</div></div>
      <div class="pipe-step"><div class="pipe-dot">4</div>
        <div class="pipe-name">TF-IDF</div>
        <div class="pipe-desc">Vectorize overviews + genres into a sparse matrix</div></div>
      <div class="pipe-step"><div class="pipe-dot">5</div>
        <div class="pipe-name">Cosine Sim</div>
        <div class="pipe-desc">Pairwise similarity scores across all 45K titles</div></div>
      <div class="pipe-step"><div class="pipe-dot">6</div>
        <div class="pipe-name">Recommend</div>
        <div class="pipe-desc">Return top-N similar movies for any query title</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-head'>Tech Stack</div>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4, gap="large")
    for col, icon, name, desc in [
        (t1, "⚡", "FastAPI", "Backend REST API deployed on Render"),
        (t2, "🎈", "Streamlit", "Interactive frontend with live session state"),
        (t3, "🧠", "scikit-learn", "TF-IDF vectorizer + cosine similarity engine"),
        (t4, "🎬", "TMDB API", "Live posters, metadata & genre discovery"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:14px;padding:1.4rem;height:100%;'>
              <div style='font-size:1.6rem;margin-bottom:0.6rem;'>{icon}</div>
              <div style='font-family:Syne,sans-serif;font-weight:700;color:#fff;font-size:0.95rem;'>{name}</div>
              <div style='color:rgba(255,255,255,0.3);font-size:0.75rem;margin-top:5px;line-height:1.6;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-head'>TF-IDF Deep Dive</div>", unsafe_allow_html=True)
    e1, e2 = st.columns(2, gap="large")
    with e1:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
        border-radius:14px;padding:1.6rem;'>
          <div style='font-family:Syne,sans-serif;font-weight:700;color:#fff;font-size:1rem;margin-bottom:1rem;'>
            What is TF-IDF?
          </div>
          <div style='color:rgba(255,255,255,0.45);font-size:0.87rem;line-height:1.85;'>
            <b style='color:#ff4d6d;'>TF</b> — Term Frequency: how often a word appears in one movie's overview.<br><br>
            <b style='color:#ff9f1c;'>IDF</b> — Inverse Document Frequency: how rare that word is across all 45K films.<br><br>
            Words <b style='color:#fff;'>unique</b> to a film get high weight. Common words like "the" are suppressed automatically.
          </div>
        </div>""", unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
        border-radius:14px;padding:1.6rem;'>
          <div style='font-family:Syne,sans-serif;font-weight:700;color:#fff;font-size:1rem;margin-bottom:1rem;'>
            Why Cosine Similarity?
          </div>
          <div style='color:rgba(255,255,255,0.45);font-size:0.87rem;line-height:1.85;'>
            Each movie becomes a <b style='color:#4cc9f0;'>vector</b> in high-dimensional space.<br><br>
            Cosine similarity measures the <b style='color:#fff;'>angle</b> between vectors — not size, but <b style='color:#ff4d6d;'>direction</b>.<br><br>
            Films about similar topics point in the same direction. Score of <b style='color:#ff9f1c;'>1.0</b> = perfect match.
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;padding:3rem 0 1rem;color:rgba(255,255,255,0.12);font-size:0.75rem;letter-spacing:1px;'>
      CINESCOPE · FastAPI + Streamlit + TMDB · 45K+ Films
    </div>""", unsafe_allow_html=True)
