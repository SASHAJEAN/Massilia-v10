import streamlit as st
import anthropic
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Massilia – Pas fâché avec le plaisir",
    page_icon="🍋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --blue:   #3FC0F0;
    --yellow: #F5B800;
    --cream:  #FFF5E6;
    --dark:   #1A2540;
    --card:   #FFFFFF;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--cream) !important;
    font-family: 'Nunito', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Hero */
.hero {
    text-align: center;
    padding: 2rem 0 1rem;
}
.hero-logo {
    font-family: 'Pacifico', cursive;
    font-size: 3.4rem;
    color: var(--blue);
    line-height: 1;
    letter-spacing: -1px;
}
.hero-tagline {
    font-size: 0.95rem;
    letter-spacing: 0.18em;
    color: var(--yellow);
    font-weight: 800;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.hero-slogan {
    font-size: 1.05rem;
    color: var(--dark);
    font-style: italic;
    margin-top: 0.5rem;
    opacity: 0.75;
}

/* Section titles */
.section-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--dark);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.4rem 0 0.6rem;
}

/* Mood pills */
.mood-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem; }
.mood-pill {
    background: var(--blue);
    color: white;
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    transition: background 0.2s;
}
.mood-pill:hover { background: var(--yellow); color: var(--dark); }

/* Result card */
.result-card {
    background: var(--card);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    border-left: 6px solid var(--blue);
    box-shadow: 0 4px 24px rgba(63,192,240,0.13);
    margin-top: 1rem;
    font-size: 0.97rem;
    line-height: 1.7;
    color: var(--dark);
}
.result-card h3 {
    font-family: 'Pacifico', cursive;
    font-size: 1.35rem;
    color: var(--blue);
    margin-bottom: 0.5rem;
}

/* Community cards */
.spot-card {
    background: white;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    border-top: 4px solid var(--yellow);
}
.spot-card .spot-name { font-weight: 800; font-size: 1rem; color: var(--dark); }
.spot-card .spot-meta { font-size: 0.82rem; color: #888; margin-top: 0.2rem; }
.spot-card .spot-tip { font-size: 0.9rem; margin-top: 0.4rem; color: var(--dark); }

/* Divider */
.wavy-divider { text-align: center; font-size: 1.4rem; margin: 0.6rem 0; letter-spacing: 0.3em; }

/* Override Streamlit button */
div.stButton > button {
    background: var(--blue) !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.55rem 2rem !important;
    transition: background 0.2s !important;
}
div.stButton > button:hover {
    background: var(--yellow) !important;
    color: var(--dark) !important;
}

/* Submit share button secondary style */
.secondary-btn > button {
    background: var(--yellow) !important;
    color: var(--dark) !important;
}

/* Select / text input */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 10px !important;
    border-color: #ddd !important;
    font-family: 'Nunito', sans-serif !important;
}

textarea {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}

