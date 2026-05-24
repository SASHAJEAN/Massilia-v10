import streamlit as st
import anthropic

st.set_page_config(
    page_title="Massilia – Pas fâché avec le plaisir",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Brand CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap');

:root {
    --blue:   #3FC0F0;
    --yellow: #F5B800;
    --cream:  #FFF8EE;
    --dark:   #1A2540;
    --card:   #FFFFFF;
    --muted:  #6B7A99;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main > div {
    background-color: var(--cream) !important;
    font-family: 'Nunito', sans-serif;
    padding-top: 0 !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"] { display: none !important; }

/* ── NAV ── */
.nav {
    background: white;
    border-bottom: 1px solid rgba(63,192,240,0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 2.5rem;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    font-family: 'Pacifico', cursive;
    font-size: 1.6rem;
    color: var(--blue);
    text-decoration: none;
}
.nav-links { display: flex; gap: 2rem; }
.nav-links a {
    color: var(--dark);
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    opacity: 0.7;
    letter-spacing: 0.05em;
}
.nav-links a:hover { opacity: 1; color: var(--blue); }
.nav-cta {
    background: var(--blue);
    color: white !important;
    border-radius: 50px;
    padding: 0.45rem 1.4rem;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    width: 100%;
    min-height: 520px;
    overflow: hidden;
    display: flex;
    align-items: center;
}
.hero-bg {
    position: absolute; inset: 0;
    background: url('https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1400&q=80') center/cover no-repeat;
    filter: brightness(0.55);
}
.hero-content {
    position: relative;
    z-index: 2;
    max-width: 640px;
    padding: 3.5rem 3rem 3.5rem 4rem;
    color: white;
}
.hero-tagline-badge {
    background: var(--yellow);
    color: var(--dark);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    border-radius: 50px;
    display: inline-block;
    padding: 0.3rem 1rem;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Pacifico', cursive;
    font-size: 3.4rem;
    line-height: 1.1;
    margin-bottom: 0.8rem;
    color: white;
}
.hero-title span { color: var(--yellow); font-style: italic; }
.hero-sub {
    font-size: 1.05rem;
    line-height: 1.65;
    opacity: 0.92;
    margin-bottom: 2rem;
    max-width: 480px;
}
.hero-btn {
    background: var(--blue);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.75rem 2rem;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
}
.hero-btn:hover { background: var(--yellow); color: var(--dark); }

/* ── PHOTO STRIP ── */
.photo-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding: 2rem 3rem;
}
.photo-strip-item {
    border-radius: 16px;
    overflow: hidden;
    aspect-ratio: 4/3;
    position: relative;
}
.photo-strip-item img {
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
    display: block;
}
.photo-strip-item:hover img { transform: scale(1.06); }
.photo-strip-item .label {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(0deg, rgba(26,37,64,0.85) 0%, transparent 100%);
    color: white;
    padding: 1rem 0.9rem 0.7rem;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.photo-strip-item .label span {
    display: block;
    font-weight: 400;
    font-size: 0.75rem;
    opacity: 0.8;
    text-transform: none;
    letter-spacing: 0;
    margin-top: 1px;
}

/* ── SECTION ── */
.section {
    padding: 2.5rem 3rem;
}
.section-header {
    margin-bottom: 1.5rem;
}
.section-eyebrow {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 0.4rem;
}
.section-title {
    font-family: 'Nunito', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--dark);
    line-height: 1.15;
    margin: 0;
}
.section-title em {
    font-style: italic;
    color: var(--blue);
}

/* ── MAP SECTION ── */
.map-wrapper {
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid rgba(63,192,240,0.2);
    box-shadow: 0 8px 40px rgba(63,192,240,0.12);
    height: 420px;
}
.map-wrapper iframe {
    width: 100%;
    height: 100%;
    border: none;
    display: block;
}
.map-pins-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}
.pin-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: white;
    border: 1.5px solid rgba(63,192,240,0.25);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--dark);
}
.pin-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── DISCOVER FORM ── */
.form-card {
    background: white;
    border-radius: 20px;
    padding: 2rem 2.2rem;
    border: 1px solid rgba(63,192,240,0.15);
    box-shadow: 0 4px 24px rgba(0,0,0,0.05);
}
.form-label {
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.mood-pill {
    background: rgba(63,192,240,0.1);
    color: var(--blue);
    border: 1.5px solid rgba(63,192,240,0.3);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.mood-pill.active, .mood-pill:hover {
    background: var(--blue);
    color: white;
    border-color: var(--blue);
}

/* ── RESULT ── */
.result-card {
    background: white;
    border-radius: 18px;
    padding: 1.8rem 2rem;
    border-left: 5px solid var(--blue);
    box-shadow: 0 4px 24px rgba(63,192,240,0.1);
    margin-top: 1.2rem;
    font-size: 0.97rem;
    line-height: 1.75;
    color: var(--dark);
}
.result-card h3 {
    font-family: 'Pacifico', cursive;
    font-size: 1.3rem;
    color: var(--blue);
    margin-bottom: 0.8rem;
}

/* ── COMMUNITY ── */
.spot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
}
.spot-card {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    border-top: 4px solid var(--yellow);
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: transform 0.2s;
}
.spot-card:hover { transform: translateY(-3px); }
.spot-name { font-weight: 800; font-size: 1rem; color: var(--dark); }
.spot-cat { color: var(--yellow); font-size: 0.85rem; font-weight: 700; }
.spot-meta { font-size: 0.8rem; color: var(--muted); margin-top: 0.3rem; }
.spot-tip { font-size: 0.9rem; margin-top: 0.5rem; color: var(--dark); line-height: 1.55; }
.spot-author {
    margin-top: 0.7rem;
    font-size: 0.78rem;
    color: var(--muted);
    font-style: italic;
}

/* ── NEWSLETTER BANNER ── */
.newsletter-band {
    background: var(--blue);
    border-radius: 24px;
    margin: 0 3rem 3rem;
    padding: 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    flex-wrap: wrap;
}
.newsletter-band h2 {
    font-family: 'Pacifico', cursive;
    font-size: 2rem;
    color: white;
    margin: 0 0 0.4rem;
}
.newsletter-band p { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin: 0; }

/* ── STREAMLIT OVERRIDES ── */
div.stButton > button {
    background: var(--blue) !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.55rem 1.8rem !important;
    transition: all 0.2s !important;
    width: 100%;
}
div.stButton > button:hover {
    background: var(--yellow) !important;
    color: var(--dark) !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    background: white !important;
}
textarea { border-radius: 10px !important; font-family: 'Nunito', sans-serif !important; }
button[data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
[data-testid="stSlider"] div[role="slider"] { background: var(--blue) !important; }
[data-testid="stForm"] { background: transparent !important; border: none !important; }
.stTabs [data-baseweb="tab-list"] { background: white; border-radius: 50px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 50px !important; }
div[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "recs" not in st.session_state:
    st.session_state.recs = None
if "community_spots" not in st.session_state:
    st.session_state.community_spots = [
        {"name": "Chez Étienne", "category": "Panisse 🍟", "vibe": "Noailles · locals only, cash", "price": "€", "tip": "Order the panisse nature and eat standing at the counter – perfect before midi.", "author": "Lucas, étudiant AMU", "lat": 43.2965, "lng": 5.3698},
        {"name": "Bar de la Marine", "category": "Pastis 🥛", "vibe": "Vieux-Port · Marcel Pagnol vibes", "price": "€€", "tip": "Grab a table outside at golden hour. Ricard + olives = la vie marseillaise.", "author": "Sofia, backpacker", "lat": 43.2951, "lng": 5.3687},
        {"name": "La Fougasserie du Panier", "category": "Fougasse 🫓", "vibe": "Le Panier · hidden bakery", "price": "€", "tip": "Anchovy & olive fougasse at 8h before the tourists arrive. Chef's kiss.", "author": "Théo, jeune actif", "lat": 43.2985, "lng": 5.3703},
        {"name": "Café Populaire", "category": "Pastis 🥛", "vibe": "Cours Julien · boho terrace", "price": "€€", "tip": "Sunday brunch then stay for the afternoon pastis session with a great playlist.", "author": "Anaïs, freelance", "lat": 43.2928, "lng": 5.3782},
        {"name": "L'Épicerie du Midi", "category": "Panisse 🍟", "vibe": "Noailles · marché vibe", "price": "€", "tip": "Hot panisse in a paper cone straight from the fryer – eat it walking.", "author": "Marco, backpacker", "lat": 43.2960, "lng": 5.3742},
        {"name": "La Virgule", "category": "Fougasse 🫓", "vibe": "La Plaine · student favourite", "price": "€", "tip": "Best fougasse au fromage in town, open until late on weekdays.", "author": "Julie, étudiante", "lat": 43.2915, "lng": 5.3795},
    ]

# ══════════════════════════════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<nav class="nav">
  <a class="nav-logo" href="#">Massilia</a>
  <div class="nav-links">
    <a href="#">Explore</a>
    <a href="#">Map</a>
    <a href="#">Community</a>
  </div>
  <a href="#" class="nav-links"><a class="nav-links nav-cta" href="#">Get Started</a></a>
</nav>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-tagline-badge">Panis · Pastis · Fougasse</div>
    <h1 class="hero-title">Pas fâché avec<br><span>le plaisir !</span></h1>
    <p class="hero-sub">Craft your Marseille experience. AI-powered recommendations for authentic spots — hidden gems, cheap pastis, golden-hour terrasses.</p>
    <a href="#" class="hero-btn">🌊 Explore the city</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PHOTO STRIP — real Unsplash photos of Marseille
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="photo-strip">
  <div class="photo-strip-item">
    <img src="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80" alt="Vieux-Port Marseille" loading="lazy"/>
    <div class="label">Vieux-Port<span>The iconic old harbour</span></div>
  </div>
  <div class="photo-strip-item">
    <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80" alt="Panisse" loading="lazy"/>
    <div class="label">Panisse<span>Crispy chickpea fritters</span></div>
  </div>
  <div class="photo-strip-item">
    <img src="https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=600&q=80" alt="Pastis apéro" loading="lazy"/>
    <div class="label">Pastis time<span>L'apéro marseillais</span></div>
  </div>
  <div class="photo-strip-item">
    <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80" alt="Calanques" loading="lazy"/>
    <div class="label">Les Calanques<span>Secret swimming spots</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT: MAP + DISCOVER FORM (side by side)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section">', unsafe_allow_html=True)

col_map, col_form = st.columns([1.1, 0.9], gap="large")

with col_map:
    st.markdown("""
    <div class="section-header">
      <div class="section-eyebrow">The Districts</div>
      <h2 class="section-title">Find the best<br><em>addresses on the map</em></h2>
    </div>
    """, unsafe_allow_html=True)

    # OpenStreetMap embed centred on Marseille with key spots
    st.markdown("""
    <div class="map-wrapper">
      <iframe
        src="https://www.openstreetmap.org/export/embed.html?bbox=5.345%2C43.283%2C5.405%2C43.310&amp;layer=mapnik&amp;marker=43.2965%2C5.3698"
        title="Map of Marseille food spots"
        allowfullscreen>
      </iframe>
    </div>
    <div class="map-pins-legend">
      <div class="pin-badge"><div class="pin-dot" style="background:#3FC0F0"></div>Pastis bar</div>
      <div class="pin-badge"><div class="pin-dot" style="background:#F5B800"></div>Panisse spot</div>
      <div class="pin-badge"><div class="pin-dot" style="background:#FF7043"></div>Fougasse bakery</div>
      <div class="pin-badge"><div class="pin-dot" style="background:#26A69A"></div>Hidden gem</div>
    </div>
    <p style="font-size:0.78rem; color:var(--muted); margin-top:0.5rem;">
      Tip: <a href="https://www.openstreetmap.org/?mlat=43.2965&mlon=5.3698#map=14/43.2965/5.3698" target="_blank" style="color:var(--blue);">Open full interactive map ↗</a>
    </p>
    """, unsafe_allow_html=True)

with col_form:
    st.markdown("""
    <div class="section-header">
      <div class="section-eyebrow">AI Discovery</div>
      <h2 class="section-title">Your <em>vibe</em>,<br>your perfect spot</h2>
    </div>
    <div class="form-card">
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-label">🎭 Mood</div>', unsafe_allow_html=True)
    mood_options = ["😎 Chill apéro", "🌅 Sunset spot", "🎉 Going out", "☀️ Beach lunch", "🤫 Hidden gem", "💸 Super broke", "🍽️ Proper dinner", "🧘 Solo & quiet"]
    mood = st.selectbox("Mood", mood_options, label_visibility="collapsed")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="form-label">👥 Group</div>', unsafe_allow_html=True)
        group = st.selectbox("Group", ["Friends", "Solo", "Date night", "Family", "Backpackers"], label_visibility="collapsed")
    with c2:
        st.markdown('<div class="form-label">🎵 Music</div>', unsafe_allow_html=True)
        music = st.selectbox("Music", ["Electro/House", "No preference", "Jazz/Soul", "Hip-hop", "Reggae", "Acoustic", "Quiet"], label_visibility="collapsed")

    st.markdown('<div class="form-label">💶 Max budget/person</div>', unsafe_allow_html=True)
    budget = st.slider("Budget", 5, 60, 15, step=5, label_visibility="collapsed",
                       format="€%d")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="form-label">🕐 Time</div>', unsafe_allow_html=True)
        time_day = st.selectbox("Time", ["Morning", "Lunch", "Afternoon", "Apéro (5–8pm)", "Dinner", "Late night"], label_visibility="collapsed")
    with c4:
        st.markdown('<div class="form-label">📍 Area</div>', unsafe_allow_html=True)
        area = st.selectbox("Area", ["Anywhere", "Vieux-Port / Panier", "Cours Julien", "Noailles", "Endoume", "Pointe Rouge", "La Plaine"], label_visibility="collapsed")

    st.markdown('<div class="form-label">✏️ Tell me more (optional)</div>', unsafe_allow_html=True)
    freetext = st.text_area("", placeholder="E.g. sea view terrace, cheap pastis, avoid touristy…", height=70, label_visibility="collapsed")

    get_recs = st.button("✨ Find my perfect spot")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── AI call ────────────────────────────────────────────────────────────────────
if get_recs:
    prompt = f"""You are Massilia, an AI guide for authentic Marseille food & lifestyle.
Give 3 specific spot recommendations.

User: mood={mood}, group={group}, music={music}, budget=€{budget}/person, time={time_day}, area={area}
Extra: {freetext or 'none'}

Focus on: panisse spots, pastis bars, fougasse bakeries, sunset bars, beach restaurants, apéro places, hidden gems.

Format each as:
**[Name]** – [neighbourhood]
🍽️ Order: ...
💶 Price: ...
🌊 Vibe: ...
🔑 Tip: ...

Warm, fun, local tone. Use occasional French naturally. Short sign-off at end."""

    with st.spinner("Cherching les bons plans… 🌊"):
        try:
            client = anthropic.Anthropic()
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.recs = msg.content[0].text
        except Exception as e:
            st.session_state.recs = f"⚠️ AI unavailable: {e}"

if st.session_state.recs:
    st.markdown('<div class="section" style="padding-top:0">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card">
      <h3>🌊 Massilia recommends</h3>
      {st.session_state.recs.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NEIGHBOURHOOD PHOTO SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section">
  <div class="section-header">
    <div class="section-eyebrow">The Districts</div>
    <h2 class="section-title">Authentic Marseille<br><em>Neighbourhoods</em></h2>
  </div>
  <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:14px;">
    <div style="grid-row: span 2; border-radius:18px; overflow:hidden; position:relative; min-height:320px;">
      <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=700&q=80"
           style="width:100%;height:100%;object-fit:cover;" alt="Cours Julien" loading="lazy"/>
      <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(26,37,64,0.85) 0%,transparent 100%);padding:1.2rem 1rem 0.9rem;color:white;">
        <div style="font-weight:800;font-size:1rem;">Cours Julien</div>
        <div style="font-size:0.8rem;opacity:0.8;">Street art, boho cafés, live music</div>
      </div>
    </div>
    <div style="border-radius:18px; overflow:hidden; position:relative; aspect-ratio:16/9;">
      <img src="https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&q=80"
           style="width:100%;height:100%;object-fit:cover;" alt="Vieux-Port" loading="lazy"/>
      <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(26,37,64,0.85) 0%,transparent 100%);padding:0.9rem 0.9rem 0.7rem;color:white;">
        <div style="font-weight:800;font-size:0.95rem;">Vieux-Port</div>
        <div style="font-size:0.78rem;opacity:0.8;">Historic heart, morning fish market</div>
      </div>
    </div>
    <div style="border-radius:18px; overflow:hidden; position:relative; aspect-ratio:16/9;">
      <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80"
           style="width:100%;height:100%;object-fit:cover;" alt="Noailles" loading="lazy"/>
      <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(26,37,64,0.85) 0%,transparent 100%);padding:0.9rem 0.9rem 0.7rem;color:white;">
        <div style="font-weight:800;font-size:0.95rem;">Noailles</div>
        <div style="font-size:0.78rem;opacity:0.8;">Spices, panisse, the real Marseille</div>
      </div>
    </div>
    <div style="border-radius:18px; overflow:hidden; position:relative; aspect-ratio:16/9;">
      <img src="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&q=80"
           style="width:100%;height:100%;object-fit:cover;" alt="Plage" loading="lazy"/>
      <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(26,37,64,0.85) 0%,transparent 100%);padding:0.9rem 0.9rem 0.7rem;color:white;">
        <div style="font-weight:800;font-size:0.95rem;">Endoume / Malmousque</div>
        <div style="font-size:0.78rem;opacity:0.8;">Rocky inlets, sunset bars, locals</div>
      </div>
    </div>
    <div style="border-radius:18px; overflow:hidden; position:relative; aspect-ratio:16/9;">
      <img src="https://images.unsplash.com/photo-1514190051997-0f6f39ca5cde?w=600&q=80"
           style="width:100%;height:100%;object-fit:cover;" alt="Le Panier" loading="lazy"/>
      <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(26,37,64,0.85) 0%,transparent 100%);padding:0.9rem 0.9rem 0.7rem;color:white;">
        <div style="font-weight:800;font-size:0.95rem;">Le Panier</div>
        <div style="font-size:0.78rem;opacity:0.8;">Oldest quarter, hidden gems</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMMUNITY SPOTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header" style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
  <div>
    <div class="section-eyebrow">Join the Community</div>
    <h2 class="section-title">Real tips from<br><em>real locals</em></h2>
  </div>
</div>
""", unsafe_allow_html=True)

tab_all, tab_panisse, tab_pastis, tab_fougasse = st.tabs(["All spots", "Panisse 🍟", "Pastis 🥛", "Fougasse 🫓"])

def render_spots(spots):
    st.markdown('<div class="spot-grid">', unsafe_allow_html=True)
    for s in spots:
        st.markdown(f"""
        <div class="spot-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div class="spot-name">{s['name']}</div>
            <div class="spot-cat">{s['category']}</div>
          </div>
          <div class="spot-meta">📍 {s['vibe']} &nbsp;·&nbsp; 💶 {s['price']}</div>
          <div class="spot-tip">"{s['tip']}"</div>
          <div class="spot-author">— {s['author']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_all:
    render_spots(st.session_state.community_spots)
with tab_panisse:
    render_spots([s for s in st.session_state.community_spots if "Panisse" in s["category"]])
with tab_pastis:
    render_spots([s for s in st.session_state.community_spots if "Pastis" in s["category"]])
with tab_fougasse:
    render_spots([s for s in st.session_state.community_spots if "Fougasse" in s["category"]])

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SHARE A SPOT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
  <div class="section-eyebrow">Share</div>
  <h2 class="section-title">Add your<br><em>hidden gem</em></h2>
</div>
""", unsafe_allow_html=True)

with st.form("share_form"):
    fc1, fc2 = st.columns(2)
    with fc1:
        s_name = st.text_input("Spot name *", placeholder="e.g. Chez Jeannot")
        s_vibe = st.text_input("Vibe / neighbourhood", placeholder="e.g. Le Panier, cash only")
    with fc2:
        s_cat = st.selectbox("Category *", ["Panisse 🍟", "Pastis 🥛", "Fougasse 🫓", "Other 🍽️"])
        s_price = st.selectbox("Price", ["€ (under €10)", "€€ (€10–20)", "€€€ (€20+)"])
    s_tip = st.text_area("Your local tip *", placeholder="What to order, best time, what makes it special…", height=90)
    s_author = st.text_input("Your name / nickname", placeholder="e.g. Théo, étudiant")
    submitted = st.form_submit_button("🌊 Share this spot")
    if submitted:
        if s_name and s_tip:
            st.session_state.community_spots.append({
                "name": s_name, "category": s_cat,
                "vibe": s_vibe or "Marseille", "price": s_price.split(" ")[0],
                "tip": s_tip, "author": s_author or "Anonymous",
                "lat": 43.2965, "lng": 5.3698,
            })
            st.success(f"Merci ! **{s_name}** has been added to the community 🎉")
        else:
            st.warning("Please fill in at least the spot name and your tip.")

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NEWSLETTER BAND
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="newsletter-band">
  <div>
    <h2>The insider's newsletter.</h2>
    <p>No spam. Only secret openings, local events, and the best places to hide from the tourists this summer.</p>
  </div>
  <div style="display:flex;gap:0.7rem;flex-wrap:wrap;">
    <input type="email" placeholder="Your email address"
      style="border-radius:50px;border:none;padding:0.65rem 1.4rem;font-family:Nunito,sans-serif;font-size:0.95rem;min-width:220px;outline:none;"/>
    <button style="background:var(--yellow);color:var(--dark);border:none;border-radius:50px;padding:0.65rem 1.6rem;font-family:Nunito,sans-serif;font-weight:800;font-size:0.95rem;cursor:pointer;">
      Subscribe
    </button>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:var(--dark);padding:2.5rem 3rem 1.5rem;margin-top:0;">
  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:2rem;margin-bottom:2rem;">
    <div>
      <div style="font-family:Pacifico,cursive;font-size:1.5rem;color:var(--blue);margin-bottom:0.4rem;">Massilia</div>
      <div style="font-size:0.82rem;color:rgba(255,255,255,0.5);font-style:italic;">Pas fâché avec le plaisir 🌊</div>
      <div style="font-size:0.78rem;color:rgba(255,255,255,0.35);margin-top:0.3rem;">Panis · Pastis · Fougasse<br>A Marseille journey from the inside.</div>
    </div>
    <div style="display:flex;gap:3rem;flex-wrap:wrap;">
      <div>
        <div style="color:rgba(255,255,255,0.6);font-size:0.8rem;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.7rem;">Explore</div>
        <div style="display:flex;flex-direction:column;gap:0.4rem;">
          <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Vieux-Port</a>
          <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Neighbourhoods</a>
          <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Interactive Map</a>
        </div>
      </div>
      <div>
        <div style="color:rgba(255,255,255,0.6);font-size:0.8rem;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.7rem;">Community</div>
        <div style="display:flex;flex-direction:column;gap:0.4rem;">
          <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Our Story</a>
          <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Contact</a>
        </div>
      </div>
    </div>
  </div>
  <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:1rem;font-size:0.75rem;color:rgba(255,255,255,0.25);">
    © 2025 Massilia. All rights reserved.
  </div>
</div>
""", unsafe_allow_html=True)
