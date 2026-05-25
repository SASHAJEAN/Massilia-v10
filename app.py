import streamlit as st
import anthropic

st.set_page_config(
    page_title="Massilia 🌊",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — mobile-first student app vibes
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:ital,wght@0,400;0,700;0,800;0,900;1,700&display=swap');

:root {
    --blue:   #3FC0F0;
    --yellow: #F5B800;
    --cream:  #FFF8EE;
    --dark:   #1A2540;
    --pink:   #FF6B8A;
    --green:  #2DD4A0;
    --muted:  #8892A4;
    --card:   #FFFFFF;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"],
section.main > div.block-container {
    background: var(--cream) !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 0 !important;
    max-width: 100% !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"],
[data-testid="stSidebarNav"] { display: none !important; }

/* ── TOP NAV BAR ── */
.topbar {
    position: sticky; top: 0; z-index: 200;
    background: white;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.7rem 1.5rem;
    border-bottom: 2px solid rgba(63,192,240,0.12);
}
.topbar-logo {
    font-family: 'Pacifico', cursive;
    font-size: 1.7rem;
    color: var(--blue);
    line-height: 1;
}
.topbar-sub {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: var(--yellow);
    font-weight: 900;
    text-transform: uppercase;
    line-height: 1;
    margin-top: 2px;
}
.topbar-right { display: flex; gap: 0.5rem; align-items: center; }
.nav-pill {
    background: var(--blue);
    color: white;
    border-radius: 50px;
    padding: 0.4rem 1rem;
    font-weight: 800;
    font-size: 0.82rem;
    cursor: pointer;
    border: none;
}
.nav-pill.outline {
    background: transparent;
    color: var(--dark);
    border: 1.5px solid rgba(26,37,64,0.15);
}

/* ── HERO MAP SECTION ── */
.map-hero {
    position: relative;
    width: 100%;
    background: #e8f4fb;
}
.map-frame {
    width: 100%; height: 420px;
    border: none; display: block;
}
.map-overlay-card {
    position: absolute;
    top: 16px; left: 16px;
    background: white;
    border-radius: 18px;
    padding: 1rem 1.2rem;
    max-width: 300px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    z-index: 10;
}
.map-overlay-title {
    font-family: 'Pacifico', cursive;
    font-size: 1.2rem;
    color: var(--dark);
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.map-overlay-title em { color: var(--blue); font-style: normal; }
.map-overlay-sub {
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.5;
    margin-bottom: 0.8rem;
}
.map-filter-pills {
    display: flex; gap: 0.4rem; flex-wrap: wrap;
}
.filter-pill {
    border-radius: 50px;
    padding: 0.28rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 800;
    border: none;
    cursor: pointer;
    white-space: nowrap;
}
.fp-panisse  { background: #FFF3CD; color: #856404; }
.fp-pastis   { background: #D1ECF1; color: #0C5460; }
.fp-fougasse { background: #D4EDDA; color: #155724; }
.fp-all      { background: var(--dark); color: white; }

/* ── SPOT CARDS ROW ── */
.spots-section { padding: 1.5rem 1.5rem 0; }
.spots-section-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.spots-section-header h2 {
    font-size: 1.35rem;
    font-weight: 900;
    color: var(--dark);
}
.spots-section-header h2 em { color: var(--blue); font-style: normal; }
.see-all {
    font-size: 0.82rem;
    font-weight: 800;
    color: var(--blue);
    cursor: pointer;
}

/* horizontal scroll row */
.cards-scroll {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 1rem;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
}
.cards-scroll::-webkit-scrollbar { display: none; }

.spot-card {
    flex: 0 0 220px;
    border-radius: 20px;
    overflow: hidden;
    background: white;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s;
    cursor: pointer;
    text-decoration: none;
    display: block;
}
.spot-card:hover { transform: translateY(-4px); }
.spot-card-img {
    width: 100%;
    height: 140px;
    object-fit: cover;
    display: block;
}
.spot-card-body { padding: 0.85rem 1rem 0.9rem; }
.spot-card-cat {
    font-size: 0.7rem;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.cat-panisse  { color: #D4A017; }
.cat-pastis   { color: var(--blue); }
.cat-fougasse { color: var(--green); }
.cat-other    { color: var(--pink); }
.spot-card-name {
    font-weight: 900;
    font-size: 0.98rem;
    color: var(--dark);
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.spot-card-vibe {
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.4;
}
.spot-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    border-top: 1px solid #f0f0f0;
}
.price-badge {
    font-size: 0.78rem;
    font-weight: 900;
    color: var(--green);
}
.rating { font-size: 0.78rem; color: var(--yellow); font-weight: 800; }

/* ── VIBES MOOD SECTION ── */
.vibes-section { padding: 1.5rem; }
.vibes-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
}
.vibe-tile {
    border-radius: 18px;
    overflow: hidden;
    aspect-ratio: 1;
    position: relative;
    cursor: pointer;
}
.vibe-tile img {
    width: 100%; height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s;
}
.vibe-tile:hover img { transform: scale(1.08); }
.vibe-tile-label {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: rgba(26,37,64,0.42);
    color: white;
    text-align: center;
    padding: 0.5rem;
    transition: background 0.2s;
}
.vibe-tile:hover .vibe-tile-label { background: rgba(63,192,240,0.65); }
.vibe-tile-emoji { font-size: 1.6rem; margin-bottom: 0.2rem; }
.vibe-tile-text { font-size: 0.72rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── AI DISCOVERY CARD ── */
.ai-section { padding: 0 1.5rem 1.5rem; }
.ai-card {
    background: var(--dark);
    border-radius: 24px;
    padding: 1.8rem;
    position: relative;
    overflow: hidden;
}
.ai-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: rgba(63,192,240,0.15);
    border-radius: 50%;
}
.ai-card::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 150px; height: 150px;
    background: rgba(245,184,0,0.1);
    border-radius: 50%;
}
.ai-eyebrow {
    font-size: 0.7rem;
    font-weight: 900;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--yellow);
    margin-bottom: 0.4rem;
}
.ai-title {
    font-family: 'Pacifico', cursive;
    font-size: 1.6rem;
    color: white;
    line-height: 1.2;
    margin-bottom: 0.5rem;
    position: relative; z-index: 1;
}
.ai-sub { font-size: 0.85rem; color: rgba(255,255,255,0.65); margin-bottom: 1.5rem; position: relative; z-index: 1; }

/* Form elements inside dark card */
.ai-form-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1rem; position: relative; z-index: 1; }
.ai-form-group { flex: 1; min-width: 120px; }
.ai-form-label { font-size: 0.7rem; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 0.35rem; }

/* ── COMMUNITY SECTION ── */
.community-section { padding: 0 1.5rem 1.5rem; }
.community-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
}
.community-card {
    background: white;
    border-radius: 18px;
    padding: 1.1rem 1.2rem;
    border-left: 4px solid var(--yellow);
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.community-card.blue  { border-left-color: var(--blue); }
.community-card.green { border-left-color: var(--green); }
.community-card.pink  { border-left-color: var(--pink); }
.community-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    overflow: hidden; flex-shrink: 0;
}
.community-avatar img { width: 100%; height: 100%; object-fit: cover; }
.community-name { font-weight: 800; font-size: 0.88rem; color: var(--dark); }
.community-role { font-size: 0.72rem; color: var(--muted); }
.community-quote {
    font-size: 0.88rem;
    line-height: 1.55;
    color: var(--dark);
    margin: 0.7rem 0 0.5rem;
    font-style: italic;
}
.community-spot-tag {
    display: inline-block;
    background: rgba(63,192,240,0.1);
    color: var(--blue);
    border-radius: 50px;
    padding: 0.2rem 0.7rem;
    font-size: 0.72rem;
    font-weight: 800;
}

/* ── RESULT BOX ── */
.result-box {
    background: white;
    border-radius: 20px;
    padding: 1.5rem 1.6rem;
    border-left: 5px solid var(--blue);
    margin-top: 1rem;
    font-size: 0.93rem;
    line-height: 1.75;
    color: var(--dark);
    position: relative; z-index: 1;
}
.result-box h3 {
    font-family: 'Pacifico', cursive;
    font-size: 1.15rem;
    color: var(--blue);
    margin-bottom: 0.7rem;
}

/* ── NEWSLETTER ── */
.newsletter {
    margin: 0 1.5rem 1.5rem;
    background: var(--blue);
    border-radius: 24px;
    padding: 2rem 1.8rem;
    text-align: center;
}
.newsletter h2 {
    font-family: 'Pacifico', cursive;
    font-size: 1.6rem;
    color: white;
    margin-bottom: 0.4rem;
}
.newsletter p { font-size: 0.88rem; color: rgba(255,255,255,0.85); margin-bottom: 1.2rem; }

/* ── FOOTER ── */
.footer {
    background: var(--dark);
    padding: 2rem 1.5rem 1.5rem;
    text-align: center;
}
.footer-logo { font-family: 'Pacifico', cursive; font-size: 1.4rem; color: var(--blue); margin-bottom: 0.3rem; }
.footer-sub { font-size: 0.72rem; color: rgba(255,255,255,0.3); margin-top: 0.3rem; }

/* ── STREAMLIT OVERRIDES ── */
div.stButton > button {
    background: var(--yellow) !important;
    color: var(--dark) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1rem !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
div.stButton > button:hover {
    background: white !important;
    color: var(--dark) !important;
    transform: scale(1.02) !important;
}
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: white !important;
}
div[data-baseweb="select"] svg { color: rgba(255,255,255,0.5) !important; }
[data-testid="stSlider"] div[role="slider"] { background: var(--yellow) !important; }
[data-testid="stSlider"] [data-testid="stTickBar"] { display: none; }
textarea {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.15) !important;
}
textarea::placeholder { color: rgba(255,255,255,0.35) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 50px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.85rem !important;
}
[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }
div[data-testid="column"] { padding: 0 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "recs" not in st.session_state:
    st.session_state.recs = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "map"

SPOTS = [
    {
        "name": "Chez Étienne",
        "category": "Panisse",
        "vibe": "Noailles · locals only, cash",
        "price": "€",
        "rating": "4.9",
        "tip": "Order the panisse nature and eat standing at the counter – perfect before midi.",
        "author": "Lucas", "role": "Étudiant AMU",
        "img": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80",
        "avatar": "https://i.pravatar.cc/80?img=12",
    },
    {
        "name": "Bar de la Marine",
        "category": "Pastis",
        "vibe": "Vieux-Port · Marcel Pagnol vibes",
        "price": "€€",
        "rating": "4.8",
        "tip": "Golden hour outside. Ricard + olives = la vie.",
        "author": "Sofia", "role": "Backpacker",
        "img": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=400&q=80",
        "avatar": "https://i.pravatar.cc/80?img=25",
    },
    {
        "name": "Fougasserie du Panier",
        "category": "Fougasse",
        "vibe": "Le Panier · hidden bakery",
        "price": "€",
        "rating": "4.7",
        "tip": "Anchovy & olive at 8h before tourists arrive.",
        "author": "Théo", "role": "Jeune actif",
        "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&q=80",
        "avatar": "https://i.pravatar.cc/80?img=33",
    },
    {
        "name": "Café Populaire",
        "category": "Pastis",
        "vibe": "Cours Julien · boho terrace",
        "price": "€€",
        "rating": "4.6",
        "tip": "Sunday brunch then stay for the afternoon pastis session.",
        "author": "Anaïs", "role": "Freelance",
        "img": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400&q=80",
        "avatar": "https://i.pravatar.cc/80?img=44",
    },
    {
        "name": "L'Épicerie du Midi",
        "category": "Panisse",
        "vibe": "Noailles · marché vibe",
        "price": "€",
        "rating": "4.5",
        "tip": "Hot panisse in a paper cone straight from the fryer.",
        "author": "Marco", "role": "Backpacker",
        "img": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=400&q=80",
        "avatar": "https://i.pravatar.cc/80?img=55",
    },
]

CAT_CLASS = {"Panisse": "cat-panisse", "Pastis": "cat-pastis", "Fougasse": "cat-fougasse", "Other": "cat-other"}
CARD_ACCENT = {"Panisse": "yellow", "Pastis": "blue", "Fougasse": "green", "Other": "pink"}

# ══════════════════════════════════════════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div>
    <div class="topbar-logo">Massilia</div>
    <div class="topbar-sub">Panis · Pastis · Fougasse</div>
  </div>
  <div class="topbar-right">
    <button class="nav-pill outline">Sign in</button>
    <button class="nav-pill">Explore 🌊</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1 ── MAP FIRST — full width hero
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="map-hero">
  <div class="map-overlay-card">
    <div class="map-overlay-title">Find the best spots in <em>Marseille</em></div>
    <div class="map-overlay-sub">Authentic addresses hand-picked by students & locals — zero tourist traps.</div>
    <div class="map-filter-pills">
      <span class="filter-pill fp-all">All</span>
      <span class="filter-pill fp-panisse">🍟 Panisse</span>
      <span class="filter-pill fp-pastis">🥛 Pastis</span>
      <span class="filter-pill fp-fougasse">🫓 Fougasse</span>
    </div>
  </div>
  <iframe class="map-frame"
    src="https://www.openstreetmap.org/export/embed.html?bbox=5.342%2C43.281%2C5.408%2C43.311&layer=mapnik"
    title="Marseille food map">
  </iframe>
</div>
<div style="background:white;padding:0.6rem 1.5rem;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #f0f0f0;">
  <span style="font-size:0.8rem;color:var(--muted);">📍 Showing <b style="color:var(--dark);">Marseille centre</b> — 12 spots nearby</span>
  <a href="https://www.openstreetmap.org/?mlat=43.2965&mlon=5.3698#map=14/43.2965/5.3698"
     target="_blank"
     style="font-size:0.78rem;font-weight:800;color:var(--blue);text-decoration:none;">
     Full map ↗
  </a>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2 ── HOT RIGHT NOW — horizontal scroll cards
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="spots-section">
  <div class="spots-section-header">
    <h2>🔥 Hot right <em>now</em></h2>
    <span class="see-all">See all →</span>
  </div>
  <div class="cards-scroll">
""", unsafe_allow_html=True)

for s in SPOTS:
    cat_class = CAT_CLASS.get(s["category"], "cat-other")
    st.markdown(f"""
    <div class="spot-card">
      <img class="spot-card-img" src="{s['img']}" alt="{s['name']}" loading="lazy"/>
      <div class="spot-card-body">
        <div class="spot-card-cat {cat_class}">{s['category']}</div>
        <div class="spot-card-name">{s['name']}</div>
        <div class="spot-card-vibe">{s['vibe']}</div>
        <div class="spot-card-footer">
          <span class="price-badge">{s['price']}</span>
          <span class="rating">★ {s['rating']}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3 ── MOOD VIBES GRID — photo tiles
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="vibes-section">
  <div class="spots-section-header">
    <h2>Choose your <em>vibe</em></h2>
    <span class="see-all">Filter AI ↓</span>
  </div>
  <div class="vibes-grid">
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1566937169390-b55a2639aad3?w=300&q=75" alt="sunset apero" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🌅</div>
        <div class="vibe-tile-text">Sunset Apéro</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=300&q=75" alt="panisse" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🍟</div>
        <div class="vibe-tile-text">Cheap Eats</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=75" alt="beach" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🏖️</div>
        <div class="vibe-tile-text">Beach Day</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?w=300&q=75" alt="night out" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🎉</div>
        <div class="vibe-tile-text">Night Out</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=300&q=75" alt="cafe" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">☕</div>
        <div class="vibe-tile-text">Chill Café</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=300&q=75" alt="friends" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">👯</div>
        <div class="vibe-tile-text">With Friends</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=300&q=75" alt="hidden gems" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🤫</div>
        <div class="vibe-tile-text">Hidden Gem</div>
      </div>
    </div>
    <div class="vibe-tile">
      <img src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=300&q=75" alt="dinner" loading="lazy"/>
      <div class="vibe-tile-label">
        <div class="vibe-tile-emoji">🍽️</div>
        <div class="vibe-tile-text">Proper Dinner</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4 ── AI DISCOVERY — dark card
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="ai-section">
  <div class="ai-card">
    <div class="ai-eyebrow">✨ AI-powered</div>
    <div class="ai-title">Tell me your vibe,<br>I'll find your spot</div>
    <div class="ai-sub">Personalized recs based on your mood, budget & what you're feeling right now.</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="ai-form-label">🎭 Mood</div>', unsafe_allow_html=True)
    mood = st.selectbox("m", ["😎 Chill apéro","🌅 Sunset spot","🎉 Going out","☀️ Beach lunch","🤫 Hidden gem","💸 Super broke","🍽️ Dinner","🧘 Solo"], label_visibility="collapsed", key="mood")
with c2:
    st.markdown('<div class="ai-form-label">👥 Group</div>', unsafe_allow_html=True)
    group = st.selectbox("g", ["Friends","Solo","Date night","Family","Backpackers"], label_visibility="collapsed", key="group")
with c3:
    st.markdown('<div class="ai-form-label">🎵 Music</div>', unsafe_allow_html=True)
    music = st.selectbox("mu", ["Electro/House","No pref","Jazz/Soul","Hip-hop","Reggae","Quiet"], label_visibility="collapsed", key="music")

c4, c5 = st.columns([1,1])
with c4:
    st.markdown('<div class="ai-form-label">💶 Budget max</div>', unsafe_allow_html=True)
    budget = st.slider("b", 5, 60, 15, step=5, label_visibility="collapsed", key="budget", format="€%d")
with c5:
    st.markdown('<div class="ai-form-label">📍 Area</div>', unsafe_allow_html=True)
    area = st.selectbox("a", ["Anywhere","Vieux-Port","Cours Julien","Noailles","Endoume","Pointe Rouge","Le Panier"], label_visibility="collapsed", key="area")

st.markdown('<div class="ai-form-label" style="margin-top:0.5rem;">✏️ Anything else?</div>', unsafe_allow_html=True)
freetext = st.text_area("ft", placeholder="Sea view terrace, cheap pastis, avoid touristy spots…", height=65, label_visibility="collapsed", key="freetext")

go = st.button("🌊 Find my perfect spot — it's free")

st.markdown("</div></div>", unsafe_allow_html=True)

# ── AI call ────────────────────────────────────────────────────────────────────
if go:
    prompt = f"""You are Massilia, an AI guide for authentic Marseille food & lifestyle.
Give exactly 3 personalized spot recommendations.

User: mood={mood}, group={group}, music={music}, budget=€{budget}/person, area={area}
Notes: {freetext or 'none'}

Focus: panisse, pastis bars, fougasse, sunset bars, beach restaurants, hidden gems.

For each spot use exactly this format:
**[Name]** · [neighbourhood]
🍽️ Order: ...
💶 Price: ...
🌊 Vibe: ...
🔑 Tip: ...

Tone: warm, fun, local — like a Marseillais mate texting you. Use occasional French naturally. Short sign-off line at end."""

    with st.spinner("Cherching les bons plans… 🌊"):
        try:
            client = anthropic.Anthropic()
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=900,
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.recs = msg.content[0].text
        except Exception as e:
            st.session_state.recs = f"⚠️ AI unavailable: {e}"

if st.session_state.recs:
    st.markdown('<div class="ai-section" style="padding-top:0">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-box">
      <h3>🌊 Your spots</h3>
      {st.session_state.recs.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5 ── COMMUNITY VOICES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="community-section">
  <div class="spots-section-header" style="margin-bottom:1rem;">
    <h2>🌊 Real <em>locals</em> say</h2>
    <span class="see-all">All stories →</span>
  </div>
  <div class="community-grid">
""", unsafe_allow_html=True)

community_posts = [
    {"author":"Julien M.","role":"Design student, AMU","avatar":"https://i.pravatar.cc/80?img=7",
     "quote":"The best way to see the city is at 6am when the sun hits the Mucem. It feels like the whole city is waking up from a dream. Don't skip the rooftop!",
     "tag":"Mucem at sunrise","accent":"blue"},
    {"author":"Anaëlis R.","role":"New here, Lyon","avatar":"https://i.pravatar.cc/80?img=47",
     "quote":"My grandmother's bouillabaisse recipe is a secret, but I can tell you where to buy the freshest rouget at the morning market in Noailles.",
     "tag":"Noailles market","accent":"yellow"},
    {"author":"Marco S.","role":"Graphic designer, local","avatar":"https://i.pravatar.cc/80?img=60",
     "quote":"The street art scene here changes constantly. Every week there's a new gallery. Best spots are behind the metro station.",
     "tag":"Street art tour","accent":"green"},
]

for p in community_posts:
    st.markdown(f"""
    <div class="community-card {p['accent']}">
      <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.7rem;">
        <div class="community-avatar">
          <img src="{p['avatar']}" alt="{p['author']}" loading="lazy"/>
        </div>
        <div>
          <div class="community-name">{p['author']}</div>
          <div class="community-role">{p['role']}</div>
        </div>
      </div>
      <div class="community-quote">"{p['quote']}"</div>
      <span class="community-spot-tag">📍 {p['tag']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6 ── SHARE A SPOT (clean tab form)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="community-section" style="padding-top:0;">
  <div class="spots-section-header" style="margin-bottom:1rem;">
    <h2>✍️ Share your <em>hidden gem</em></h2>
  </div>
""", unsafe_allow_html=True)

with st.form("share_form", clear_on_submit=True):
    fs1, fs2 = st.columns(2)
    with fs1:
        s_name = st.text_input("Spot name *", placeholder="e.g. Chez Jeannot")
        s_vibe = st.text_input("Neighbourhood / vibe", placeholder="e.g. Le Panier, cash only")
    with fs2:
        s_cat  = st.selectbox("Type", ["Panisse 🍟","Pastis 🥛","Fougasse 🫓","Other 🍽️"])
        s_price= st.selectbox("Price", ["€ under €10","€€ €10–20","€€€ €20+"])
    s_tip    = st.text_area("Your tip *", placeholder="What to order, best time, secret trick…", height=80)
    s_author = st.text_input("Your name", placeholder="e.g. Théo, étudiant")
    submitted = st.form_submit_button("🌊 Add to the map")
    if submitted:
        if s_name and s_tip:
            st.success(f"🎉 Merci ! **{s_name}** is now on the Massilia map.")
        else:
            st.warning("Fill in name + tip at minimum.")

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7 ── NEWSLETTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="newsletter">
  <h2>The insider's newsletter.</h2>
  <p>No spam. Only secret openings, local events, and the best places<br>to hide from the tourists this summer.</p>
  <div style="display:flex;gap:0.6rem;max-width:400px;margin:0 auto;flex-wrap:wrap;justify-content:center;">
    <input type="email" placeholder="Your email address"
      style="border-radius:50px;border:none;padding:0.65rem 1.2rem;
             font-family:Nunito,sans-serif;font-size:0.9rem;flex:1;min-width:180px;outline:none;"/>
    <button style="background:var(--yellow);color:var(--dark);border:none;border-radius:50px;
                   padding:0.65rem 1.4rem;font-family:Nunito,sans-serif;font-weight:900;
                   font-size:0.9rem;cursor:pointer;white-space:nowrap;">
      Subscribe
    </button>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="footer-logo">Massilia</div>
  <div style="font-size:0.75rem;color:rgba(255,255,255,0.45);font-style:italic;margin:0.3rem 0 1rem;">
    Pas fâché avec le plaisir 🌊
  </div>
  <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1.2rem;">
    <a href="#" style="color:rgba(255,255,255,0.45);font-size:0.82rem;text-decoration:none;">Explore</a>
    <a href="#" style="color:rgba(255,255,255,0.45);font-size:0.82rem;text-decoration:none;">Map</a>
    <a href="#" style="color:rgba(255,255,255,0.45);font-size:0.82rem;text-decoration:none;">Community</a>
    <a href="#" style="color:rgba(255,255,255,0.45);font-size:0.82rem;text-decoration:none;">Contact</a>
  </div>
  <div class="footer-sub">© 2025 Massilia · Panis · Pastis · Fougasse</div>
</div>
""", unsafe_allow_html=True)
