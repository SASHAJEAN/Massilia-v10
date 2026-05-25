import streamlit as st
import anthropic
import base64, pathlib

st.set_page_config(
    page_title="Massilia 🌊",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Encode uploaded brand images to base64 so they work in HTML ───────────────
def img_b64(path):
    try:
        data = pathlib.Path(path).read_bytes()
        ext  = pathlib.Path(path).suffix.lstrip(".")
        mime = "image/jpeg" if ext in ("jpg","jpeg") else "image/png"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return ""

LOGO_SRC    = img_b64("/mnt/user-data/uploads/5.jpg")   # full wordmark logo
PATTERN_SRC = img_b64("/mnt/user-data/uploads/8.jpg")   # pastis/fougasse pattern
ICON_SRC    = img_b64("/mnt/user-data/uploads/9.jpg")   # app icon (yellow bg)

# ── Session state ──────────────────────────────────────────────────────────────
if "screen"   not in st.session_state: st.session_state.screen   = "onboard"
if "mood"     not in st.session_state: st.session_state.mood     = "😎 Chill"
if "messages" not in st.session_state: st.session_state.messages = []
if "ai_input" not in st.session_state: st.session_state.ai_input = ""
if "loading"  not in st.session_state: st.session_state.loading  = False

# ── Navigation helper ─────────────────────────────────────────────────────────
def go(screen): st.session_state.screen = screen; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css');

:root {{
  --blue:   #29B6F6;
  --yellow: #F5B800;
  --beige:  #FDF6EC;
  --dark:   #1A1A2E;
  --coral:  #E8704A;
  --text:   #2C2C3E;
  --muted:  #888898;
  --card:   #fff;
  --border: rgba(0,0,0,0.08);
}}

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"],
section.main > div.block-container {{
  background: transparent !important;
  font-family: 'Nunito', sans-serif !important;
  padding: 0 !important;
  max-width: 100% !important;
}}

/* page backdrop = pastis pattern */
[data-testid="stAppViewContainer"] {{
  background-image: url('{PATTERN_SRC}') !important;
  background-size: 320px auto !important;
  background-repeat: repeat !important;
  background-attachment: fixed !important;
}}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"] {{ display: none !important; }}

/* ── PAGE CENTERING ── */
.page-wrap {{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 2rem 1rem 3rem;
  gap: 2rem;
  flex-wrap: wrap;
}}

/* ── PHONE FRAME ── */
.phone-frame {{
  width: 340px;
  flex-shrink: 0;
  background: #111;
  border-radius: 40px;
  padding: 12px;
  box-shadow: 0 32px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.08) inset;
}}
.phone-screen {{
  width: 316px;
  min-height: 640px;
  max-height: 680px;
  border-radius: 30px;
  overflow: hidden;
  background: var(--beige);
  position: relative;
  display: flex;
  flex-direction: column;
}}

/* ── SCROLLABLE CONTENT AREA ── */
.screen-scroll {{
  flex: 1;
  overflow-y: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
}}
.screen-scroll::-webkit-scrollbar {{ display: none; }}

/* ── BOTTOM NAV ── */
.bottom-nav {{
  display: flex;
  background: var(--card);
  border-top: 0.5px solid var(--border);
  padding: 8px 0 6px;
  flex-shrink: 0;
}}
.nav-item {{
  flex: 1; display: flex; flex-direction: column;
  align-items: center; gap: 2px;
  cursor: pointer; padding: 2px 0;
  color: var(--muted); font-size: 10px;
  transition: color 0.15s;
  border: none; background: none;
  font-family: 'Nunito', sans-serif;
}}
.nav-item.active {{ color: var(--blue); }}
.nav-item i {{ font-size: 20px; }}
.nav-item.ai-btn .nav-dot {{
  width: 40px; height: 40px;
  background: var(--yellow);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin-top: -8px;
  border: 3px solid var(--beige);
  font-size: 18px; color: var(--dark);
}}

