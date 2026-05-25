import streamlit as st
import anthropic
import base64
from pathlib import Path

st.set_page_config(
    page_title="Massilia — Panis · Pastis · Fougasse",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Embed real brand images as base64 ──────────────────────────────────────
def img_b64(path):
    try:
        data = Path(path).read_bytes()
        ext = Path(path).suffix.lstrip(".")
        mime = "image/jpeg" if ext in ("jpg","jpeg") else f"image/{ext}"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return ""

LOGO_DATA    = img_b64("logo.jpg")
PATTERN_DATA = img_b64("pattern.jpg")

# ════════════════════════════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,700&display=swap');

:root {
  --blue:   #3FC0F0;
  --yellow: #F5B800;
  --cream:  #FEF5E4;
  --dark:   #1A2540;
  --green:  #18B07A;
  --muted:  #5A6680;
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
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.topbar-logo { height: 44px; width: auto; display: block; }
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

/* ══ HERO — pattern bg + logo ══ */
.hero-wrap {
  position: relative; width: 100%;
  min-height: 340px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.hero-pattern {
  position: absolute; inset: 0;
  background-repeat: repeat;
  background-size: 220px auto;
  opacity: 0.18;
  pointer-events: none;
}
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(160deg, rgba(254,245,228,0.80) 0%, rgba(254,245,228,0.55) 60%, rgba(63,192,240,0.08) 100%);
}
.hero-content {
  position: relative; z-index: 2;
  display: flex; flex-direction: column;
  align-items: center; text-align: center;
  padding: 2.8rem 1.5rem 2rem;
}
.hero-logo-img { height: 140px; width: auto; drop-shadow: 0 4px 24px rgba(63,192,240,0.3); margin-bottom: 0.2rem; }
.hero-tagline {
  font-family: 'Nunito',sans-serif; font-weight: 800; font-size: 1.05rem;
  color: var(--blue); letter-spacing: 0.05em; margin-top: 0.2rem;
}
.hero-sub {
  margin-top: 0.6rem; font-size: 1rem; color: var(--dark);
  font-weight: 600; max-width: 440px; line-height: 1.55;
  opacity: 0.8;
}

/* ══ AI PROFILE CARD ══ (first, hero feature) */
.ai-card {
  margin: 0 auto 0;
  max-width: 860px;
  border-radius: 28px; overflow: hidden;
  box-shadow: 0 12px 48px rgba(63,192,240,0.22);
  border: 2px solid rgba(63,192,240,0.2);
}
.ai-banner {
  background: linear-gradient(135deg, #1A2540 0%, #0D3A5C 80%, #0A5070 100%);
  padding: 1.6rem 2rem;
  display: flex; align-items: flex-start; gap: 1.2rem;
}
.ai-avatar-ring {
  width: 58px; height: 58px; border-radius: 50%;
  border: 3px solid rgba(63,192,240,0.5);
  background: rgba(63,192,240,0.15);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem; flex-shrink: 0;
}
.ai-eyebrow {
  font-size: 0.68rem; font-weight: 900; letter-spacing: 0.22em;
  text-transform: uppercase; color: var(--yellow); margin-bottom: 0.2rem;
}
.ai-headline {
  font-family: 'Pacifico',cursive; font-size: 1.5rem;
  color: #fff; line-height: 1.15; margin-bottom: 0.25rem;
}
.ai-subline { font-size: 0.83rem; color: rgba(255,255,255,0.65); line-height: 1.5; margin-bottom: 0.6rem; }
.ai-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.abadge {
  background: rgba(63,192,240,0.18); color: #7DD9F7;
  border: 1px solid rgba(63,192,240,0.35);
  border-radius: 50px; padding: 0.22rem 0.8rem;
  font-size: 0.72rem; font-weight: 800;
}

.ai-body {
  background: #fff; padding: 1.6rem 2rem 0.5rem;
}
.ai-body-intro { margin-bottom: 1.2rem; }
.ai-body-intro h3 { font-size: 1.05rem; font-weight: 900; color: var(--dark); margin-bottom: 0.2rem; }
.ai-body-intro p  { font-size: 0.85rem; color: var(--muted); line-height: 1.5; }

.pf-label {
  font-size: 0.72rem; font-weight: 900;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 0.3rem; margin-top: 0.1rem;
}

/* selects inside white card */
.ai-body div[data-baseweb="select"] > div {
  background: #F5F7FA !important; border-color: #DDE3EE !important;
  color: var(--dark) !important; border-radius: 12px !important;
  font-family: 'Nunito',sans-serif !important;
}
.ai-body div[data-baseweb="select"] span { color: var(--dark) !important; }
.ai-body div[data-baseweb="select"] svg  { color: var(--muted) !important; }
.ai-body textarea {
  background: #F5F7FA !important; color: var(--dark) !important;
  border-color: #DDE3EE !important; border-radius: 12px !important;
}
.ai-body textarea::placeholder { color: #AAB4C4 !important; }
.ai-body [data-testid="stSlider"] div[role="slider"] { background: var(--blue) !important; }
.ai-body [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

/* CTA */
.ai-cta { padding: 1rem 2rem 1.8rem; background: #fff; }
.ai-cta div.stButton > button {
  background: linear-gradient(135deg, var(--blue) 0%, #1BA8E0 100%) !important;
  color: #fff !important; font-size: 1.05rem !important;
  padding: 0.8rem 2rem !important; border-radius: 50px !important;
  border: none !important; font-family: 'Nunito',sans-serif !important;
  font-weight: 900 !important; width: 100% !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 20px rgba(63,192,240,0.35) !important;
}
.ai-cta div.stButton > button:hover {
  background: linear-gradient(135deg, var(--yellow) 0%, #E5A800 100%) !important;
  color: var(--dark) !important;
  box-shadow: 0 4px 20px rgba(245,184,0,0.35) !important;
}

/* ── RESULT BOX ── */
.result-wrap { padding: 0 0 1.5rem; max-width: 860px; margin: 0 auto; }
.result-box {
  background: #fff; border-radius: 20px;
  padding: 1.6rem 1.8rem;
  border-left: 5px solid var(--blue);
  box-shadow: 0 4px 24px rgba(63,192,240,0.12);
  font-size: 0.95rem; line-height: 1.85; color: var(--dark);
}
.result-box h3 {
  font-family: 'Pacifico',cursive; font-size: 1.2rem;
  color: var(--blue); margin-bottom: 0.7rem;
}

/* ── MAP HERO ── */
.map-section { padding: 2rem 2rem 0; }
.map-hero { position: relative; width: 100%; border-radius: 24px; overflow: hidden; }
.map-frame { width: 100%; height: 400px; border: none; display: block; }
.map-overlay-card {
  position: absolute; top: 16px; left: 16px;
  background: #fff; border-radius: 20px;
  padding: 1.1rem 1.3rem; max-width: 278px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18); z-index: 10;
}
.map-overlay-card h3 {
  font-family: 'Pacifico',cursive; font-size: 1rem;
  color: var(--dark); line-height: 1.25; margin-bottom: 0.3rem;
}
.map-overlay-card h3 em { color: var(--blue); font-style: normal; }
.map-overlay-card p { font-size: 0.78rem; color: var(--muted); line-height: 1.5; margin-bottom: 0.8rem; }
.filter-pills { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.fpill {
  border-radius: 50px; padding: 0.28rem 0.8rem;
  font-size: 0.72rem; font-weight: 800; border: none; cursor: pointer;
}
.fpill-all      { background: var(--dark);  color: #fff; }
.fpill-panisse  { background: #FFF0B3;      color: #6B4A00; }
.fpill-pastis   { background: #CBF0FF;      color: #083C52; }
.fpill-fougasse { background: #C6F7E4;      color: #0A3D28; }

.map-bar {
  background: rgba(255,255,255,0.9); padding: 0.55rem 1.2rem;
  display: flex; align-items: center; justify-content: space-between;
  border-top: 1px solid #EBEBEB; border-radius: 0 0 24px 24px;
}
.map-bar span { font-size: 0.8rem; color: var(--muted); }
.map-bar b    { color: var(--dark); }
.map-bar a    { font-size: 0.8rem; font-weight: 800; color: var(--blue); text-decoration: none; }

/* ── SECTION WRAPPERS ── */
.sec { padding: 2rem 2rem 0; }
.sec-hdr {
  display: flex; align-items: baseline; justify-content: space-between;
  margin-bottom: 1.1rem;
}
.sec-hdr h2 { font-size: 1.4rem; font-weight: 900; color: var(--dark); }
.sec-hdr h2 em { color: var(--blue); font-style: normal; }
.sec-hdr .see-all { font-size: 0.83rem; font-weight: 800; color: var(--blue); cursor: pointer; }

/* ── SCROLL CARDS ── */
.cards-scroll {
  display: flex; gap: 1rem; overflow-x: auto;
  padding-bottom: 1rem; -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.cards-scroll::-webkit-scrollbar { display: none; }
.spot-card {
  flex: 0 0 210px; border-radius: 20px; overflow: hidden;
  background: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.2s; cursor: pointer;
}
.spot-card:hover { transform: translateY(-4px); }
.spot-card-img { width: 210px; height: 140px; object-fit: cover; display: block; }
.spot-card-body { padding: 0.8rem 0.95rem 0.9rem; }
.spot-card-cat { font-size: 0.68rem; font-weight: 900; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.25rem; }
.c-panisse  { color: #8A6000; }
.c-pastis   { color: #0A6A9A; }
.c-fougasse { color: #0A7050; }
.c-other    { color: #A0304A; }
.spot-card-name { font-weight: 900; font-size: 0.96rem; color: var(--dark); line-height: 1.2; margin-bottom: 0.25rem; }
.spot-card-vibe { font-size: 0.76rem; color: var(--muted); line-height: 1.4; }
.spot-card-foot { display: flex; justify-content: space-between; align-items: center; margin-top: 0.55rem; padding-top: 0.55rem; border-top: 1px solid #F0F0EA; }
.price  { font-size: 0.78rem; font-weight: 900; color: var(--green); }
.rating { font-size: 0.78rem; font-weight: 800; color: #C08B00; }

/* ── VIBES GRID ── */
.vibes-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; }
.vibe-tile { border-radius: 18px; overflow: hidden; aspect-ratio: 1/1; position: relative; cursor: pointer; }
.vibe-tile img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.3s; }
.vibe-tile:hover img { transform: scale(1.07); }
.vibe-overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: rgba(26,37,64,0.4); color: #fff; text-align: center; padding: 0.5rem;
  transition: background 0.2s;
}
.vibe-tile:hover .vibe-overlay { background: rgba(63,192,240,0.65); }
.vibe-emoji { font-size: 1.55rem; margin-bottom: 0.2rem; }
.vibe-label { font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.07em; }

/* ── COMMUNITY ── */
.community-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px,1fr)); gap: 1rem; }
.community-card { background: #fff; border-radius: 18px; padding: 1.1rem 1.2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.cc-blue   { border-left: 4px solid var(--blue);   }
.cc-yellow { border-left: 4px solid var(--yellow); }
.cc-green  { border-left: 4px solid var(--green);  }
.cc-avatar { width: 36px; height: 36px; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.cc-avatar img { width: 100%; height: 100%; object-fit: cover; }
.cc-name   { font-weight: 800; font-size: 0.88rem; color: var(--dark); }
.cc-role   { font-size: 0.72rem; color: var(--muted); }
.cc-quote  { font-size: 0.88rem; line-height: 1.55; color: var(--dark); margin: 0.7rem 0 0.5rem; font-style: italic; }
.cc-tag    { display: inline-block; background: rgba(63,192,240,0.1); color: #0A6A9A; border-radius: 50px; padding: 0.2rem 0.7rem; font-size: 0.72rem; font-weight: 800; }

/* ── SHARE FORM ── */
.share-sec { padding: 2rem 2rem 0; }
.share-sec div[data-baseweb="select"] > div { background: #fff !important; border-color: #DDE3EE !important; color: var(--dark) !important; border-radius: 12px !important; }
.share-sec div[data-baseweb="select"] span  { color: var(--dark) !important; }
.share-sec div[data-baseweb="input"] input  { background: #fff !important; color: var(--dark) !important; border-color: #DDE3EE !important; }
.share-sec textarea { background: #fff !important; color: var(--dark) !important; border-color: #DDE3EE !important; }
.share-sec div.stButton > button { background: var(--yellow) !important; color: var(--dark) !important; font-weight: 900 !important; }

/* ── NEWSLETTER ── */
.newsletter { margin: 2rem 2rem 0; background: var(--blue); border-radius: 24px; padding: 2.2rem 2rem; text-align: center; }
.newsletter h2 { font-family: 'Pacifico',cursive; font-size: 1.7rem; color: #fff; margin-bottom: 0.4rem; }
.newsletter p  { font-size: 0.9rem; color: rgba(255,255,255,0.9); margin-bottom: 1.2rem; line-height: 1.6; }

/* ── FOOTER ── */
.footer { background: var(--dark); padding: 2.2rem 2rem 1.5rem; text-align: center; margin-top: 2rem; }

/* ── GLOBAL OVERRIDES ── */
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

/* ── SECTION DIVIDER ── */
.divider { height: 2px; background: linear-gradient(90deg, transparent, rgba(63,192,240,0.2), transparent); margin: 2.5rem 2rem 0; }

/* ── SECTION LABEL CHIP ── */
.section-chip {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(63,192,240,0.1); color: var(--blue);
  border: 1px solid rgba(63,192,240,0.3); border-radius: 50px;
  padding: 0.25rem 0.9rem; font-size: 0.72rem; font-weight: 900;
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.7rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "recs" not in st.session_state:
    st.session_state.recs = None

# ════════════════════════════════════════════════════════════════════════════
# NAV
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <img src="{LOGO_DATA}" class="topbar-logo" alt="Massilia"/>
  <div style="display:flex;gap:0.5rem;align-items:center;">
    <button class="nav-pill ghost">Sign in</button>
    <button class="nav-pill">Explore 🌊</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# HERO — pattern background + logo
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-pattern" style="background-image:url('{PATTERN_DATA}');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <img src="{LOGO_DATA}" class="hero-logo-img" alt="Massilia"/>
    <div class="hero-sub">
      Découvre les meilleures adresses de Marseille — panisse, pastis, fougasse &amp; bien plus —<br>
      choisies par des locaux, pour toi.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 1 ── AI PROFILE — hero feature, first content section
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div style="padding: 2rem 2rem 0;">""", unsafe_allow_html=True)
st.markdown("""
<span class="section-chip">✨ Powered by AI</span>
<div class="ai-card">
  <div class="ai-banner">
    <div class="ai-avatar-ring">🌊</div>
    <div>
      <div class="ai-eyebrow">Ton expérience personnalisée</div>
      <div class="ai-headline">Ton vibe,<br>ta Marseille</div>
      <div class="ai-subline">
        Dis-nous ton humeur, ton budget, avec qui tu es —<br>
        notre IA te trouve le spot parfait en quelques secondes.
      </div>
      <div class="ai-badges">
        <span class="abadge">📍 Géo-localisé</span>
        <span class="abadge">💶 Budget malin</span>
        <span class="abadge">🎭 Mood-based</span>
        <span class="abadge">✨ IA générative</span>
      </div>
    </div>
  </div>
  <div class="ai-body">
    <div class="ai-body-intro">
      <h3>C'est quoi ton plan aujourd'hui ?</h3>
      <p>Plus tu nous en dis, meilleures seront tes recommandations.</p>
    </div>
""", unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    st.markdown('<div class="pf-label">🎭 Ton humeur</div>', unsafe_allow_html=True)
    mood = st.selectbox("mood", ["😎 Apéro chill","🌅 Vue sur la mer","🎉 Soirée","☀️ Déj en terrasse","🤫 Plan de local","💸 Petit budget","🍽️ Dîner sérieux","🧘 Solo & tranquille"], label_visibility="collapsed", key="mood")
with r1c2:
    st.markdown('<div class="pf-label">👥 Vous êtes combien ?</div>', unsafe_allow_html=True)
    group = st.selectbox("group", ["Entre amis","Solo","En couple","En famille","Backpackers"], label_visibility="collapsed", key="group")
with r1c3:
    st.markdown('<div class="pf-label">🎵 Ambiance musicale</div>', unsafe_allow_html=True)
    music = st.selectbox("music", ["Pas de préférence","Électro / House","Jazz / Soul","Hip-hop","Reggae","Acoustique","Silence total"], label_visibility="collapsed", key="music")

r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    st.markdown('<div class="pf-label">💶 Budget max / personne</div>', unsafe_allow_html=True)
    budget = st.slider("budget", 5, 60, 15, step=5, label_visibility="collapsed", key="budget", format="€%d")
    st.caption(f"Jusqu'à **€{budget}** par personne")
with r2c2:
    st.markdown('<div class="pf-label">🕐 Moment de la journée</div>', unsafe_allow_html=True)
    time_day = st.selectbox("time", ["Matin","Déjeuner","Après-midi","Apéro (17h–20h)","Dîner","Nuit"], label_visibility="collapsed", key="time_day")
with r2c3:
    st.markdown('<div class="pf-label">📍 Quartier</div>', unsafe_allow_html=True)
    area = st.selectbox("area", ["Peu importe","Vieux-Port","Cours Julien","Noailles","Endoume","Pointe Rouge","Le Panier","La Joliette"], label_visibility="collapsed", key="area")

st.markdown('<div class="pf-label" style="margin-top:0.6rem;">✏️ Un mot sur tes envies ?</div>', unsafe_allow_html=True)
freetext = st.text_area("extra", placeholder="ex : terrasse avec vue mer, pastis pas cher, éviter les touristes, besoin de wifi…", height=70, label_visibility="collapsed", key="freetext")

st.markdown("</div>", unsafe_allow_html=True)  # close ai-body

st.markdown('<div class="ai-cta">', unsafe_allow_html=True)
go = st.button("🌊 Trouve mon spot parfait — c'est gratuit")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # close ai-card
st.markdown("</div>", unsafe_allow_html=True)  # close padding wrapper

# ── AI CALL ────────────────────────────────────────────────────────────────────
if go:
    prompt = f"""Tu es Massilia, le guide IA de l'authentique Marseille — bouffe, apéro, vie locale.
Donne exactement 3 recommandations de spots personnalisées.

Profil utilisateur : humeur={mood}, groupe={group}, musique={music}, budget=€{budget}/personne, moment={time_day}, quartier={area}
Détails supplémentaires : {freetext or 'aucun'}

Focus : spots à panisse, bars à pastis, boulangeries fougasse, bars coucher de soleil, restos de plage, pépites cachées.

Pour chaque spot :
**[Nom]** · [quartier]
🍽️ Commander : ...
💶 Prix : ...
🌊 Ambiance : ...
🔑 Astuce : ...

Ton : chaleureux, fun, local — comme un pote marseillais qui t'envoie un message. Quelques mots en français naturellement glissés. Mot de fin sympa."""

    with st.spinner("On cherche les bons plans… 🌊"):
        try:
            client = anthropic.Anthropic()
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.recs = msg.content[0].text
        except Exception as e:
            st.session_state.recs = f"⚠️ IA indisponible : {e}"

if st.session_state.recs:
    st.markdown('<div style="padding: 1rem 2rem 0;"><div class="result-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-box">
      <h3>🌊 Tes spots, rien que pour toi</h3>
      {st.session_state.recs.replace(chr(10), "<br>")}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 2 ── MAP
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="map-section">
  <div class="sec-hdr">
    <h2>📍 La carte des <em>spots</em></h2>
    <span class="see-all">Voir tous →</span>
  </div>
  <div class="map-hero">
    <div class="map-overlay-card">
      <h3>Les meilleures adresses de <em>Marseille</em></h3>
      <p>Adresses authentiques sélectionnées par des étudiants & locaux.</p>
      <div class="filter-pills">
        <span class="fpill fpill-all">Tout</span>
        <span class="fpill fpill-panisse">🍟 Panisse</span>
        <span class="fpill fpill-pastis">🥛 Pastis</span>
        <span class="fpill fpill-fougasse">🫓 Fougasse</span>
      </div>
    </div>
    <iframe class="map-frame"
      src="https://www.openstreetmap.org/export/embed.html?bbox=5.342%2C43.281%2C5.408%2C43.311&layer=mapnik"
      title="Carte spots Marseille" loading="lazy">
    </iframe>
    <div class="map-bar">
      <span>📍 <b>Centre de Marseille</b> — 12 spots à proximité</span>
      <a href="https://www.openstreetmap.org/?mlat=43.2965&mlon=5.3698#map=14/43.2965/5.3698" target="_blank">Carte complète ↗</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 3 ── HOT RIGHT NOW
# ════════════════════════════════════════════════════════════════════════════
SPOTS = [
    {"name":"Chez Étienne",         "category":"Panisse",  "vibe":"Noailles · cash only, que des locaux", "price":"€",   "rating":"4.9",
     "img":"https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=420&h=280&fit=crop&q=80"},
    {"name":"Bar de la Marine",      "category":"Pastis",   "vibe":"Vieux-Port · vibes Pagnol",            "price":"€€",  "rating":"4.8",
     "img":"https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=420&h=280&fit=crop&q=80"},
    {"name":"Fougasserie du Panier", "category":"Fougasse", "vibe":"Le Panier · boulangerie cachée",        "price":"€",   "rating":"4.7",
     "img":"https://images.unsplash.com/photo-1509440159596-0249088772ff?w=420&h=280&fit=crop&q=80"},
    {"name":"Café Populaire",        "category":"Pastis",   "vibe":"Cours Julien · terrasse bobo",         "price":"€€",  "rating":"4.6",
     "img":"https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=420&h=280&fit=crop&q=80"},
    {"name":"L'Épicerie du Midi",    "category":"Panisse",  "vibe":"Noailles · vibe marché",               "price":"€",   "rating":"4.5",
     "img":"https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=420&h=280&fit=crop&q=80"},
    {"name":"Le Trolleybus",         "category":"Pastis",   "vibe":"Vieux-Port · DJ tard le soir",         "price":"€€",  "rating":"4.4",
     "img":"https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?w=420&h=280&fit=crop&q=80"},
]
CAT_C = {"Panisse":"c-panisse","Pastis":"c-pastis","Fougasse":"c-fougasse"}

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="sec">
  <div class="sec-hdr">
    <h2>🔥 En ce moment <em>à Marseille</em></h2>
    <span class="see-all">Voir tout →</span>
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

# ════════════════════════════════════════════════════════════════════════════
# 4 ── VIBE GRID
# ════════════════════════════════════════════════════════════════════════════
VIBES = [
    ("https://images.unsplash.com/photo-1566937169390-b55a2639aad3?w=300&h=300&fit=crop&q=75","🌅","Apéro Sunset"),
    ("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=300&h=300&fit=crop&q=75","🍟","Petits Prix"),
    ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&h=300&fit=crop&q=75","🏖️","Journée Plage"),
    ("https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?w=300&h=300&fit=crop&q=75","🎉","Nuit à Marseille"),
    ("https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=300&h=300&fit=crop&q=75","☕","Café Tranquille"),
    ("https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=300&h=300&fit=crop&q=75","👯","Entre Amis"),
    ("https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=300&h=300&fit=crop&q=75","🤫","Plan de Local"),
    ("https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=300&h=300&fit=crop&q=75","🍽️","Vrai Dîner"),
]

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="sec">
  <div class="sec-hdr">
    <h2>Choisis ton <em>vibe</em></h2>
    <span class="see-all">Tout voir →</span>
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

# ════════════════════════════════════════════════════════════════════════════
# 5 ── COMMUNITY VOICES
# ════════════════════════════════════════════════════════════════════════════
POSTS = [
    {"author":"Julien M.","role":"Étudiant en design, AMU","avatar":"https://i.pravatar.cc/80?img=7",
     "quote":"Le meilleur moment pour voir la ville c'est à 6h quand le soleil tape sur le Mucem. Toute la ville se réveille d'un rêve.",
     "tag":"Mucem au lever du soleil","accent":"cc-blue"},
    {"author":"Anaëlis R.","role":"Arrivée de Lyon récemment","avatar":"https://i.pravatar.cc/80?img=47",
     "quote":"Je peux pas te filer la recette de la bouillabaisse, mais je sais où trouver le meilleur rouget au marché de Noailles le matin.",
     "tag":"Marché Noailles","accent":"cc-yellow"},
    {"author":"Marco S.","role":"Graphiste, Marseillais de souche","avatar":"https://i.pravatar.cc/80?img=60",
     "quote":"La scène street art change toutes les semaines. Nouvelle galerie derrière le métro chaque mois. Cette ville ne s'arrête jamais.",
     "tag":"Street art tour","accent":"cc-green"},
]

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="sec">
  <div class="sec-hdr" style="margin-bottom:1rem;">
    <h2>🌊 Les <em>locaux</em> parlent</h2>
    <span class="see-all">Toutes les histoires →</span>
  </div>
  <div class="community-grid">
""", unsafe_allow_html=True)

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
      <div class="cc-quote">« {p['quote']} »</div>
      <span class="cc-tag">📍 {p['tag']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 6 ── SHARE A SPOT
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="share-sec">
  <div class="sec-hdr" style="margin-bottom:1rem;">
    <h2>✍️ Partage ta <em>pépite</em></h2>
  </div>
""", unsafe_allow_html=True)

with st.form("share_form", clear_on_submit=True):
    fs1, fs2 = st.columns(2)
    with fs1:
        s_name = st.text_input("Nom du spot *", placeholder="ex. Chez Jeannot")
        s_vibe = st.text_input("Quartier / ambiance", placeholder="ex. Le Panier, cash only")
    with fs2:
        s_cat   = st.selectbox("Type", ["Panisse 🍟","Pastis 🥛","Fougasse 🫓","Autre 🍽️"])
        s_price = st.selectbox("Prix", ["€ moins de 10€","€€ 10–20€","€€€ 20€+"])
    s_tip    = st.text_area("Ton bon plan *", placeholder="Quoi commander, meilleur horaire, le truc que personne sait…", height=80)
    s_author = st.text_input("Ton prénom", placeholder="ex. Théo, étudiant")
    sub = st.form_submit_button("🌊 Ajouter à la carte")
    if sub:
        if s_name and s_tip:
            st.success(f"🎉 Merci ! **{s_name}** est maintenant sur la carte Massilia.")
        else:
            st.warning("Remplis au moins le nom du spot et ton bon plan.")

st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 7 ── NEWSLETTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="newsletter">
  <h2>La newsletter des initiés.</h2>
  <p>Pas de spam. Seulement les ouvertures secrètes, les événements locaux,<br>et les meilleures planques loin des touristes cet été.</p>
  <div style="display:flex;gap:0.6rem;max-width:420px;margin:0 auto;flex-wrap:wrap;justify-content:center;">
    <input type="email" placeholder="Ton adresse email"
      style="border-radius:50px;border:none;padding:0.65rem 1.3rem;
             font-family:Nunito,sans-serif;font-size:0.9rem;flex:1;min-width:190px;
             outline:none;color:#1A2540;"/>
    <button style="background:#F5B800;color:#1A2540;border:none;border-radius:50px;
                   padding:0.65rem 1.5rem;font-family:Nunito,sans-serif;font-weight:900;
                   font-size:0.9rem;cursor:pointer;white-space:nowrap;">S'inscrire</button>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  <div style="display:flex;justify-content:center;margin-bottom:0.6rem;">
    <img src="{LOGO_DATA}" style="height:52px;width:auto;opacity:0.9;" alt="Massilia"/>
  </div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-style:italic;margin:0.4rem 0 1.2rem;">
    Pas fâché avec le plaisir 🌊
  </div>
  <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1.2rem;">
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Explorer</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Carte</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Communauté</a>
    <a href="#" style="color:rgba(255,255,255,0.5);font-size:0.85rem;text-decoration:none;">Contact</a>
  </div>
  <div style="font-size:0.72rem;color:rgba(255,255,255,0.25);">© 2025 Massilia · Panis · Pastis · Fougasse</div>
</div>
""", unsafe_allow_html=True)