/* Budget slider accent */
div[data-testid="stSlider"] div[role="slider"] {
    background: var(--blue) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "recs" not in st.session_state:
    st.session_state.recs = None
if "community_spots" not in st.session_state:
    st.session_state.community_spots = [
        {
            "name": "Chez Étienne",
            "category": "Panisse 🍟",
            "vibe": "Locals only, cash, no menu",
            "price": "€",
            "tip": "Order the panisse nature and eat standing at the counter – perfect before 12h.",
            "author": "Lucas, étudiant AMU",
        },
        {
            "name": "Bar de la Marine",
            "category": "Pastis 🥛",
            "vibe": "Old Port classic, Marcel Pagnol vibes",
            "price": "€€",
            "tip": "Grab a table outside at golden hour. Ricard + olives = life.",
            "author": "Sofia, backpacker",
        },
        {
            "name": "La Fougasserie du Panier",
            "category": "Fougasse 🫓",
            "vibe": "Hidden bakery in Le Panier",
            "price": "€",
            "tip": "The anchovy & olive fougasse at 8am before tourists arrive is 🔥",
            "author": "Théo, jeune actif",
        },
    ]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-logo">Massilia</div>
  <div class="hero-tagline">Panis · Pastis · Fougasse</div>
  <div class="hero-slogan">Pas fâché avec le plaisir 🌊</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="wavy-divider">〰〰〰</div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_discover, tab_community, tab_share = st.tabs(["🍋 Discover", "🌊 Community Spots", "✍️ Share a Spot"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – AI DISCOVERY
# ════════════════════════════════════════════════════════════════════════════
with tab_discover:
    st.markdown('<div class="section-title">🎭 Your vibe right now</div>', unsafe_allow_html=True)

    mood_options = ["😎 Chill apéro", "🌅 Sunset spot", "🎉 Going out tonight", "☀️ Beach lunch", "🤫 Hidden gem", "💸 Super broke", "🍽️ Proper dinner", "🧘 Quiet & solo"]
    mood = st.selectbox("Mood", mood_options, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">👥 Group type</div>', unsafe_allow_html=True)
        group = st.selectbox("Group", ["Friends", "Solo", "Date night", "Family", "Backpackers"], label_visibility="collapsed")
    with col2:
        st.markdown('<div class="section-title">🎵 Music vibe</div>', unsafe_allow_html=True)
        music = st.selectbox("Music", ["Electro / House", "No preference", "Jazz / Soul", "Hip-hop / Trap", "Reggae / Afro", "Acoustic / Folk", "None / Quiet"], label_visibility="collapsed")

    st.markdown('<div class="section-title">💶 Max budget per person</div>', unsafe_allow_html=True)
    budget = st.slider("Budget (€)", 5, 60, 15, step=5, label_visibility="collapsed")
    st.caption(f"Budget: up to **€{budget}** per person")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">🕐 Time of day</div>', unsafe_allow_html=True)
        time_day = st.selectbox("Time", ["Morning", "Lunch", "Afternoon", "Apéro (5–8pm)", "Dinner", "Late night"], label_visibility="collapsed")
    with col4:
        st.markdown('<div class="section-title">📍 Area</div>', unsafe_allow_html=True)
        area = st.selectbox("Area", ["Anywhere in Marseille", "Old Port / Panier", "Cours Julien", "Noailles", "Endoume / Malmousque", "Pointe Rouge / beach", "La Plaine", "Centre-ville"], label_visibility="collapsed")

    st.markdown('<div class="section-title">✏️ Tell me more (optional)</div>', unsafe_allow_html=True)
    freetext = st.text_area("", placeholder="E.g. I want a terrace with sea view and cheap pastis, avoid touristy places…", height=80, label_visibility="collapsed")

    st.markdown("")
    get_recs = st.button("✨ Find my perfect spot")

    if get_recs:
        prompt = f"""You are Massilia, an AI guide for authentic Marseille food & lifestyle experiences.
A user is looking for recommendations. Give them 3 specific, detailed spot suggestions.

User profile:
- Mood: {mood}
- Group: {group}
- Music vibe: {music}
- Max budget: €{budget}/person
- Time of day: {time_day}
- Area preference: {area}
- Extra notes: {freetext or 'None'}

Focus on: panisse spots, pastis bars, fougasse bakeries, sunset bars, beach restaurants, apéro places, hidden gems — authentic Marseille experiences.

Format your response as 3 recommendations. For each:
**[Spot Name]** – [neighbourhood]
🍽️ What to order: ...
💶 Price range: ...
🌊 Vibe: ...
🔑 Local tip: ...

Keep the tone warm, fun and local — like advice from a Marseillais friend. Use occasional French words naturally. End with a short motivating sign-off line."""

        with st.spinner("Cherching les bons plans... 🌊"):
            try:
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state.recs = message.content[0].text
            except Exception as e:
                st.session_state.recs = f"⚠️ Couldn't connect to AI: {e}"

    if st.session_state.recs:
        st.markdown(f'<div class="result-card"><h3>🌊 Massilia recommends</h3>{st.session_state.recs.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – COMMUNITY SPOTS
# ════════════════════════════════════════════════════════════════════════════
with tab_community:
    st.markdown('<div class="section-title">🌊 Local spots shared by the community</div>', unsafe_allow_html=True)
    st.caption("Real tips from students, young workers and backpackers in Marseille.")

    filter_cat = st.selectbox("Filter by", ["All", "Panisse 🍟", "Pastis 🥛", "Fougasse 🫓", "Other 🍽️"], label_visibility="visible")

    for spot in st.session_state.community_spots:
        if filter_cat != "All" and filter_cat not in spot["category"]:
            continue
        st.markdown(f"""
        <div class="spot-card">
            <div class="spot-name">{spot['name']} <span style="color:var(--yellow)">{spot['category']}</span></div>
            <div class="spot-meta">📍 {spot['vibe']} &nbsp;·&nbsp; 💶 {spot['price']} &nbsp;·&nbsp; 👤 {spot['author']}</div>
            <div class="spot-tip">💬 {spot['tip']}</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 – SHARE A SPOT
# ════════════════════════════════════════════════════════════════════════════
with tab_share:
    st.markdown('<div class="section-title">✍️ Share your favourite hidden gem</div>', unsafe_allow_html=True)
    st.caption("Help the Massilia community discover the best of Marseille 🌊")

    with st.form("share_form"):
        s_name = st.text_input("Spot name *", placeholder="e.g. Chez Jeannot")
        s_cat = st.selectbox("Category *", ["Panisse 🍟", "Pastis 🥛", "Fougasse 🫓", "Other 🍽️"])
        s_vibe = st.text_input("Vibe / neighbourhood", placeholder="e.g. Le Panier, very local, cash only")
        s_price = st.selectbox("Price range", ["€ (under €10)", "€€ (€10–20)", "€€€ (€20+)"])
        s_tip = st.text_area("Your local tip *", placeholder="What to order, best time to go, what makes it special…", height=90)
        s_author = st.text_input("Your name / nickname", placeholder="e.g. Théo, étudiant")

        submitted = st.form_submit_button("🌊 Share this spot")

        if submitted:
            if s_name and s_tip:
                st.session_state.community_spots.append({
                    "name": s_name,
                    "category": s_cat,
                    "vibe": s_vibe or "Marseille",
                    "price": s_price.split(" ")[0],
                    "tip": s_tip,
                    "author": s_author or "Anonymous",
                })
                st.success(f"Merci ! **{s_name}** has been added to the community spots 🎉")
            else:
                st.warning("Please fill in at least the spot name and your tip.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:2.5rem; padding-top:1rem; border-top:2px dashed #F5B800; opacity:0.6; font-size:0.8rem; color:#1A2540;">
    <b>Massilia</b> · Panis · Pastis · Fougasse · <i>Pas fâché avec le plaisir</i> 🌊
</div>
""", unsafe_allow_html=True)