/* ── ONBOARDING ── */
.onboard-bg {{
  background: linear-gradient(160deg, #29B6F6 0%, #0288D1 100%);
  min-height: 640px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 2rem 1.5rem;
  text-align: center;
  position: relative; overflow: hidden;
}}
.onboard-pattern-overlay {{
  position: absolute; inset: 0; opacity: 0.07;
  background-image: url('{PATTERN_SRC}');
  background-size: 120px auto;
  pointer-events: none;
}}
.onboard-logo-img {{
  width: 200px; height: auto;
  filter: brightness(0) invert(1);
  position: relative; z-index: 1;
  margin-bottom: 0.5rem;
}}
.onboard-tagline {{
  font-size: 22px; font-weight: 700;
  color: #fff; margin-top: 1.5rem;
  line-height: 1.35; position: relative; z-index: 1;
}}
.onboard-tagline em {{ color: var(--yellow); font-style: normal; }}
.onboard-desc {{
  font-size: 13px; color: rgba(255,255,255,0.82);
  margin-top: 0.8rem; line-height: 1.6;
  position: relative; z-index: 1; max-width: 260px;
}}
.pill-row {{
  display: flex; gap: 8px; margin-top: 1.5rem;
  position: relative; z-index: 1; flex-wrap: wrap; justify-content: center;
}}
.icon-pill {{
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 999px;
  padding: 7px 14px;
  font-size: 12px; color: #fff;
  display: flex; align-items: center; gap: 5px;
}}
.cta-btn {{
  margin-top: 1.5rem;
  background: var(--yellow); color: var(--dark);
  border: none; padding: 14px 36px;
  border-radius: 999px; font-size: 15px;
  font-weight: 700; cursor: pointer;
  position: relative; z-index: 1;
  font-family: 'Nunito', sans-serif;
  transition: transform 0.15s;
}}
.cta-btn:hover {{ transform: scale(1.04); }}

/* ── HOME ── */
.home-header {{
  background: var(--blue);
  padding: 1.1rem 1.2rem 1rem;
}}
.home-topbar {{
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 0.75rem;
}}
.home-logo-img {{
  height: 28px; width: auto;
  filter: brightness(0) invert(1);
}}
.home-avatar {{
  width: 34px; height: 34px; border-radius: 50%;
  background: var(--yellow);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: var(--dark);
}}
.home-greeting {{ font-size: 20px; font-weight: 700; color: #fff; line-height: 1.25; }}
.home-greeting span {{ color: var(--yellow); }}
.home-subtext {{ font-size: 11px; color: rgba(255,255,255,0.72); margin-top: 3px; }}

.mood-bar {{
  background: var(--card);
  margin: 0 1rem; margin-top: -14px;
  border-radius: 14px; padding: 0.85rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}}
.mood-label {{ font-size: 10px; font-weight: 700; color: var(--muted); letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase; }}
.mood-chips {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.mood-chip {{
  padding: 5px 11px; border-radius: 999px;
  background: var(--beige); border: 1.5px solid var(--border);
  font-size: 11px; cursor: pointer; color: var(--text);
  font-family: 'Nunito', sans-serif; transition: all 0.15s;
}}
.mood-chip.sel {{
  background: var(--yellow); border-color: var(--yellow);
  color: var(--dark); font-weight: 700;
}}

.ai-shortcut {{
  margin: 0.75rem 1rem;
  background: var(--dark); border-radius: 12px;
  padding: 11px 13px;
  display: flex; align-items: center; gap: 10px;
  cursor: pointer;
}}
.ai-s-icon {{
  width: 32px; height: 32px; background: var(--yellow);
  border-radius: 8px; display: flex; align-items: center;
  justify-content: center; font-size: 15px; flex-shrink: 0;
}}
.ai-s-label {{ font-size: 10px; color: rgba(255,255,255,0.55); text-transform: uppercase; letter-spacing: 0.5px; }}
.ai-s-prompt {{ font-size: 12px; color: #fff; font-weight: 600; }}

.sec-row {{
  display: flex; justify-content: space-between;
  align-items: center; padding: 0.85rem 1.2rem 0.4rem;
}}
.sec-title {{ font-size: 14px; font-weight: 700; color: var(--text); }}
.sec-more  {{ font-size: 11px; color: var(--blue); cursor: pointer; }}

.h-scroll {{
  display: flex; gap: 10px;
  padding: 0 1.2rem 0.75rem;
  overflow-x: auto; scrollbar-width: none;
}}
.h-scroll::-webkit-scrollbar {{ display: none; }}

.place-card {{
  min-width: 130px; max-width: 130px;
  background: var(--card); border-radius: 14px;
  overflow: hidden; border: 0.5px solid var(--border);
  cursor: pointer; transition: transform 0.15s; flex-shrink: 0;
}}
.place-card:hover {{ transform: translateY(-2px); }}
.place-img {{
  height: 72px; width: 100%;
  object-fit: cover; display: block;
}}
.place-img-emoji {{
  height: 72px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
}}
.place-info {{ padding: 7px 9px 9px; }}
.place-name {{ font-size: 11px; font-weight: 700; color: var(--text); line-height: 1.2; }}
.place-type {{ font-size: 9px; color: var(--muted); margin-top: 1px; }}
.place-tags {{ display: flex; gap: 3px; margin-top: 4px; flex-wrap: wrap; }}
.place-tag {{
  font-size: 9px; padding: 2px 5px;
  border-radius: 999px;
  background: var(--beige); color: var(--text);
  border: 0.5px solid var(--border);
}}
.price-rating {{ font-size: 9px; font-weight: 700; color: var(--coral); margin-top: 4px; }}

/* ── AI CHAT ── */
.ai-header {{
  background: var(--dark);
  padding: 1.1rem 1.2rem 1.3rem;
  flex-shrink: 0;
}}
.ai-header-row {{ display: flex; align-items: center; gap: 10px; }}
.ai-header-icon {{
  width: 36px; height: 36px; background: var(--yellow);
  border-radius: 10px; display: flex; align-items: center;
  justify-content: center; font-size: 18px;
}}
.ai-title {{ font-size: 17px; font-weight: 700; color: #fff; }}
.ai-subtitle {{ font-size: 11px; color: rgba(255,255,255,0.55); margin-top: 2px; }}

.bubbles-wrap {{ padding: 0.85rem 1.1rem; display: flex; flex-direction: column; gap: 10px; }}
.bubble {{
  padding: 10px 13px; border-radius: 16px;
  font-size: 12px; line-height: 1.5; max-width: 88%;
}}
.bubble.ai {{
  background: var(--card); border: 0.5px solid var(--border);
  border-bottom-left-radius: 4px; color: var(--text); align-self: flex-start;
}}
.bubble.user {{
  background: var(--blue); color: #fff;
  border-bottom-right-radius: 4px; align-self: flex-end;
}}
.bubble.result {{
  background: var(--yellow); color: var(--dark);
  border-bottom-left-radius: 4px; align-self: flex-start; max-width: 100%;
}}

.result-card {{
  background: var(--card); border-radius: 14px;
  margin: 0 1.1rem; padding: 13px;
  border: 0.5px solid var(--border);
}}
.rc-label {{ font-size: 9px; font-weight: 700; color: var(--blue); letter-spacing: 1px; margin-bottom: 7px; text-transform: uppercase; }}
.rc-row {{ display: flex; gap: 9px; align-items: flex-start; }}
.rc-emoji {{ font-size: 26px; }}
.rc-name {{ font-size: 14px; font-weight: 700; color: var(--text); }}
.rc-desc {{ font-size: 10px; color: var(--muted); margin-top: 1px; }}
.rc-badges {{ display: flex; gap: 4px; margin-top: 8px; flex-wrap: wrap; }}
.rc-badge {{ font-size: 9px; padding: 3px 7px; border-radius: 999px; font-weight: 600; }}
.rb-blue   {{ background: #E3F2FD; color: #0277BD; }}
.rb-yellow {{ background: #FFF8E1; color: #E65100; }}
.rb-green  {{ background: #E8F5E9; color: #2E7D32; }}
.rc-tip {{ margin-top: 9px; font-size: 10px; color: var(--muted); line-height: 1.5; }}
.rc-actions {{ display: flex; gap: 7px; margin-top: 9px; }}
.rc-btn {{
  flex: 1; border: none; border-radius: 8px;
  padding: 8px; font-size: 11px; font-weight: 600;
  cursor: pointer; font-family: 'Nunito', sans-serif;
}}
.rc-btn.map  {{ background: var(--blue);   color: #fff; }}
.rc-btn.save {{ background: var(--yellow); color: var(--dark); }}

/* ── EXPLORE ── */
.explore-header {{
  background: var(--blue); padding: 1.1rem 1.2rem;
}}
.search-bar {{
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 999px; padding: 9px 13px;
  display: flex; align-items: center; gap: 7px;
  color: rgba(255,255,255,0.8); font-size: 12px;
  cursor: pointer; margin-top: 0.6rem;
}}
.filter-row {{
  display: flex; gap: 6px; margin-top: 9px;
  overflow-x: auto; scrollbar-width: none;
}}
.filter-row::-webkit-scrollbar {{ display: none; }}
.filter-chip {{
  padding: 5px 11px; border-radius: 999px;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  font-size: 10px; color: #fff; white-space: nowrap;
  cursor: pointer; transition: all 0.15s;
}}
.filter-chip.on {{ background: var(--yellow); border-color: var(--yellow); color: var(--dark); font-weight: 700; }}

.map-area {{
  background: #C8E6C9; height: 155px;
  position: relative; overflow: hidden;
}}
.map-grid-bg {{
  position: absolute; inset: 0;
  background-image:
    repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0, rgba(0,0,0,0.05) 1px, transparent 0, transparent 38px),
    repeating-linear-gradient(90deg, rgba(0,0,0,0.05) 0, rgba(0,0,0,0.05) 1px, transparent 0, transparent 38px);
}}
.map-pin {{
  position: absolute; display: flex; flex-direction: column; align-items: center; cursor: pointer;
}}
.map-pin-dot {{
  width: 26px; height: 26px; border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  display: flex; align-items: center; justify-content: center;
  border: 2px solid #fff;
}}
.map-pin-dot span {{ transform: rotate(45deg); font-size: 11px; }}
.map-pin-label {{
  font-size: 8px; font-weight: 700; background: #fff;
  border-radius: 4px; padding: 1px 4px;
  color: var(--text); margin-top: 2px; white-space: nowrap;
}}
.map-badge {{
  position: absolute; bottom: 7px; right: 7px;
  background: #fff; border-radius: 7px; padding: 4px 9px;
  font-size: 9px; font-weight: 600; color: var(--text);
}}

.list-card {{
  margin: 0 1.1rem 9px;
  background: var(--card); border-radius: 13px;
  padding: 11px; display: flex; gap: 11px;
  align-items: center; border: 0.5px solid var(--border);
  cursor: pointer; transition: transform 0.15s;
}}
.list-card:hover {{ transform: translateX(2px); }}
.list-emoji {{ font-size: 28px; width: 42px; text-align: center; }}
.list-info {{ flex: 1; }}
.list-name {{ font-size: 12px; font-weight: 700; color: var(--text); }}
.list-meta {{ font-size: 10px; color: var(--muted); margin-top: 1px; }}
.list-right {{ text-align: right; }}
.list-price  {{ font-size: 10px; font-weight: 700; color: var(--coral); }}
.list-rating {{ font-size: 10px; color: var(--yellow); }}

/* ── PROFILE ── */
.profile-hdr {{
  background: var(--dark);
  padding: 1.4rem 1.2rem 1.8rem;
  text-align: center;
}}
.profile-av {{
  width: 60px; height: 60px; border-radius: 50%;
  background: var(--yellow);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; color: var(--dark);
  margin: 0 auto 9px;
  border: 3px solid rgba(255,255,255,0.2);
}}
.profile-name-txt {{ font-size: 17px; font-weight: 700; color: #fff; }}
.profile-handle   {{ font-size: 11px; color: rgba(255,255,255,0.48); margin-top: 2px; }}
.profile-loc      {{ font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 3px; }}
.profile-stats {{
  display: flex; justify-content: center; gap: 22px; margin-top: 13px;
}}
.stat {{ text-align: center; }}
.stat-num   {{ font-size: 17px; font-weight: 700; color: #fff; }}
.stat-label {{ font-size: 9px;  color: rgba(255,255,255,0.45); margin-top: 1px; }}

.badges-row {{
  display: flex; gap: 7px; padding: 0.85rem 1.2rem;
  overflow-x: auto; scrollbar-width: none;
}}
.badges-row::-webkit-scrollbar {{ display: none; }}
.badge-card {{
  min-width: 68px; background: var(--card);
  border-radius: 12px; padding: 9px 7px;
  text-align: center; border: 0.5px solid var(--border);
}}
.badge-emoji  {{ font-size: 20px; }}
.badge-name   {{ font-size: 9px; color: var(--muted); margin-top: 3px; line-height: 1.3; }}
.badge-unlock {{ font-size: 8px; font-weight: 700; color: var(--blue); margin-top: 1px; }}

.fav-grid {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 7px;
  padding: 0 1.2rem 0.85rem;
}}
.fav-card {{
  background: var(--card); border-radius: 11px;
  padding: 11px; border: 0.5px solid var(--border);
}}
.fav-emoji {{ font-size: 18px; }}
.fav-name  {{ font-size: 10px; font-weight: 700; color: var(--text); margin-top: 3px; }}
.fav-type  {{ font-size: 9px;  color: var(--muted); }}

.prefs-card {{
  background: var(--card); border-radius: 12px;
  border: 0.5px solid var(--border); overflow: hidden;
  margin: 0 1.2rem 0.85rem;
}}
.pref-row {{
  padding: 10px 13px; border-bottom: 0.5px solid var(--border);
  display: flex; justify-content: space-between; font-size: 11px;
}}
.pref-row:last-child {{ border-bottom: none; }}
.pref-key   {{ color: var(--text); font-weight: 600; }}
.pref-value {{ color: var(--blue); font-weight: 700; }}

/* ── SIDEBAR PANEL ── */
.side-panel {{
  width: 300px; flex-shrink: 0;
}}
.side-card {{
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  border-radius: 18px; padding: 1.2rem 1.3rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(255,255,255,0.6);
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}
.side-card h3 {{ font-size: 13px; font-weight: 800; color: var(--text); margin-bottom: 0.6rem; }}
.side-nav-btn {{
  width: 100%; display: flex; align-items: center; gap: 10px;
  background: var(--beige); border: 1.5px solid var(--border);
  border-radius: 999px; padding: 9px 16px;
  font-size: 13px; color: var(--text); font-weight: 600;
  cursor: pointer; margin-bottom: 6px;
  font-family: 'Nunito', sans-serif; transition: all 0.15s;
}}
.side-nav-btn:hover, .side-nav-btn.active {{
  background: var(--yellow); border-color: var(--yellow); color: var(--dark);
}}
.arch-dot {{
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}}
.arch-row {{
  display: flex; align-items: center; gap: 8px;
  padding: 5px 0; border-bottom: 0.5px solid rgba(0,0,0,0.06);
  font-size: 11px; color: #555;
}}
.arch-row:last-child {{ border-bottom: none; }}
.arch-row b {{ font-weight: 700; color: var(--text); }}

/* ── STREAMLIT WIDGET OVERRIDES (inside AI form) ── */
div.stButton > button {{
  background: var(--yellow) !important; color: var(--dark) !important;
  font-family: 'Nunito', sans-serif !important; font-weight: 800 !important;
  font-size: 0.9rem !important; border-radius: 999px !important;
  border: none !important; padding: 0.6rem 1.5rem !important;
  width: 100% !important; transition: all 0.2s !important;
}}
div.stButton > button:hover {{ background: var(--blue) !important; color: #fff !important; }}
div[data-baseweb="select"] > div {{
  border-radius: 999px !important; font-family: 'Nunito', sans-serif !important;
  font-weight: 600 !important; background: var(--beige) !important;
  border-color: var(--border) !important; color: var(--text) !important;
}}
textarea {{
  border-radius: 14px !important; font-family: 'Nunito', sans-serif !important;
  font-size: 12px !important; background: var(--beige) !important;
  color: var(--text) !important; border-color: var(--border) !important;
}}
textarea::placeholder {{ color: var(--muted) !important; }}
[data-testid="stSlider"] div[role="slider"] {{ background: var(--blue) !important; }}
[data-testid="stForm"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
div[data-testid="column"] {{ padding: 0 0.25rem !important; }}
[data-testid="stCaptionContainer"] {{ color: var(--muted) !important; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPER — bottom nav HTML
# ══════════════════════════════════════════════════════════════════════════════
def bottom_nav(active):
    screens = [
        ("home",    "ti-home",    "Home"),
        ("explore", "ti-compass", "Explore"),
        ("ai",      None,         "AI"),
        ("saved",   "ti-heart",   "Saved"),
        ("profile", "ti-user",    "Me"),
    ]
    html = '<div class="bottom-nav">'
    for s, icon, label in screens:
        a = "active" if s == active else ""
        if s == "ai":
            html += f'<button class="nav-item ai-btn {a}" onclick="window.parent.postMessage(\'go:{s}\',\'*\')"><div class="nav-dot">✨</div><span style="margin-top:2px;font-size:9px;">{label}</span></button>'
        else:
            html += f'<button class="nav-item {a}" onclick="window.parent.postMessage(\'go:{s}\',\'*\')"><i class="ti {icon}"></i><span>{label}</span></button>'
    html += '</div>'
    return html

# ══════════════════════════════════════════════════════════════════════════════
# SCREEN BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def screen_onboard():
    return f"""
<div class="onboard-bg">
  <div class="onboard-pattern-overlay"></div>
  <img src="{LOGO_SRC}" class="onboard-logo-img" alt="Massilia"/>
  <div class="onboard-tagline">Discover Marseille<br>like a <em>local.</em></div>
  <div class="onboard-desc">AI-powered recs for pastis bars, panisse spots, hidden gems & sunset apéros — based on your mood, budget & vibe.</div>
  <div class="pill-row">
    <div class="icon-pill">🧠 AI-powered</div>
    <div class="icon-pill">📍 Hyperlocal</div>
  </div>
  <div class="pill-row" style="margin-top:6px;">
    <div class="icon-pill">🥂 Pastis</div>
    <div class="icon-pill">🥘 Panisse</div>
    <div class="icon-pill">🫓 Fougasse</div>
  </div>
  <button class="cta-btn" onclick="window.parent.postMessage('go:home','*')">Start exploring →</button>
  <div style="font-size:11px;color:rgba(255,255,255,0.55);margin-top:10px;position:relative;z-index:1;">Already have an account? Sign in</div>
</div>
"""

def screen_home():
    mood = st.session_state.mood
    moods = ["😎 Chill","🔥 Party","❤️ Romantic","👨‍👩‍👧 Family","🎒 Solo"]
    chips = "".join([
        f'<div class="mood-chip {"sel" if m==mood else ""}" onclick="window.parent.postMessage(\'mood:{m}\',\'*\')">{m}</div>'
        for m in moods
    ])
    return f"""
<div class="screen-scroll">
  <div class="home-header">
    <div class="home-topbar">
      <img src="{LOGO_SRC}" class="home-logo-img" alt="Massilia"/>
      <div class="home-avatar">JM</div>
    </div>
    <div class="home-greeting">Salut Julien 👋<br>What's your <span>vibe today?</span></div>
    <div class="home-subtext">📍 Vieux-Port · 22°C ☀️ · 18:30</div>
  </div>
  <div class="mood-bar">
    <div class="mood-label">YOUR MOOD RIGHT NOW</div>
    <div class="mood-chips">{chips}</div>
  </div>
  <div class="ai-shortcut" onclick="window.parent.postMessage('go:ai','*')">
    <div class="ai-s-icon">✨</div>
    <div style="flex:1;">
      <div class="ai-s-label">ASK THE AI CONCIERGE</div>
      <div class="ai-s-prompt">"Chill sunset apéro near the sea, under €12"</div>
    </div>
    <i class="ti ti-chevron-right" style="color:rgba(255,255,255,0.4);font-size:17px;"></i>
  </div>
  <div class="sec-row"><div class="sec-title">🌅 Perfect for tonight</div><div class="sec-more">See all</div></div>
  <div class="h-scroll">
    <div class="place-card"><div class="place-img-emoji" style="background:#FFF9C4;">🌊</div><div class="place-info"><div class="place-name">Bar de la Marine</div><div class="place-type">Pastis · Vieux-Port</div><div class="place-tags"><div class="place-tag">Sunset</div><div class="place-tag">Terrace</div></div><div class="price-rating">€€ · 4.8 ★</div></div></div>
    <div class="place-card"><div class="place-img-emoji" style="background:#E3F2FD;">🏖️</div><div class="place-info"><div class="place-name">L'Escale Borely</div><div class="place-type">Beach bar · Borely</div><div class="place-tags"><div class="place-tag">Beach</div><div class="place-tag">DJ</div></div><div class="price-rating">€€ · 4.6 ★</div></div></div>
    <div class="place-card"><div class="place-img-emoji" style="background:#F3E5F5;">🎸</div><div class="place-info"><div class="place-name">Le Café Julien</div><div class="place-type">Wine · Cours Julien</div><div class="place-tags"><div class="place-tag">Live music</div></div><div class="price-rating">€ · 4.9 ★</div></div></div>
    <div class="place-card"><div class="place-img-emoji" style="background:#E8F5E9;">🌿</div><div class="place-info"><div class="place-name">La Friche</div><div class="place-type">Urban · Belle de Mai</div><div class="place-tags"><div class="place-tag">Artsy</div></div><div class="price-rating">€€ · 4.7 ★</div></div></div>
  </div>
  <div class="sec-row"><div class="sec-title">🥘 Panisse spots</div><div class="sec-more">See all</div></div>
  <div class="h-scroll">
    <div class="place-card"><div class="place-img-emoji" style="background:#FFF3E0;">🫔</div><div class="place-info"><div class="place-name">Chez Etienne</div><div class="place-type">Traditional · Panier</div><div class="place-tags"><div class="place-tag">Local</div><div class="place-tag">Cheap</div></div><div class="price-rating">€ · 5.0 ★</div></div></div>
    <div class="place-card"><div class="place-img-emoji" style="background:#FFF9C4;">🌾</div><div class="place-info"><div class="place-name">L'Épicerie du Midi</div><div class="place-type">Marché · Noailles</div><div class="place-tags"><div class="place-tag">Student</div></div><div class="price-rating">€ · 4.8 ★</div></div></div>
    <div class="place-card"><div class="place-img-emoji" style="background:#FCE4EC;">🫓</div><div class="place-info"><div class="place-name">Fougasserie Panier</div><div class="place-type">Bakery · Le Panier</div><div class="place-tags"><div class="place-tag">Hidden</div></div><div class="price-rating">€ · 4.7 ★</div></div></div>
  </div>
  <div style="height:60px;"></div>
</div>
{bottom_nav("home")}
"""

def screen_ai():
    msgs = st.session_state.messages
    bubble_html = ""
    for m in msgs:
        role_class = "user" if m["role"] == "user" else ("result" if m.get("result") else "ai")
        bubble_html += f'<div class="bubble {role_class}">{m["content"]}</div>'
    if not msgs:
        bubble_html = '<div class="bubble ai">Salut ! 🌊 Tell me your vibe, budget, who you\'re with, and what you fancy tonight...</div>'

    result_card = ""
    for m in msgs:
        if m.get("result"):
            result_card = f"""
<div class="result-card">
  <div class="rc-label">✨ AI TOP PICK</div>
  <div class="rc-row"><div class="rc-emoji">🌊</div><div><div class="rc-name">Bar de la Marine</div><div class="rc-desc">Vieux-Port · 10 min walk</div></div></div>
  <div class="rc-badges">
    <div class="rc-badge rb-blue">🎵 Electro nights</div>
    <div class="rc-badge rb-yellow">🥂 Pastis €4</div>
    <div class="rc-badge rb-green">💸 Avg €12pp</div>
  </div>
  <div class="rc-tip">Best sunset terrace on the Old Port. Locals love the Wednesday electro sessions. No tourist menu — real Marseille.</div>
  <div class="rc-actions">
    <button class="rc-btn map">See on map</button>
    <button class="rc-btn save">Save spot</button>
  </div>
</div>"""
            break

    return f"""
<div class="ai-header">
  <div class="ai-header-row">
    <div class="ai-header-icon">✨</div>
    <div>
      <div class="ai-title">AI Concierge</div>
      <div class="ai-subtitle">Describe your perfect Marseille moment</div>
    </div>
  </div>
</div>
<div class="screen-scroll" style="padding-bottom:0;">
  <div class="bubbles-wrap">{bubble_html}</div>
  {result_card}
  <div style="height:12px;"></div>
</div>
{bottom_nav("ai")}
"""

def screen_explore():
    return f"""
<div class="screen-scroll">
  <div class="explore-header">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <div style="font-size:16px;font-weight:700;color:#fff;">Explore Marseille</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.6);background:rgba(255,255,255,0.15);padding:4px 9px;border-radius:999px;">📍 Vieux-Port</div>
    </div>
    <div class="search-bar"><i class="ti ti-search" style="font-size:14px;"></i> Pastis, panisse, sunset bar...</div>
    <div class="filter-row">
      <div class="filter-chip on">All</div>
      <div class="filter-chip">🥂 Pastis</div>
      <div class="filter-chip">🥘 Panisse</div>
      <div class="filter-chip">🌅 Sunset</div>
      <div class="filter-chip">🏖️ Beach</div>
      <div class="filter-chip">🎵 Music</div>
    </div>
  </div>
  <div class="map-area">
    <div class="map-grid-bg"></div>
    <div class="map-pin" style="top:33%;left:36%;"><div class="map-pin-dot" style="background:#29B6F6;"><span>🥂</span></div><div class="map-pin-label">Marine</div></div>
    <div class="map-pin" style="top:52%;left:56%;"><div class="map-pin-dot" style="background:#F5B800;"><span>🥘</span></div><div class="map-pin-label">Étienne</div></div>
    <div class="map-pin" style="top:22%;left:63%;"><div class="map-pin-dot" style="background:#E8704A;"><span>🌅</span></div><div class="map-pin-label">Escale</div></div>
    <div class="map-badge">12 spots near you</div>
  </div>
  <div class="sec-row"><div class="sec-title">Nearby spots</div><div class="sec-more" onclick="window.parent.postMessage('go:ai','*')">Ask AI ✨</div></div>
  <div class="list-card"><div class="list-emoji">🥂</div><div class="list-info"><div class="list-name">Bar de la Marine</div><div class="list-meta">Pastis bar · Vieux-Port · 200m</div><div style="margin-top:3px;display:flex;gap:3px;"><span class="rc-badge rb-blue" style="font-size:8px;">Sunset</span><span class="rc-badge rb-yellow" style="font-size:8px;">Terrace</span></div></div><div class="list-right"><div class="list-price">€€</div><div class="list-rating">★ 4.8</div></div></div>
  <div class="list-card"><div class="list-emoji">🥘</div><div class="list-info"><div class="list-name">Chez Etienne</div><div class="list-meta">Panisse · Le Panier · 600m</div><div style="margin-top:3px;display:flex;gap:3px;"><span class="rc-badge rb-green" style="font-size:8px;">Local fave</span><span class="rc-badge rb-yellow" style="font-size:8px;">Student €</span></div></div><div class="list-right"><div class="list-price">€</div><div class="list-rating">★ 5.0</div></div></div>
  <div class="list-card"><div class="list-emoji">🌅</div><div class="list-info"><div class="list-name">Vallon des Auffes</div><div class="list-meta">Calanque · Endoume · 1.2km</div><div style="margin-top:3px;"><span class="rc-badge rb-blue" style="font-size:8px;">Hidden gem</span></div></div><div class="list-right"><div class="list-price">€€€</div><div class="list-rating">★ 4.9</div></div></div>
  <div style="height:60px;"></div>
</div>
{bottom_nav("explore")}
"""

def screen_profile():
    return f"""
<div class="screen-scroll">
  <div class="profile-hdr">
    <div class="profile-av">JM</div>
    <div class="profile-name-txt">Julien M.</div>
    <div class="profile-handle">@julien · Student, AMU</div>
    <div class="profile-loc">📍 Vieux-Port · Since 2024</div>
    <div class="profile-stats">
      <div class="stat"><div class="stat-num">47</div><div class="stat-label">Reviews</div></div>
      <div class="stat"><div class="stat-num">12</div><div class="stat-label">Lists</div></div>
      <div class="stat"><div class="stat-num">238</div><div class="stat-label">Following</div></div>
    </div>
  </div>
  <div class="sec-row" style="padding-top:0.7rem;"><div class="sec-title">🏆 Badges earned</div><div class="sec-more">All badges</div></div>
  <div class="badges-row">
    <div class="badge-card"><div class="badge-emoji">🥂</div><div class="badge-name">Pastis Pro</div><div class="badge-unlock">Unlocked</div></div>
    <div class="badge-card"><div class="badge-emoji">🌅</div><div class="badge-name">Sunset Chaser</div><div class="badge-unlock">Unlocked</div></div>
    <div class="badge-card"><div class="badge-emoji">🗺️</div><div class="badge-name">Explorer</div><div class="badge-unlock">Unlocked</div></div>
    <div class="badge-card" style="opacity:0.45;"><div class="badge-emoji">🔒</div><div class="badge-name">Fougasse Fan</div><div class="badge-unlock" style="color:var(--muted);">5 more</div></div>
    <div class="badge-card" style="opacity:0.45;"><div class="badge-emoji">🔒</div><div class="badge-name">Calanque King</div><div class="badge-unlock" style="color:var(--muted);">2 more</div></div>
  </div>
  <div class="sec-row" style="padding-top:0.2rem;"><div class="sec-title">❤️ My favourite spots</div><div class="sec-more">All</div></div>
  <div class="fav-grid">
    <div class="fav-card"><div class="fav-emoji">🥂</div><div class="fav-name">Bar de la Marine</div><div class="fav-type">Pastis · Vieux-Port</div></div>
    <div class="fav-card"><div class="fav-emoji">🥘</div><div class="fav-name">Chez Etienne</div><div class="fav-type">Panisse · Le Panier</div></div>
    <div class="fav-card"><div class="fav-emoji">🌊</div><div class="fav-name">Les Calanques</div><div class="fav-type">Nature · Cassis</div></div>
    <div class="fav-card"><div class="fav-emoji">🎵</div><div class="fav-name">Café Julien</div><div class="fav-type">Live music · C.Julien</div></div>
  </div>
  <div class="sec-row" style="padding-top:0.1rem;padding-bottom:0.5rem;"><div class="sec-title">⚙️ My preferences</div></div>
  <div class="prefs-card">
    <div class="pref-row"><span class="pref-key">Budget</span><span class="pref-value">€ — Student</span></div>
    <div class="pref-row"><span class="pref-key">Vibe</span><span class="pref-value">Chill / Local</span></div>
    <div class="pref-row"><span class="pref-key">Music</span><span class="pref-value">Electro / Jazz</span></div>
  </div>
  <div style="height:60px;"></div>
</div>
{bottom_nav("profile")}
"""

# ══════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
scr = st.session_state.screen

if   scr == "onboard": phone_html = screen_onboard()
elif scr == "home":    phone_html = screen_home()
elif scr == "ai":      phone_html = screen_ai()
elif scr == "explore": phone_html = screen_explore()
elif scr == "profile": phone_html = screen_profile()
else:                  phone_html = screen_home()

st.markdown(f"""
<div class="page-wrap">

  <!-- PHONE -->
  <div class="phone-frame">
    <div class="phone-screen">{phone_html}</div>
  </div>

  <!-- SIDEBAR -->
  <div class="side-panel">
    <div class="side-card">
      <h3>Navigate screens</h3>
      <button class="side-nav-btn {'active' if scr=='onboard' else ''}" onclick="window.parent.postMessage('go:onboard','*')">👋 Onboarding</button>
      <button class="side-nav-btn {'active' if scr=='home' else ''}"    onclick="window.parent.postMessage('go:home','*')">🏠 Home</button>
      <button class="side-nav-btn {'active' if scr=='ai' else ''}"      onclick="window.parent.postMessage('go:ai','*')">✨ AI Chat</button>
      <button class="side-nav-btn {'active' if scr=='explore' else ''}" onclick="window.parent.postMessage('go:explore','*')">🧭 Explore</button>
      <button class="side-nav-btn {'active' if scr=='profile' else ''}" onclick="window.parent.postMessage('go:profile','*')">👤 Profile</button>
    </div>
    <div class="side-card">
      <h3>App architecture</h3>
      <div class="arch-row"><div class="arch-dot" style="background:#29B6F6;"></div><b>Frontend</b> React Native + Expo</div>
      <div class="arch-row"><div class="arch-dot" style="background:#F5B800;"></div><b>Backend</b> Supabase + Edge Functions</div>
      <div class="arch-row"><div class="arch-dot" style="background:#E8704A;"></div><b>AI</b> Claude API (mood → rec engine)</div>
      <div class="arch-row"><div class="arch-dot" style="background:#66BB6A;"></div><b>Maps</b> Mapbox GL JS</div>
      <div class="arch-row"><div class="arch-dot" style="background:#AB47BC;"></div><b>Auth</b> Supabase Auth + Google SSO</div>
    </div>
  </div>

</div>

<script>
window.addEventListener('message', function(e) {{
  const d = e.data;
  if (typeof d === 'string') {{
    if (d.startsWith('go:'))   window.location.href = window.location.pathname + '?nav=' + d.slice(3);
    if (d.startsWith('mood:')) window.location.href = window.location.pathname + '?mood=' + encodeURIComponent(d.slice(5));
  }}
}});
</script>
""", unsafe_allow_html=True)

# ── Handle query-param navigation (postMessage → URL → st.query_params) ───────
params = st.query_params
if "nav" in params:
    new_screen = params["nav"]
    if new_screen != st.session_state.screen:
        st.session_state.screen = new_screen
        st.query_params.clear()
        st.rerun()
if "mood" in params:
    st.session_state.mood = params["mood"]
    st.query_params.clear()
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# AI CHAT FORM — below the phone, only visible on AI screen
# ══════════════════════════════════════════════════════════════════════════════
if scr == "ai":
    st.markdown("""
    <div style="display:flex;justify-content:center;margin-top:-1rem;padding-bottom:2rem;">
      <div style="width:340px;">
    """, unsafe_allow_html=True)

    with st.form("ai_form", clear_on_submit=True):
        user_input = st.text_area(
            "", placeholder="e.g. Chill sunset apéro near the sea, electro music, cheap pastis, under €15 with 3 friends",
            height=80, label_visibility="collapsed"
        )
        c1, c2 = st.columns(2)
        with c1:
            budget = st.selectbox("Budget", ["€ under €10","€€ €10–20","€€€ €20+"], label_visibility="collapsed")
        with c2:
            area   = st.selectbox("Area",   ["Vieux-Port","Cours Julien","Noailles","Endoume","Le Panier","Anywhere"], label_visibility="collapsed")
        send = st.form_submit_button("✨ Ask Massilia AI")

    if send and user_input.strip():
        st.session_state.messages.append({"role":"user","content": user_input.strip()})
        prompt = f"""You are Massilia, an AI guide for authentic Marseille food & lifestyle.
User: {user_input.strip()}
Budget: {budget}, Area: {area}

Give 3 hyperlocal Marseille spot recommendations. Focus on: pastis bars, panisse, fougasse, sunset bars, beach spots, hidden gems.
Format: **[Name]** · [area] — then 🍽️ Order, 💶 Price, 🌊 Vibe, 🔑 Tip on separate lines.
Be warm, fun, local. Occasional French. Short sign-off."""

        with st.spinner("Cherching les bons plans… 🌊"):
            try:
                client = anthropic.Anthropic()
                msg = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=800,
                    messages=[{"role":"user","content":prompt}]
                )
                reply = msg.content[0].text
            except Exception as e:
                reply = f"⚠️ {e}"

        st.session_state.messages.append({"role":"assistant","content":reply,"result":True})
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
