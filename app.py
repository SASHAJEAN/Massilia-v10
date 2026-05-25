import streamlit as st
import anthropic

st.set_page_config(
    page_title="Massilia 🌊",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Real Massilia logo — faithful SVG recreation from uploaded brand image ──
# Blue Pacifico-style script "Massilia" + fork integrated into M stem
# + gold compass dot above second s + gold "PANIS · PASTIS · FOUGASSE" subtitle
LOGO_NAV = """
<svg viewBox="0 0 380 72" xmlns="http://www.w3.org/2000/svg" style="height:48px;width:auto;display:block;">
  <!-- Fork: left of wordmark, tines top + handle merging into M -->
  <g fill="#3FC0F0">
    <rect x="8"  y="8"  width="5" height="22" rx="2.5"/>
    <rect x="18" y="8"  width="5" height="22" rx="2.5"/>
    <rect x="28" y="8"  width="5" height="22" rx="2.5"/>
    <rect x="13" y="28" width="15" height="28" rx="7.5"/>
  </g>
  <!-- Wordmark -->
  <text x="48" y="54"
    font-family="Pacifico, 'Brush Script MT', cursive"
    font-size="48" fill="#3FC0F0" letter-spacing="-1">Massilia</text>
  <!-- Gold compass dot (sits above second 's', approx x=190) -->
  <circle cx="196" cy="16" r="11" fill="#F5B800"/>
  <polygon points="196,8 199.5,16 196,13.5 192.5,16" fill="white"/>
  <polygon points="196,24 192.5,16 196,18.5 199.5,16" fill="white" opacity="0.55"/>
  <!-- Subtitle -->
  <text x="48" y="70"
    font-family="'Nunito', Arial, sans-serif"
    font-size="11" font-weight="900" fill="#F5B800" letter-spacing="3.5">PANIS · PASTIS · FOUGASSE</text>
</svg>
"""

LOGO_FOOTER = """
<svg viewBox="0 0 380 72" xmlns="http://www.w3.org/2000/svg" style="height:44px;width:auto;display:inline-block;">
  <g fill="#3FC0F0">
    <rect x="8"  y="8"  width="5" height="22" rx="2.5"/>
    <rect x="18" y="8"  width="5" height="22" rx="2.5"/>
    <rect x="28" y="8"  width="5" height="22" rx="2.5"/>
    <rect x="13" y="28" width="15" height="28" rx="7.5"/>
  </g>
  <text x="48" y="54"
    font-family="Pacifico, 'Brush Script MT', cursive"
    font-size="48" fill="#3FC0F0" letter-spacing="-1">Massilia</text>
  <circle cx="196" cy="16" r="11" fill="#F5B800"/>
  <polygon points="196,8 199.5,16 196,13.5 192.5,16" fill="white"/>
  <polygon points="196,24 192.5,16 196,18.5 199.5,16" fill="white" opacity="0.55"/>
  <text x="48" y="70"
    font-family="'Nunito', Arial, sans-serif"
    font-size="11" font-weight="900" fill="#F5B800" letter-spacing="3.5">PANIS · PASTIS · FOUGASSE</text>
</svg>
"""

# ════════════════════════════════════════════════════════════════════════════
# CSS — readability-first: every text element has a deliberate colour
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,700&display=swap');

:root {
  --blue:   #3FC0F0;
  --yellow: #F5B800;
  --cream:  #FFF8EE;
  --dark:   #1A2540;
  --green:  #18B07A;
  --muted:  #5A6680;   /* contrast-checked against white: 5.3:1 ✓ */
  --card:   #FFFFFF;
}

*, *::before, *::after { box-sizing: border-box; }

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
[data-testid="stHeader"] { display: none !important; }

/* ── NAV ── */
.topbar {
  position: sticky; top: 0; z-index: 200;
  background: #fff;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.55rem 2rem;
  border-bottom: 2px solid rgba(63,192,240,0.13);
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.nav-pill {
  background: var(--blue); color: #fff;
  border-radius: 50px; padding: 0.4rem 1.1rem;
  font-weight: 800; font-size: 0.85rem;
  cursor: pointer; border: none; font-family: 'Nunito',sans-serif;
}
.nav-pill.ghost {
  background: transparent; color: var(--dark);
  border: 1.5px solid rgba(26,37,64,0.2);
}

/* ── MAP HERO ── */
.map-hero { position: relative; width: 100%; }
.map-frame { width: 100%; height: 440px; border: none; display: block; }
.map-overlay-card {
  position: absolute; top: 16px; left: 16px;
  background: #fff; border-radius: 20px;
  padding: 1.1rem 1.3rem; max-width: 288px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18); z-index: 10;
}
.map-overlay-card h3 {
  font-family: 'Pacifico',cursive; font-size: 1.1rem;
  color: var(--dark); line-height: 1.25; margin-bottom: 0.3rem;
}
.map-overlay-card h3 em { color: var(--blue); font-style: normal; }
.map-overlay-card p { font-size: 0.8rem; color: var(--muted); line-height: 1.5; margin-bottom: 0.8rem; }
.filter-pills { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.fpill {
  border-radius: 50px; padding: 0.28rem 0.8rem;
  font-size: 0.75rem; font-weight: 800; border: none;
  cursor: pointer; font-family: 'Nunito',sans-serif;
}
.fpill-all      { background: var(--dark);  color: #fff; }
.fpill-panisse  { background: #FFF0B3;      color: #6B4A00; }
.fpill-pastis   { background: #CBF0FF;      color: #083C52; }
.fpill-fougasse { background: #C6F7E4;      color: #0A3D28; }

.map-bar {
  background: #fff; padding: 0.6rem 2rem;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid #EBEBEB;
}
.map-bar span { font-size: 0.82rem; color: var(--muted); }
.map-bar b    { color: var(--dark); }
.map-bar a    { font-size: 0.82rem; font-weight: 800; color: var(--blue); text-decoration: none; }

/* ── SECTION WRAPPERS ── */
.sec { padding: 2rem 2rem 0; }
.sec-hdr {
  display: flex; align-items: baseline; justify-content: space-between;
  margin-bottom: 1.1rem;
}
.sec-hdr h2 { font-size: 1.4rem; font-weight: 900; color: var(--dark); }
.sec-hdr h2 em { color: var(--blue); font-style: normal; }
.sec-hdr .see-all { font-size: 0.83rem; font-weight: 800; color: var(--blue); cursor: pointer; }

/* ── HORIZONTAL SCROLL CARDS — UNIFORM SIZE ── */
.cards-scroll {
  display: flex; gap: 1rem; overflow-x: auto;
  padding-bottom: 1rem; -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.cards-scroll::-webkit-scrollbar { display: none; }
.spot-card {
  flex: 0 0 210px;          /* ← fixed width, every card identical */
  border-radius: 20px; overflow: hidden;
  background: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.2s; cursor: pointer;
}
.spot-card:hover { transform: translateY(-4px); }
.spot-card-img {
  width: 210px; height: 140px;   /* ← fixed dimensions = consistent grid */
  object-fit: cover; display: block; flex-shrink: 0;
}
.spot-card-body { padding: 0.8rem 0.95rem 0.9rem; }
.spot-card-cat {
  font-size: 0.68rem; font-weight: 900;
  letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.25rem;
}
.c-panisse  { color: #8A6000; }
.c-pastis   { color: #0A6A9A; }
.c-fougasse { color: #0A7050; }
.c-other    { color: #A0304A; }
.spot-card-name { font-weight: 900; font-size: 0.96rem; color: var(--dark); line-height: 1.2; margin-bottom: 0.25rem; }
.spot-card-vibe { font-size: 0.76rem; color: var(--muted); line-height: 1.4; }
.spot-card-foot {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 0.55rem; padding-top: 0.55rem; border-top: 1px solid #F0F0EA;
}
.price  { font-size: 0.78rem; font-weight: 900; color: var(--green); }
.rating { font-size: 0.78rem; font-weight: 800; color: #C08B00; }

/* ══════════════════════════════════════
   PERSONALISED PROFILE — hero feature
══════════════════════════════════════ */
.profile-wrap {
  margin: 2rem 2rem 0;
  border-radius: 28px; overflow: hidden;
  box-shadow: 0 8px 40px rgba(63,192,240,0.18);
  border: 2px solid rgba(63,192,240,0.18);
}
/* dark header banner */
.profile-banner {
  background: linear-gradient(135deg, #1A2540 0%, #0D3A5C 100%);
  padding: 1.8rem 2.2rem;
  display: flex; align-items: flex-start; gap: 1.2rem;
}
.profile-avatar-ring {
  width: 64px; height: 64px; border-radius: 50%;
  border: 3px solid rgba(63,192,240,0.5);
  background: rgba(63,192,240,0.15);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; flex-shrink: 0;
}
.profile-banner-text {}
.profile-eyebrow {
  font-size: 0.68rem; font-weight: 900; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--yellow); margin-bottom: 0.25rem;
}
.profile-headline {
  font-family: 'Pacifico', cursive;
  font-size: 1.55rem; color: #fff; line-height: 1.15; margin-bottom: 0.3rem;
}
.profile-subline { font-size: 0.83rem; color: rgba(255,255,255,0.65); line-height: 1.5; margin-bottom: 0.7rem; }
.profile-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.pbadge {
  background: rgba(63,192,240,0.18); color: #7DD9F7;
  border: 1px solid rgba(63,192,240,0.35);
  border-radius: 50px; padding: 0.22rem 0.8rem;
  font-size: 0.72rem; font-weight: 800;
}

/* white body of the profile card */
.profile-body {
  background: #fff; padding: 1.8rem 2.2rem 0.5rem;
}
.profile-body-intro { margin-bottom: 1.5rem; }
.profile-body-intro h3 { font-size: 1.05rem; font-weight: 900; color: var(--dark); margin-bottom: 0.2rem; }
.profile-body-intro p  { font-size: 0.85rem; color: var(--muted); line-height: 1.5; }

/* labels above each select — readable dark text on white */
.pf-label {
  font-size: 0.72rem; font-weight: 900;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 0.3rem; margin-top: 0.1rem;
}

/* Streamlit selects inside white profile body → dark text */
.profile-body div[data-baseweb="select"] > div {
  background: #F5F7FA !important;
  border-color: #DDE3EE !important;
  color: var(--dark) !important;
  border-radius: 12px !important;
  font-family: 'Nunito', sans-serif !important;
}
.profile-body div[data-baseweb="select"] span { color: var(--dark) !important; }
.profile-body div[data-baseweb="select"] svg  { color: var(--muted) !important; }
.profile-body textarea {
  background: #F5F7FA !important; color: var(--dark) !important;
  border-color: #DDE3EE !important; border-radius: 12px !important;
}
.profile-body textarea::placeholder { color: #AAB4C4 !important; }
.profile-body [data-testid="stSlider"] div[role="slider"] { background: var(--blue) !important; }
.profile-body [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

/* CTA row */
.profile-cta { padding: 1rem 2.2rem 1.8rem; background: #fff; }
.profile-cta div.stButton > button {
  background: var(--blue)  !important;
  color: #fff              !important;
  font-size: 1.05rem       !important;
  padding: 0.75rem 2rem    !important;
  border-radius: 50px      !important;
  border: none             !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900         !important;
  width: 100%              !important;
  transition: all 0.2s     !important;
}
.profile-cta div.stButton > button:hover {
  background: var(--yellow) !important;
  color: var(--dark)        !important;
}

/* ── RESULT BOX ── */
.result-wrap { padding: 1rem 2rem; }
.result-box {
  background: #fff; border-radius: 20px;
  padding: 1.6rem 1.8rem;
  border-left: 5px solid var(--blue);
  box-shadow: 0 4px 24px rgba(63,192,240,0.1);
  font-size: 0.95rem; line-height: 1.8; color: var(--dark);
}
.result-box h3 {
  font-family: 'Pacifico',cursive; font-size: 1.15rem;
  color: var(--blue); margin-bottom: 0.7rem;
}

/* ── VIBE GRID — uniform square tiles ── */
.vibes-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.8rem;
}
.vibe-tile {
  border-radius: 18px; overflow: hidden;
  aspect-ratio: 1 / 1; position: relative; cursor: pointer;
}
.vibe-tile img {
  width: 100%; height: 100%;
  object-fit: cover; display: block; transition: transform 0.3s;
}
.vibe-tile:hover img { transform: scale(1.07); }
.vibe-overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: rgba(26,37,64,0.4);
  color: #fff; text-align: center; padding: 0.5rem;
  transition: background 0.2s;
}
.vibe-tile:hover .vibe-overlay { background: rgba(63,192,240,0.6); }
.vibe-emoji { font-size: 1.55rem; margin-bottom: 0.2rem; }
.vibe-label { font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.07em; }

/* ── COMMUNITY ── */
.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}
.community-card {
  background: #fff; border-radius: 18px;
  padding: 1.1rem 1.2rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.cc-blue   { border-left: 4px solid var(--blue);   }
.cc-yellow { border-left: 4px solid var(--yellow); }
.cc-green  { border-left: 4px solid var(--green);  }
.cc-avatar { width: 36px; height: 36px; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.cc-avatar img { width: 100%; height: 100%; object-fit: cover; }
.cc-name   { font-weight: 800; font-size: 0.88rem; color: var(--dark); }
.cc-role   { font-size: 0.72rem; color: var(--muted); }
.cc-quote  { font-size: 0.88rem; line-height: 1.55; color: var(--dark); margin: 0.7rem 0 0.5rem; font-style: italic; }
.cc-tag    {
  display: inline-block; background: rgba(63,192,240,0.1);
  color: #0A6A9A; border-radius: 50px;
  padding: 0.2rem 0.7rem; font-size: 0.72rem; font-weight: 800;
}

/* ── SHARE FORM — all on white bg → dark text ── */
.share-sec { padding: 2rem 2rem 0; }
.share-sec div[data-baseweb="select"] > div {
  background: #fff !important; border-color: #DDE3EE !important;
  color: var(--dark) !important; border-radius: 12px !important;
}
.share-sec div[data-baseweb="select"] span { color: var(--dark) !important; }
.share-sec div[data-baseweb="input"]  input {
  background: #fff !important; color: var(--dark) !important;
  border-color: #DDE3EE !important;
}
.share-sec textarea {
  background: #fff !important; color: var(--dark) !important;
  border-color: #DDE3EE !important;
}
.share-sec div.stButton > button {
  background: var(--yellow) !important; color: var(--dark) !important;
  font-weight: 900 !important;
}

/* ── NEWSLETTER ── */
.newsletter {
  margin: 2rem 2rem 0;
  background: var(--blue); border-radius: 24px;
  padding: 2.2rem 2rem; text-align: center;
}
.newsletter h2 {
  font-family: 'Pacifico',cursive; font-size: 1.7rem;
  color: #fff; margin-bottom: 0.4rem;
}
.newsletter p { font-size: 0.9rem; color: rgba(255,255,255,0.9); margin-bottom: 1.2rem; line-height: 1.6; }

/* ── FOOTER ── */
.footer { background: var(--dark); padding: 2.2rem 2rem 1.5rem; text-align: center; margin-top: 2rem; }

/* ── GLOBAL STREAMLIT OVERRIDES ── */
div.stButton > button {
  background: var(--yellow) !important; color: var(--dark) !important;
  font-family: 'Nunito',sans-serif !important; font-weight: 900 !important;
  font-size: 0.95rem !important; border-radius: 50px !important;
  border: none !important; padding: 0.6rem 1.8rem !important;
  width: 100% !important; transition: all 0.2s !important;
}
div.stButton > button:hover { background: var(--dark) !important; color: #fff !important; }
div[data-baseweb="select"] > div { border-radius: 12px !important; font-family: 'Nunito',sans-serif !important; }
[data-testid="stForm"]  { background: transparent !important; border: none !important; padding: 0 !important; }
div[data-testid="column"] { padding: 0 0.35rem !important; }
.stTabs [data-baseweb="tab-list"] { background: #fff; border-radius: 50px; padding: 4px; gap: 2px; }
.stTabs [data-baseweb="tab"] { border-radius: 50px !important; font-family: 'Nunito',sans-serif !important; font-weight: 800 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "recs" not in st.session_state:
    st.session_state.recs = None

# All images use the same aspect ratio source → consistent card height
SPOTS = [
    {"name":"Chez Étienne",          "category":"Panisse",  "vibe":"Noailles · cash only, locals",  "price":"€",   "rating":"4.9",
     "img":"https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=420&h=280&fit=crop&q=80"},
    {"name":"Bar de la Marine",       "category":"Pastis",   "vibe":"Vieux-Port · Pagnol vibes",     "price":"€€",  "rating":"4.8",
     "img":"https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=420&h=280&fit=crop&q=80"},
    {"name":"Fougasserie du Panier",  "category":"Fougasse", "vibe":"Le Panier · hidden bakery",      "price":"€",   "rating":"4.7",
     "img":"https://images.unsplash.com/photo-1509440159596-0249088772ff?w=420&h=280&fit=crop&q=80"},
    {"name":"Café Populaire",         "category":"Pastis",   "vibe":"Cours Julien · boho terrace",   "price":"€€",  "rating":"4.6",
     "img":"https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=420&h=280&fit=crop&q=80"},
    {"name":"L'Épicerie du Midi",     "category":"Panisse",  "vibe":"Noailles · marché vibe",        "price":"€",   "rating":"4.5",
     "img":"https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=420&h=280&fit=crop&q=80"},
    {"name":"Le Trolleybus",          "category":"Pastis",   "vibe":"Vieux-Port · late night DJ",    "price":"€€",  "rating":"4.4",
     "img":"https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?w=420&h=280&fit=crop&q=80"},
]
CAT_C = {"Panisse":"c-panisse","Pastis":"c-pastis","Fougasse":"c-fougasse"}

# ══════════════════════════════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <div>{LOGO_NAV}</div>
  <div style="display:flex;gap:0.5rem;align-items:center;">
    <button class="nav-pill ghost">Sign in</button>
    <button class="nav-pill">Explore 🌊</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1 ── MAP FIRST — full-width hero
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="map-hero">
  <div class="map-overlay-card">
    <h3>Find the best spots in <em>Marseille</em></h3>
    <p>Authentic addresses hand-picked by students & locals — zero tourist traps.</p>
    <div class="filter-pills">
      <span class="fpill fpill-all">All</span>
      <span class="fpill fpill-panisse">🍟 Panisse</span>
      <span class="fpill fpill-pastis">🥛 Pastis</span>
      <span class="fpill fpill-fougasse">🫓 Fougasse</span>
    </div>
  </div>
  <iframe class="map-frame"
    src="https://www.openstreetmap.org/export/embed.html?bbox=5.342%2C43.281%2C5.408%2C43.311&layer=mapnik"
    title="Marseille food map" loading="lazy">
  </iframe>
</div>
<div class="map-bar">
  <span>📍 Showing <b>Marseille centre</b> — 12 spots nearby</span>
  <a href="https://www.openstreetmap.org/?mlat=43.2965&mlon=5.3698#map=14/43.2965/5.3698" target="_blank">Full map ↗</a>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2 ── HOT RIGHT NOW — uniform scroll cards
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec">
  <div class="sec-hdr">
    <h2>🔥 Hot right <em>now</em></h2>
    <span class="see-all">See all →</span>
  </div>
  <div class="cards-scroll">
""", unsafe_allow_html=True)

for s in SPOTS:
    cc = CAT_C.get(s["category"], "c-other")
    st.markdown(f"""
    <div class="spot-card">
      <img class="spot-card-img" src="{s['img']}" alt="{s['name']}" loading="lazy"/>
      <div class="spot-card-body">
        <div class="spot-card-cat {cc}">{s['category']}</div>
        <div class="spot-card-name">{s['name']}</div>
        <div class="spot-card-vibe">{s['vibe']}</div>
        <div class="spot-card-foot">
          <span class="price">{s['price']}</span>
          <span class="rating">★ {s['rating']}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3 ── PERSONALISED PROFILE  ← highlighted as THE core feature
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="profile-wrap">
  <!-- dark header banner -->
  <div class="profile-banner">
    <div class="profile-avatar-ring">🧑‍🎓</div>
    <div class="profile-banner-text">
      <div class="profile-eyebrow">✨ Your personalised profile</div>
      <div class="profile-headline">Your vibe,<br>your Marseille</div>
      <div class="profile-subline">
        Tell us your mood, budget and who you're with —<br>
        our AI finds your perfect spot in seconds.
      </div>
      <div class="profile-badges">
        <span class="pbadge">📍 Location-aware</span>
        <span class="pbadge">💶 Budget-smart</span>
        <span class="pbadge">🎭 Mood-based</span>
        <span class="pbadge">✨ AI-powered</span>
      </div>
    </div>
  </div>
  <!-- white form body -->
  <div class="profile-body">
    <div class="profile-body-intro">
      <h3>What are you in the mood for right now?</h3>
      <p>Fill in your profile — the more you tell us, the better your recommendations.</p>
    </div>
""", unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    st.markdown('<div class="pf-label">🎭 Your mood</div>', unsafe_allow_html=True)
    mood = st.selectbox("mood", ["😎 Chill apéro","🌅 Sunset spot","🎉 Going out","☀️ Beach lunch","🤫 Hidden gem","💸 Super broke","🍽️ Proper dinner","🧘 Solo & quiet"], label_visibility="collapsed", key="mood")
with r1c2:
    st.markdown('<div class="pf-label">👥 Who are you with?</div>', unsafe_allow_html=True)
    group = st.selectbox("group", ["Friends","Solo","Date night","Family","Backpackers"], label_visibility="collapsed", key="group")
with r1c3:
    st.markdown('<div class="pf-label">🎵 Music vibe</div>', unsafe_allow_html=True)
    music = st.selectbox("music", ["Electro / House","No preference","Jazz / Soul","Hip-hop","Reggae","Acoustic","Quiet"], label_visibility="collapsed", key="music")

r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    st.markdown('<div class="pf-label">💶 Max budget / person</div>', unsafe_allow_html=True)
    budget = st.slider("budget", 5, 60, 15, step=5, label_visibility="collapsed", key="budget", format="€%d")
    st.caption(f"Up to **€{budget}** per person")
with r2c2:
    st.markdown('<div class="pf-label">🕐 Time of day</div>', unsafe_allow_html=True)
    time_day = st.selectbox("time", ["Morning","Lunch","Afternoon","Apéro (5–8pm)","Dinner","Late night"], label_visibility="collapsed", key="time_day")
with r2c3:
    st.markdown('<div class="pf-label">📍 Neighbourhood</div>', unsafe_allow_html=True)
    area = st.selectbox("area", ["Anywhere","Vieux-Port","Cours Julien","Noailles","Endoume","Pointe Rouge","Le Panier"], label_visibility="collapsed", key="area")

st.markdown('<div class="pf-label" style="margin-top:0.6rem;">✏️ Anything else you want?</div>', unsafe_allow_html=True)
freetext = st.text_area("extra", placeholder="e.g. sea-view terrace, cheap pastis, avoid tourists, need wifi…", height=70, label_visibility="collapsed", key="freetext")

st.markdown("</div>", unsafe_allow_html=True)  # close profile-body

st.markdown('<div class="profile-cta">', unsafe_allow_html=True)
go = st.button("✨ Find my perfect spot — it's free")
st.markdown("</div></div>", unsafe_allow_html=True)  # close cta + profile-wrap

# ── AI call ────────────────────────────────────────────────────────────────────
if go:
    prompt = f"""You are Massilia, an AI guide for authentic Marseille food & lifestyle.
Give exactly 3 personalized spot recommendations.

User profile: mood={mood}, group={group}, music={music}, budget=€{budget}/person, time={time_day}, area={area}
Notes: {freetext or 'none'}

Focus: panisse spots, pastis bars, fougasse bakeries, sunset bars, beach restaurants, hidden gems.

For each spot:
**[Name]** · [neighbourhood]
🍽️ Order: ...
💶 Price: ...
🌊 Vibe: ...
🔑 Tip: ...

Tone: warm, fun, local — like a Marseillais mate texting you. Use occasional French naturally. Short sign-off at end."""

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
    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-box">
      <h3>🌊 Your spots, just for you</h3>
      {st.session_state.recs.replace(chr(10), "<br>")}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4 ── MOOD VIBES GRID — uniform square tiles
# ══════════════════════════════════════════════════════════════════════════════
VIBES = [
    ("https://images.unsplash.com/photo-1566937169390-b55a2639aad3?w=300&h=300&fit=crop&q=75","🌅","Sunset Apéro"),
    ("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=300&h=300&fit=crop&q=75","🍟","Cheap Eats"),
    ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&h=300&fit=crop&q=75","🏖️","Beach Day"),
    ("https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?w=300&h=300&fit=crop&q=75","🎉","Night Out"),
    ("https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=300&h=300&fit=crop&q=75","☕","Chill Café"),
    ("https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=300&h=300&fit=crop&q=75","👯","With Friends"),
    ("https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=300&h=300&fit=crop&q=75","🤫","Hidden Gem"),
    ("https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=300&h=300&fit=crop&q=75","🍽️","Proper Dinner"),
]

st.markdown("""
<div class="sec">
  <div class="sec-hdr">
    <h2>Pick your <em>vibe</em></h2>
    <span class="see-all">Browse all →</span>
  </div>
  <div class="vibes-grid">
""", unsafe_allow_html=True)

for img, emoji, label in VIBES:
    st.markdown(f"""
    <div class="vibe-tile">
      <img src="{img}" alt="{label}" loading="lazy"/>
      <div class="vibe-overlay">
        <div class="vibe-emoji">{emoji}</div>
        <div class="vibe-label">{label}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5 ── COMMUNITY VOICES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec">
  <div class="sec-hdr" style="margin-bottom:1rem;">
    <h2>🌊 Real <em>locals</em> say</h2>
    <span class="see-all">All stories →</span>
  </div>
  <div class="community-grid">
""", unsafe_allow_html=True)

POSTS = [
    {"author":"Julien M.","role":"Design student, AMU","avatar":"https://i.pravatar.cc/80?img=7",
     "quote":"Best way to see the city is at 6am when the sun hits the Mucem. The whole city wakes up from a dream. Don't skip the rooftop!",
     "tag":"Mucem at sunrise","accent":"cc-blue"},
    {"author":"Anaëlis R.","role":"New here from Lyon","avatar":"https://i.pravatar.cc/80?img=47",
     "quote":"Can't share the bouillabaisse recipe, but I'll tell you where to find the freshest rouget at the Noailles morning market.",
     "tag":"Noailles market","accent":"cc-yellow"},
    {"author":"Marco S.","role":"Graphic designer, local","avatar":"https://i.pravatar.cc/80?img=60",
     "quote":"The street art scene changes every week. New gallery behind the metro every month. This city never stops.",
     "tag":"Street art tour","accent":"cc-green"},
]

for p in POSTS:
    st.markdown(f"""
    <div class="community-card {p['accent']}">
      <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.6rem;">
        <div class="cc-avatar"><img src="{p['avatar']}" alt="{p['author']}" loading="lazy"/></div>
        <div>
          <div class="cc-name">{p['author']}</div>
          <div class="cc-role">{p['role']}</div>
        </div>
      </div>
      <div class="cc-quote">"{p['quote']}"</div>
      <span class="cc-tag">📍 {p['tag']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6 ── SHARE A SPOT — white bg, dark readable text
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="share-sec">
  <div class="sec-hdr" style="margin-bottom:1rem;">
    <h2>✍️ Share your <em>hidden gem</em></h2>
  </div>
""", unsafe_allow_html=True)

with st.form("share_form", clear_on_submit=True):
    fs1, fs2 = st.columns(2)
    with fs1:
        s_name = st.text_input("Spot name *", placeholder="e.g. Chez Jeannot")
        s_vibe = st.text_input("Neighbourhood / vibe", placeholder="e.g. Le Panier, cash only")
    with fs2:
        s_cat   = st.selectbox("Type", ["Panisse 🍟","Pastis 🥛","Fougasse 🫓","Other 🍽️"])
        s_price = st.selectbox("Price", ["€ under €10","€€ €10–20","€€€ €20+"])
    s_tip    = st.text_area("Your tip *", placeholder="What to order, best time, secret trick…", height=80)
    s_author = st.text_input("Your name", placeholder="e.g. Théo, étudiant")
    sub = st.form_submit_button("🌊 Add to the map")
    if sub:
        if s_name and s_tip:
            st.success(f"🎉 Merci ! **{s_name}** is now on the Massilia map.")
        else:
            st.warning("Please fill in at least the spot name and your tip.")

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7 ── NEWSLETTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="newsletter">
  <h2>The insider's newsletter.</h2>
  <p>No spam. Only secret openings, local events,<br>and the best places to hide from tourists this summer.</p>
  <div style="display:flex;gap:0.6rem;max-width:420px;margin:0 auto;flex-wrap:wrap;justify-content:center;">
    <input type="email" placeholder="Your email address"
      style="border-radius:50px;border:none;padding:0.65rem 1.3rem;
             font-family:Nunito,sans-serif;font-size:0.9rem;flex:1;min-width:190px;
             outline:none;color:#1A2540;"/>
    <button style="background:#F5B800;color:#1A2540;border:none;border-radius:50px;
                   padding:0.65rem 1.5rem;font-family:Nunito,sans-serif;font-weight:900;
                   font-size:0.9rem;cursor:pointer;white-space:nowrap;">Subscribe</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  <div style="display:flex;justify-content:center;margin-bottom:0.5rem;">{LOGO_FOOTER}</div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-style:italic;margin:0.4rem 0 1.2rem;">
    Pas fâché avec le plaisir 🌊
  </div>
  <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1.2rem;">
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Explore</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Map</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Community</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Contact</a>
  </div>
  <div style="font-size:0.72rem;color:rgba(255,255,255,0.25);">© 2025 Massilia · Panis · Pastis · Fougasse</div>
</div>
""", unsafe_allow_html=True)
