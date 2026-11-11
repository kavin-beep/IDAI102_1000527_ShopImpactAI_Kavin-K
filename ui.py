"""Shared presentation: the ShopImpact design system, animations and small HTML
components. Native Streamlit controls keep their semantics; decorative HTML is
aria-hidden or carries plain text so meaning never depends on colour or motion.
"""
from html import escape
from string import Template
import streamlit as st

# Vibrant category palette shared by every chart (text labels always accompany colour).
CATEGORY_COLORS = {
    "New clothing": "#F43F5E",
    "Second-hand clothing": "#10B981",
    "Leather footwear": "#F59E0B",
    "New electronics": "#8B5CF6",
    "Refurbished electronics": "#06B6D4",
    "Single-use household goods": "#FB7185",
    "Reusable household goods": "#84CC16",
    "Repair services": "#3B82F6",
}
CATEGORY_ICONS = {
    "New clothing": "👕", "Second-hand clothing": "🧥", "Leather footwear": "👞",
    "New electronics": "💻", "Refurbished electronics": "🔋", "Single-use household goods": "🧴",
    "Reusable household goods": "🫙", "Repair services": "🧵",
}


def theme_name():
    return st.session_state.get("visual_theme", "Normal")


def motion_on():
    return st.session_state.get("scenery_motion", True)


def theme_controls():
    """Theme and animation choices remain in this browser session."""
    with st.sidebar:
        with st.expander("🎨 Theme & animation", expanded=False):
            theme = st.selectbox("Theme", ["Normal", "Day", "Night"], key="visual_theme",
                                 help="Normal: fresh aurora · Day: sun and clouds · Night: stars and falling stars")
            motion = st.checkbox("Animated scenery", value=True, key="scenery_motion",
                                 help="Turns off background scenery and interface animations. Your device's reduced-motion setting is respected too.")
            st.caption("Applies to this session, including sign-in.")
    paused = "" if motion else " si-paused"
    if theme == "Night":
        content = "".join(f'<i class="si-star si-star-{n}"></i>' for n in range(1, 6))
        content += '<i class="si-moon"></i>'
        scene = "night"
    elif theme == "Day":
        content = '<i class="si-sun"></i><i class="si-cloud si-cloud-1"></i><i class="si-cloud si-cloud-2"></i><i class="si-cloud si-cloud-3"></i>'
        scene = "day"
    else:
        content = '<i class="si-blob si-blob-1"></i><i class="si-blob si-blob-2"></i><i class="si-blob si-blob-3"></i>'
        scene = "aurora"
    leaves = "".join(f'<i class="si-leaf si-leaf-{n}">{"🍃" if n % 2 else "🌿"}</i>' for n in range(1, 7)) if scene != "night" else ""
    st.markdown(f'<div class="si-scenery si-{scene}{paused}" aria-hidden="true">{content}{leaves}</div>', unsafe_allow_html=True)
    if not motion:
        st.markdown("<style>.stApp *,.stApp *::before,.stApp *::after{animation:none!important;transition:none!important;}</style>",
                    unsafe_allow_html=True)


BASE_CSS = Template(r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
@property --si-n {syntax:'<integer>';initial-value:0;inherits:false;}
.stApp {
  --si-bg:$bg; --si-surface:$surface; --si-solid:$solid; --si-muted:$muted; --si-ink:$ink; --si-line:$line;
  --si-primary:#0E9F6E; --si-primary-2:#14B8A6;
  --si-grad:linear-gradient(120deg,#10B981 0%,#14B8A6 30%,#3B82F6 65%,#8B5CF6 100%);
  --si-grad-warm:linear-gradient(120deg,#F59E0B,#F43F5E 55%,#EC4899);
  --si-grad-soft:linear-gradient(135deg,#ECFDF5,#E0F2FE 55%,#F5F3FF);
  --si-shadow:0 1px 2px rgba(15,46,37,.04),0 10px 30px -12px rgba(15,46,37,.18);
  --si-radius:20px;
  background:var(--si-bg); color:var(--si-ink);
  font-family:'Plus Jakarta Sans',ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;
}
.stApp p,.stApp li,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp h1,.stApp h2,.stApp h3,.stApp h4,
.stApp [data-baseweb="tab"] p,.stApp [data-testid="stMetricValue"] div {font-family:'Plus Jakarta Sans',ui-sans-serif,system-ui,sans-serif;}
.stApp h1 {font-size:clamp(1.9rem,3.4vw,3rem);font-weight:800;letter-spacing:-.045em;line-height:1.08;}
.stApp h2,.stApp h3 {letter-spacing:-.03em;font-weight:750;color:var(--si-ink);}
.stApp [data-testid="stHeader"] {background:transparent;}
.stApp [data-testid="stMainBlockContainer"] {max-width:1380px;padding-top:2.2rem;padding-bottom:4rem;position:relative;z-index:1;}
.stApp [data-testid="stCaptionContainer"] {opacity:1;}
.stApp [data-testid="stCaptionContainer"] p {color:var(--si-muted);line-height:1.6;}

/* Sidebar */
.stApp [data-testid="stSidebar"] {background:$sidebar;border-right:1px solid var(--si-line);backdrop-filter:blur(18px);}
.stApp [data-testid="stSidebar"] [data-testid="stExpander"] {background:var(--si-surface);}
.si-side-brand {display:flex;align-items:center;gap:12px;margin:4px 0 6px;}
.si-logo {width:46px;height:46px;border-radius:15px;display:grid;place-items:center;font-size:1.45rem;
  background:var(--si-grad);background-size:200% 200%;box-shadow:0 8px 22px -8px #10B98199;}
.si-side-brand b {font-size:1.35rem;letter-spacing:-.03em;color:var(--si-ink);display:block;line-height:1.1;}
.si-side-brand small {color:var(--si-muted);font-size:.78rem;}
.si-user {display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;background:var(--si-surface);
  border:1px solid var(--si-line);margin:14px 0 10px;box-shadow:var(--si-shadow);}
.si-avatar {width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-weight:800;color:#fff;
  background:var(--si-grad-warm);flex:none;}
.si-user b {color:var(--si-ink);display:block;font-size:.95rem;}
.si-user small {color:var(--si-muted);font-size:.78rem;}

/* Cards and surfaces */
.stApp [data-testid="stMetric"] {background:var(--si-surface);border:1px solid var(--si-line);border-radius:var(--si-radius);
  padding:22px 24px;min-height:128px;box-shadow:var(--si-shadow);position:relative;overflow:hidden;backdrop-filter:blur(14px);}
.stApp [data-testid="stMetric"]::before {content:"";position:absolute;inset:0 0 auto 0;height:4px;background:var(--si-grad);background-size:200% 100%;}
.stApp [data-testid="stMetricLabel"] p {color:var(--si-muted);font-size:.84rem;font-weight:600;letter-spacing:.01em;}
.stApp [data-testid="stMetricValue"] {font-size:clamp(1.45rem,2.4vw,2.1rem);font-weight:800;letter-spacing:-.04em;color:var(--si-ink);}
.st-key-kpis [data-testid="stMetric"]::after {position:absolute;right:18px;top:18px;font-size:1.6rem;width:48px;height:48px;
  border-radius:15px;display:grid;place-items:center;background:var(--si-grad-soft);}
.st-key-kpis [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"]::after {content:"💸";}
.st-key-kpis [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"]::after {content:"☁️";}
.st-key-kpis [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"]::after {content:"♻️";}
.st-key-kpis [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"]::before {background:linear-gradient(90deg,#06B6D4,#3B82F6,#8B5CF6);}
.st-key-kpis [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"]::before {background:linear-gradient(90deg,#84CC16,#10B981,#14B8A6);}
.stApp [data-testid="stForm"] {padding:24px;background:var(--si-surface);border:1px solid var(--si-line);border-radius:var(--si-radius);box-shadow:var(--si-shadow);}
.stApp [data-testid="stExpander"] {border:1px solid var(--si-line);border-radius:16px;background:var(--si-surface);overflow:hidden;}
.stApp [data-testid="stExpander"] summary:hover {background:rgba(16,185,129,.06);}
.stApp [class*="st-key-card"] {background:var(--si-surface);border:1px solid var(--si-line);border-radius:24px;padding:24px 26px;
  box-shadow:var(--si-shadow);backdrop-filter:blur(14px);}
.stApp .st-key-card_add {background:linear-gradient(var(--si-solid),var(--si-solid)) padding-box,var(--si-grad) border-box;
  border:2px solid transparent;}
.stApp [data-testid="stAlert"] {border-radius:14px;}
.stApp [data-testid="stDataFrame"] {border-radius:16px;overflow:hidden;border:1px solid var(--si-line);}
.stApp [data-testid="stVegaLiteChart"],.stApp [data-testid="stArrowVegaLiteChart"] {background:transparent;}

/* Buttons */
.stApp button {border-radius:12px;font-weight:650;transition:transform .18s ease,box-shadow .18s ease,background-color .18s ease,border-color .18s ease;}
.stApp [data-testid="stBaseButton-secondary"],.stApp [data-testid="stBaseButton-secondaryFormSubmit"] {background:var(--si-solid);border:1px solid var(--si-line);}
.stApp [data-testid="stBaseButton-secondary"]:hover,.stApp [data-testid="stBaseButton-secondaryFormSubmit"]:hover {
  border-color:#10B981;color:#0E9F6E;transform:translateY(-2px);box-shadow:0 8px 18px -10px #10B98188;}
.stApp [data-testid="stBaseButton-primary"],.stApp [data-testid="stBaseButton-primaryFormSubmit"],.stApp button[kind="primary"] {
  background:var(--si-grad);background-size:200% 100%;border:0;color:#fff;box-shadow:0 10px 24px -10px #10B981cc;
  position:relative;overflow:hidden;}
.stApp [data-testid="stBaseButton-primary"] p,.stApp [data-testid="stBaseButton-primaryFormSubmit"] p,.stApp button[kind="primary"] p {color:#fff;}
.stApp [data-testid="stBaseButton-primary"]:hover,.stApp [data-testid="stBaseButton-primaryFormSubmit"]:hover {
  transform:translateY(-2px) scale(1.01);box-shadow:0 16px 30px -12px #3B82F6cc;background-position:100% 0;color:#fff;}
.stApp [data-testid="stBaseButton-primary"]::after,.stApp [data-testid="stBaseButton-primaryFormSubmit"]::after {
  content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;transform:skewX(-20deg);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);}
.stApp button:active {transform:scale(.97);}
.stApp button:focus-visible,.stApp input:focus-visible,.stApp textarea:focus-visible {outline:3px solid #3B82F6;outline-offset:3px;}
.stApp [data-baseweb="input"],.stApp [data-baseweb="select"] > div,.stApp [data-baseweb="textarea"] {border-radius:12px;}

/* Tabs */
.stApp [data-baseweb="tab-list"] {gap:6px;padding:7px;background:var(--si-surface);border-radius:18px;border:1px solid var(--si-line);
  box-shadow:var(--si-shadow);backdrop-filter:blur(14px);overflow-x:auto;}
.stApp [data-baseweb="tab"] {padding:10px 16px;border-radius:12px;height:auto;transition:background-color .2s ease,color .2s ease;}
.stApp [data-baseweb="tab"]:hover {background:rgba(16,185,129,.08);}
.stApp [data-baseweb="tab"] p {font-weight:650;font-size:.92rem;}
.stApp [data-baseweb="tab"][aria-selected="true"] {background:var(--si-grad);box-shadow:0 8px 20px -10px #3B82F6aa;}
.stApp [data-baseweb="tab"][aria-selected="true"] p {color:#fff;}
.stApp [data-baseweb="tab-highlight"],.stApp [data-baseweb="tab-border"] {display:none;}
.stApp [data-testid="stTabs"] [role="tabpanel"] {padding-top:22px;}

/* Hero */
.si-hero {position:relative;overflow:hidden;border-radius:30px;padding:36px 40px;margin-bottom:26px;color:#fff;
  background:linear-gradient(120deg,#047857,#0D9488 30%,#2563EB 68%,#7C3AED);background-size:220% 220%;
  box-shadow:0 30px 60px -30px #1E3A8A99;display:grid;grid-template-columns:1.6fr 1fr;gap:28px;align-items:center;}
.si-hero::before {content:"";position:absolute;width:520px;height:520px;right:-140px;top:-220px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.28),transparent 65%);}
.si-hero::after {content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.18) 1px,transparent 1px);
  background-size:22px 22px;mask-image:linear-gradient(90deg,transparent,#000 70%);-webkit-mask-image:linear-gradient(90deg,transparent,#000 70%);pointer-events:none;}
.si-hero > * {position:relative;z-index:1;}
.si-hero h1 {margin:6px 0 12px;color:#fff;font-family:'Fraunces',Georgia,serif;font-weight:700;letter-spacing:-.03em;}
.si-hero p {margin:0;color:rgba(255,255,255,.86);line-height:1.7;max-width:640px;font-size:1.02rem;}
.si-hero .si-greet {font-weight:700;color:#D1FAE5;font-size:.95rem;letter-spacing:.02em;}
.si-shine {background:linear-gradient(90deg,#FDE68A,#FBCFE8,#A7F3D0,#FDE68A);background-size:300% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;}
.si-chip {display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.16);color:#fff;border:1px solid rgba(255,255,255,.28);
  border-radius:999px;padding:6px 12px;font-size:.76rem;font-weight:700;margin:0 8px 8px 0;backdrop-filter:blur(6px);}
.si-chip .si-dot {width:8px;height:8px;border-radius:50%;background:#A7F3D0;box-shadow:0 0 0 0 #A7F3D0;}
.si-hero-side {display:flex;flex-direction:column;align-items:center;gap:16px;}
.si-orb {position:relative;width:150px;height:150px;}
.si-orb svg {width:100%;height:100%;transform:rotate(-90deg);}
.si-orb .si-orb-in {position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.si-orb .si-orb-in span {font-size:2.4rem;line-height:1;}
.si-orb .si-orb-in b {font-size:.92rem;margin-top:6px;}
.si-orb .si-orb-in small {font-size:.72rem;opacity:.8;}
.si-mini {display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;}
.si-mini div {background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:10px 6px;text-align:center;backdrop-filter:blur(6px);}
.si-mini b {display:block;font-size:1.35rem;font-weight:800;}
.si-mini small {font-size:.7rem;opacity:.85;}
.si-count {--si-n:var(--to);counter-reset:si var(--si-n);}
.si-count::after {content:counter(si);}

/* Section headings */
.si-section {display:flex;align-items:center;gap:14px;margin:30px 0 14px;}
.si-section .si-ico {width:44px;height:44px;border-radius:14px;display:grid;place-items:center;font-size:1.3rem;flex:none;
  background:var(--si-grad-soft);border:1px solid var(--si-line);}
.si-section h3 {margin:0;padding:0;font-size:1.35rem;}
.si-section p {margin:2px 0 0;color:var(--si-muted);font-size:.9rem;}

/* Live estimate pill */
.si-estimate {display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;padding:14px 18px;border-radius:16px;margin:4px 0 14px;
  background:var(--si-grad-soft);border:1px dashed rgba(16,185,129,.45);color:var(--si-ink);}
.si-estimate b {font-size:1.25rem;background:var(--si-grad);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800;}
.si-estimate span {color:var(--si-muted);font-size:.86rem;}
.si-estimate .si-tag {padding:4px 10px;border-radius:999px;font-size:.75rem;font-weight:700;color:#065F46;background:#D1FAE5;}
.si-estimate .si-tag.si-new {color:#9F1239;background:#FFE4E6;}

/* Goal rings */
.si-rings {display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:8px 0 6px;}
.si-ring {display:flex;align-items:center;gap:16px;padding:16px;border-radius:20px;background:var(--si-surface);border:1px solid var(--si-line);box-shadow:var(--si-shadow);}
.si-ring-svg {position:relative;width:96px;height:96px;flex:none;}
.si-ring-svg svg {width:100%;height:100%;transform:rotate(-90deg);}
.si-ring-svg .si-track {stroke:var(--si-line);}
.si-ring-svg b {position:absolute;inset:0;display:grid;place-items:center;font-size:1.05rem;font-weight:800;color:var(--si-ink);}
.si-ring-txt strong {display:block;color:var(--si-ink);font-size:1rem;}
.si-ring-txt span {color:var(--si-muted);font-size:.84rem;line-height:1.5;}
.si-ring-txt em {display:inline-block;margin-top:6px;font-style:normal;font-size:.74rem;font-weight:700;padding:3px 9px;border-radius:999px;}
.si-ok {background:#D1FAE5;color:#065F46;} .si-over {background:#FFE4E6;color:#9F1239;}

/* Equivalents */
.si-equiv {display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.si-equiv div {position:relative;overflow:hidden;padding:20px;border-radius:20px;color:#fff;box-shadow:var(--si-shadow);}
.si-equiv div:nth-child(1) {background:linear-gradient(135deg,#F97316,#F43F5E);}
.si-equiv div:nth-child(2) {background:linear-gradient(135deg,#6366F1,#8B5CF6);}
.si-equiv div:nth-child(3) {background:linear-gradient(135deg,#10B981,#0D9488);}
.si-equiv i {position:absolute;right:-8px;bottom:-18px;font-size:4.6rem;font-style:normal;opacity:.28;}
.si-equiv b {display:block;font-size:2rem;font-weight:800;letter-spacing:-.03em;}
.si-equiv span {font-size:.86rem;opacity:.92;}

/* Alternatives */
.si-alts {display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.si-alt {padding:18px;border-radius:18px;background:var(--si-surface);border:1px solid var(--si-line);box-shadow:var(--si-shadow);
  transition:transform .25s ease,box-shadow .25s ease;}
.si-alt:hover {transform:translateY(-4px);box-shadow:0 18px 34px -18px #10B98188;}
.si-alt .si-num {width:34px;height:34px;border-radius:11px;display:grid;place-items:center;color:#fff;font-weight:800;background:var(--si-grad);margin-bottom:10px;}
.si-alt p {margin:0;color:var(--si-ink);font-weight:600;line-height:1.5;}

/* Tip, story, badges */
.si-tip {position:relative;padding:20px 22px;border-radius:20px;color:#3B0764;background:linear-gradient(135deg,#FEF3C7,#FCE7F3 60%,#EDE9FE);
  border:1px solid rgba(139,92,246,.18);}
.si-tip small {font-weight:800;letter-spacing:.12em;font-size:.68rem;color:#9D174D;}
.si-tip p {margin:8px 0 0;font-size:1rem;line-height:1.6;color:#3B0764;font-weight:600;}
.si-story {display:flex;gap:14px;align-items:flex-start;padding:16px 20px;border-radius:18px;background:var(--si-surface);border:1px solid var(--si-line);
  border-left:5px solid #8B5CF6;box-shadow:var(--si-shadow);margin:6px 0 18px;}
.si-story span {font-size:1.5rem;}
.si-story p {margin:0;color:var(--si-ink);line-height:1.6;}
.st-key-badges [data-testid="stAlert"] {background:linear-gradient(120deg,#FEF9C3,#DCFCE7,#CFFAFE);border:1px solid #FDE68A;
  box-shadow:0 10px 24px -14px #F59E0B;}
.st-key-badges [data-testid="stAlert"] p {color:#713F12;font-weight:750;}
.si-empty {text-align:center;padding:26px 18px;border-radius:20px;border:2px dashed var(--si-line);color:var(--si-muted);}
.si-empty span {display:block;font-size:2.4rem;margin-bottom:6px;}

/* Journey */
.si-level {display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;padding:26px;border-radius:26px;color:#fff;
  background:linear-gradient(120deg,#7C3AED,#2563EB 50%,#0D9488);background-size:200% 200%;box-shadow:0 26px 50px -28px #4C1D95;}
.si-level .si-big {font-size:4rem;width:110px;height:110px;border-radius:30px;display:grid;place-items:center;background:rgba(255,255,255,.16);}
.si-level h2 {color:#fff;margin:0;font-size:1.8rem;}
.si-level p {margin:4px 0 0;color:rgba(255,255,255,.88);}
.si-bar {height:14px;border-radius:999px;background:rgba(255,255,255,.22);overflow:hidden;margin-top:14px;}
.si-bar i {display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#FDE68A,#F9A8D4,#A7F3D0);background-size:200% 100%;}
.si-path {display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;}
.si-path span {padding:5px 11px;border-radius:999px;font-size:.76rem;font-weight:700;background:rgba(255,255,255,.14);}
.si-path span.si-here {background:#fff;color:#4C1D95;}
.si-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px;}
.si-medal {padding:18px;border-radius:20px;text-align:center;background:var(--si-surface);border:1px solid var(--si-line);box-shadow:var(--si-shadow);
  transition:transform .25s ease;}
.si-medal:hover {transform:translateY(-4px) rotate(-1deg);}
.si-medal span {display:grid;place-items:center;margin:0 auto 10px;width:62px;height:62px;border-radius:50%;font-size:1.8rem;
  background:var(--si-grad-soft);}
.si-medal.si-got span {background:conic-gradient(from 0deg,#FDE68A,#F9A8D4,#A7F3D0,#93C5FD,#FDE68A);box-shadow:0 0 0 4px var(--si-solid),0 10px 24px -8px #F59E0B;}
.si-medal b {display:block;color:var(--si-ink);}
.si-medal small {color:var(--si-muted);line-height:1.4;display:block;margin-top:4px;}
.si-medal em {display:inline-block;margin-top:10px;font-style:normal;font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;}
.si-medal.si-locked {opacity:.62;filter:grayscale(.6);}
.si-points {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.si-points div {padding:16px;border-radius:18px;background:var(--si-surface);border:1px solid var(--si-line);}
.si-points b {display:block;font-size:1.5rem;color:var(--si-ink);font-weight:800;}
.si-points small {color:var(--si-muted);}

/* Wishlist */
.si-wish {display:flex;gap:16px;align-items:center;padding:16px 18px;border-radius:20px;background:var(--si-surface);border:1px solid var(--si-line);
  box-shadow:var(--si-shadow);margin-bottom:8px;}
.si-wish .si-wi {font-size:1.7rem;width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:var(--si-grad-soft);flex:none;}
.si-wish b {color:var(--si-ink);font-size:1.02rem;}
.si-wish p {margin:2px 0 0;color:var(--si-muted);font-size:.84rem;}
.si-wish .si-days {margin-left:auto;text-align:right;}
.si-wish .si-days strong {display:block;font-size:1.4rem;color:var(--si-ink);}
.si-wish .si-days small {color:var(--si-muted);}
.si-ready {font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;background:#DCFCE7;color:#166534;}
.si-cool {font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;background:#E0F2FE;color:#075985;}

/* Sign-in brand panel */
.si-eyebrow {font-size:.74rem;letter-spacing:.16em;font-weight:700;color:var(--si-muted);margin-bottom:12px;}
.si-brand {border-radius:30px;padding:42px;color:#fff;min-height:540px;position:relative;overflow:hidden;margin:0 10px 22px 0;
  background:linear-gradient(135deg,#065F46,#0D9488 35%,#2563EB 70%,#7C3AED);background-size:220% 220%;box-shadow:0 40px 80px -40px #1E3A8A;}
.si-brand::before,.si-brand::after {content:"";position:absolute;border-radius:50%;filter:blur(10px);}
.si-brand::before {width:340px;height:340px;right:-110px;top:-90px;background:radial-gradient(circle,#F9A8D4aa,transparent 65%);}
.si-brand::after {width:300px;height:300px;left:-80px;bottom:-120px;background:radial-gradient(circle,#FDE68Aaa,transparent 65%);}
.si-brand > * {position:relative;z-index:1;}
.si-brand h2 {color:#fff;font-family:'Fraunces',Georgia,serif;font-size:clamp(2.2rem,3.6vw,3.4rem);line-height:1.06;margin:28px 0 18px;max-width:420px;letter-spacing:-.03em;}
.si-brand p {color:rgba(255,255,255,.88);font-size:1.02rem;line-height:1.7;}
.si-brand .si-wordmark {display:flex;align-items:center;gap:10px;color:#fff;font-size:1.2rem;font-weight:800;letter-spacing:-.02em;}
.si-brand .si-wordmark i {font-style:normal;width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:rgba(255,255,255,.2);}
.si-feats {display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:26px;}
.si-feats span {padding:11px 13px;border-radius:14px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);font-size:.85rem;font-weight:600;backdrop-filter:blur(6px);}
.si-brand .si-globe {position:absolute;right:30px;top:30px;font-size:3.4rem;opacity:.95;z-index:1;}
.si-auth-note {font-size:.82rem;color:var(--si-muted);padding-top:12px;}

/* Scenery */
.si-scenery {position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:0;}
.si-blob {position:absolute;border-radius:50%;filter:blur(70px);opacity:.42;}
.si-blob-1 {width:520px;height:520px;left:-140px;top:-120px;background:#6EE7B7;}
.si-blob-2 {width:460px;height:460px;right:-120px;top:18%;background:#93C5FD;}
.si-blob-3 {width:420px;height:420px;left:35%;bottom:-200px;background:#F0ABFC;}
.si-leaf {position:absolute;top:-40px;font-style:normal;font-size:20px;opacity:0;}
.si-leaf-1 {left:8%;--d:0s;--t:19s;} .si-leaf-2 {left:24%;--d:6s;--t:23s;} .si-leaf-3 {left:46%;--d:11s;--t:21s;}
.si-leaf-4 {left:63%;--d:3s;--t:25s;} .si-leaf-5 {left:80%;--d:9s;--t:20s;} .si-leaf-6 {left:93%;--d:15s;--t:24s;}
.si-night {background-image:radial-gradient(1.5px 1.5px at 18% 15%,#E0EAFF 98%,transparent),radial-gradient(1px 1px at 62% 28%,#CCDFFF 98%,transparent),
  radial-gradient(1.2px 1.2px at 85% 60%,#CCDFFF 98%,transparent),radial-gradient(1px 1px at 40% 80%,#FDE68A 98%,transparent);background-size:270px 230px;}
.si-star {position:absolute;width:110px;height:2px;background:linear-gradient(90deg,transparent,#DAE8FF);opacity:0;transform:rotate(35deg);border-radius:50%;}
.si-star-1 {left:12%;top:8%;--delay:0s;} .si-star-2 {left:48%;top:16%;--delay:4s;} .si-star-3 {left:70%;top:4%;--delay:8s;}
.si-star-4 {left:25%;top:35%;--delay:12s;} .si-star-5 {left:55%;top:48%;--delay:16s;}
.si-moon {position:absolute;right:8%;top:9%;width:84px;height:84px;border-radius:50%;box-shadow:-18px 10px 0 0 #FDE68A;transform:rotate(-20deg);opacity:.85;}
.si-sun {position:absolute;right:9%;top:10%;width:110px;height:110px;border-radius:50%;background:radial-gradient(circle,#FFF7CC,#FCD34D);
  box-shadow:0 0 80px 34px #FDE68A66;opacity:.8;}
.si-cloud {position:absolute;width:190px;height:45px;border-radius:80px;background:#FFFFFF;opacity:.6;}
.si-cloud::before,.si-cloud::after {content:"";position:absolute;background:inherit;border-radius:50%;}
.si-cloud::before {width:80px;height:80px;left:30px;bottom:0;} .si-cloud::after {width:100px;height:100px;right:25px;bottom:0;}
.si-cloud-1 {left:8%;top:18%;} .si-cloud-2 {left:55%;top:64%;} .si-cloud-3 {left:30%;top:40%;transform:scale(.6);opacity:.4;}

/* Motion */
@media (prefers-reduced-motion:no-preference) {
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"],
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {animation:si-rise .7s cubic-bezier(.2,.8,.2,1) backwards;}
  .stApp [data-testid="stVerticalBlock"] > :nth-child(2) {animation-delay:.05s;} .stApp [data-testid="stVerticalBlock"] > :nth-child(3) {animation-delay:.1s;}
  .stApp [data-testid="stVerticalBlock"] > :nth-child(4) {animation-delay:.15s;} .stApp [data-testid="stVerticalBlock"] > :nth-child(5) {animation-delay:.2s;}
  .stApp [data-testid="stVerticalBlock"] > :nth-child(6) {animation-delay:.25s;} .stApp [data-testid="stVerticalBlock"] > :nth-child(n+7) {animation-delay:.3s;}
  .stApp [data-testid="stMetric"] {transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s ease;}
  .stApp [data-testid="stMetric"]:hover {transform:translateY(-5px);box-shadow:0 22px 40px -22px #0F766E;}
  .stApp [data-testid="stMetric"]::before {animation:si-flow 6s linear infinite;}
  .stApp [data-testid="stMetricValue"] {animation:si-pop .8s cubic-bezier(.2,1.4,.4,1) backwards .25s;}
  .si-logo {animation:si-flow 8s ease infinite,si-bob 5s ease-in-out infinite;}
  .si-hero,.si-brand,.si-level {animation:si-flow 16s ease infinite;}
  .si-shine {animation:si-flow 6s linear infinite;}
  .si-chip .si-dot {animation:si-ping 2s infinite;}
  .si-orb .si-arc,.si-ring-svg .si-arc {animation:si-draw 1.6s cubic-bezier(.2,.8,.2,1) backwards .2s;}
  .si-orb .si-orb-in span,.si-brand .si-globe {animation:si-bob 4s ease-in-out infinite;}
  .si-count {animation:si-count 1.8s cubic-bezier(.2,.8,.2,1);}
  .si-mini div,.si-equiv div,.si-alt,.si-medal,.si-wish,.si-points div,.si-feats span {animation:si-rise .7s cubic-bezier(.2,.8,.2,1) backwards;}
  .si-mini div:nth-child(2),.si-equiv div:nth-child(2),.si-alt:nth-child(2),.si-medal:nth-child(2),.si-points div:nth-child(2),.si-feats span:nth-child(2) {animation-delay:.12s;}
  .si-mini div:nth-child(3),.si-equiv div:nth-child(3),.si-alt:nth-child(3),.si-medal:nth-child(3),.si-points div:nth-child(3),.si-feats span:nth-child(3) {animation-delay:.24s;}
  .si-medal:nth-child(4),.si-points div:nth-child(4),.si-feats span:nth-child(4) {animation-delay:.36s;}
  .si-medal:nth-child(n+5) {animation-delay:.48s;}
  .si-medal.si-got span {animation:si-spin 10s linear infinite;}
  .si-bar i {animation:si-grow 1.6s cubic-bezier(.2,.8,.2,1) backwards .3s,si-flow 4s linear infinite;transform-origin:left;}
  .st-key-badges [data-testid="stAlert"] {animation:si-pop .7s cubic-bezier(.2,1.5,.4,1) backwards;}
  .si-equiv i {animation:si-bob 5s ease-in-out infinite;}
  .si-tip {animation:si-rise .6s ease backwards;}
  .stApp [data-testid="stBaseButton-primary"]::after,.stApp [data-testid="stBaseButton-primaryFormSubmit"]::after {animation:si-sheen 3.8s ease-in-out infinite;}
  .si-blob {animation:si-blob 22s ease-in-out infinite alternate;}
  .si-blob-2 {animation-duration:28s;animation-delay:-8s;} .si-blob-3 {animation-duration:25s;animation-delay:-14s;}
  .si-leaf {animation:si-leaf var(--t) linear infinite;animation-delay:var(--d);}
  .si-star {animation:si-fall 22s linear infinite;animation-delay:var(--delay);}
  .si-cloud {animation:si-drift 55s ease-in-out infinite alternate;} .si-cloud-2 {animation-delay:-25s;}
  .si-sun {animation:si-glow 12s ease-in-out infinite alternate;}
  .si-moon {animation:si-glow 10s ease-in-out infinite alternate;}
}
@keyframes si-rise {from {opacity:0;transform:translateY(18px);}}
@keyframes si-pop {from {opacity:0;transform:scale(.85);}}
@keyframes si-flow {0% {background-position:0% 50%;} 50% {background-position:100% 50%;} 100% {background-position:0% 50%;}}
@keyframes si-bob {0%,100% {transform:translateY(0);} 50% {transform:translateY(-7px);}}
@keyframes si-ping {0% {box-shadow:0 0 0 0 rgba(167,243,208,.9);} 80%,100% {box-shadow:0 0 0 10px rgba(167,243,208,0);}}
@keyframes si-draw {from {stroke-dashoffset:var(--c);}}
@keyframes si-count {from {--si-n:0;}}
@keyframes si-grow {from {transform:scaleX(0);}}
@keyframes si-spin {to {filter:hue-rotate(360deg);}}
@keyframes si-sheen {0%,60% {left:-60%;} 100% {left:130%;}}
@keyframes si-blob {0% {transform:translate(0,0) scale(1);} 50% {transform:translate(80px,40px) scale(1.12);} 100% {transform:translate(-40px,90px) scale(.95);}}
@keyframes si-leaf {0% {opacity:0;transform:translate(0,0) rotate(0);} 8% {opacity:.55;} 92% {opacity:.45;} 100% {opacity:0;transform:translate(90px,110vh) rotate(540deg);}}
@keyframes si-fall {0%,6% {opacity:0;transform:translate(0,0) rotate(35deg);} 8% {opacity:.7;} 16% {opacity:0;transform:translate(340px,238px) rotate(35deg);} 100% {opacity:0;}}
@keyframes si-drift {to {transform:translateX(120px);}}
@keyframes si-glow {to {transform:scale(1.07);opacity:1;}}
.si-paused *,.si-paused *::before,.si-paused *::after {animation:none!important;}
@media (prefers-reduced-motion:reduce) {.si-scenery * {animation:none!important;} .si-leaf {display:none;}}

/* Responsive */
@media (max-width:1100px) {
  .stApp [data-testid="stMainBlockContainer"] {padding-left:1.4rem;padding-right:1.4rem;}
  .si-hero {grid-template-columns:1fr;} .si-alts,.si-equiv {grid-template-columns:1fr 1fr;} .si-points {grid-template-columns:1fr 1fr;}
}
@media (max-width:760px) {
  .stApp [data-testid="stMainBlockContainer"] {padding-top:4.5rem;padding-left:1rem;padding-right:1rem;}
  .stApp [data-testid="stHorizontalBlock"] {row-gap:1rem;}
  .si-hero {padding:24px;border-radius:24px;} .si-brand {min-height:0;padding:26px;margin-right:0;}
  .si-brand h2 {font-size:2rem;margin:16px 0 12px;} .si-feats,.si-brand .si-globe {display:none;}
  .si-alts,.si-equiv,.si-rings {grid-template-columns:1fr;} .si-level {grid-template-columns:1fr;text-align:center;}
  .si-level .si-big {margin:0 auto;}
  .stApp [data-testid="stMetric"] {min-height:104px;padding:16px 18px;}
}
</style>""")

NIGHT_CSS = """<style>
.stApp {--si-bg:#070D1F;--si-surface:rgba(20,32,58,.78);--si-solid:#121D36;--si-muted:#B6C4DD;--si-ink:#EEF3FB;--si-line:rgba(148,163,209,.22);
  --si-grad-soft:linear-gradient(135deg,#0F2A3A,#1C2550 60%,#2A1B4D);
  background:radial-gradient(1200px 600px at 80% -10%,#1E1B4B 0%,transparent 60%),radial-gradient(900px 500px at -10% 30%,#052E2B 0%,transparent 60%),#070D1F;
  color:var(--si-ink);color-scheme:dark;}
.stApp [data-testid="stSidebar"] {background:rgba(10,18,38,.92);}
.stApp h1,.stApp h2,.stApp h3,.stApp label,.stApp p,.stApp li,.stApp [data-testid="stMetricValue"],.stApp [data-testid="stMarkdownContainer"] {color:var(--si-ink);}
.stApp [data-baseweb="input"],.stApp [data-baseweb="input"] input,.stApp [data-baseweb="textarea"],.stApp textarea,.stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="base-input"],.stApp [data-testid="stNumberInput"] button,.stApp [data-testid="stDateInput"] input {background:#16233F;color:#EEF3FB;border-color:#3A4C70;}
.stApp input::placeholder,.stApp textarea::placeholder {color:#93A3C0;}
.stApp [data-testid="stBaseButton-secondary"],.stApp [data-testid="stBaseButton-secondaryFormSubmit"] {background:#16233F;color:#EEF3FB;border-color:#3A4C70;}
.stApp button p {color:#EEF3FB;}
.stApp [data-testid="stExpander"] details,.stApp [data-testid="stExpander"] summary {background:var(--si-solid);}
.stApp [data-testid="stExpander"] summary,.stApp [data-testid="stExpander"] summary p {color:var(--si-ink);}
.stApp [data-testid="stAlert"] {background:#16233F;color:#EEF3FB;}
.stApp a {color:#93C5FD;}
.si-tip {background:linear-gradient(135deg,#3B1D5A,#1E2A5A);border-color:#4C3A7A;} .si-tip p {color:#F5E8FF;} .si-tip small {color:#F9A8D4;}
.si-estimate .si-tag {background:#064E3B;color:#A7F3D0;} .si-estimate .si-tag.si-new {background:#4C0519;color:#FECDD3;}
.si-ok {background:#064E3B;color:#A7F3D0;} .si-over {background:#4C0519;color:#FECDD3;}
.st-key-badges [data-testid="stAlert"] {background:linear-gradient(120deg,#422006,#14532D,#164E63);border-color:#854D0E;}
.st-key-badges [data-testid="stAlert"] p {color:#FEF3C7;}
.si-ready {background:#14532D;color:#BBF7D0;} .si-cool {background:#0C4A6E;color:#BAE6FD;}
</style>"""

DAY_CSS = """<style>
.stApp {--si-bg:#EAF6FF;background:linear-gradient(160deg,#DBF0FF 0%,#F0F9FF 40%,#FEFCE8 100%);}
.stApp [data-testid="stSidebar"] {background:rgba(240,249,255,.85);}
.si-hero {background:linear-gradient(120deg,#0284C7,#0EA5E9 35%,#22C55E 75%,#EAB308);background-size:220% 220%;}
</style>"""

CONTRAST_CSS = """<style>
.stApp {--si-bg:#FFFFFF;--si-surface:#FFFFFF;--si-solid:#FFFFFF;--si-muted:#1F2937;--si-ink:#000000;--si-line:#4B5563;
  --si-grad:linear-gradient(#0B5D44,#0B5D44);--si-grad-soft:linear-gradient(#F3F4F6,#F3F4F6);--si-shadow:none;background:#FFFFFF;color:#000;}
.si-hero,.si-brand,.si-level,.si-equiv div {background:#0B3D2E!important;box-shadow:none!important;}
.si-hero::after,.si-hero::before,.si-brand::before,.si-brand::after {display:none;}
.si-shine {color:#FFFFFF;background:none;-webkit-background-clip:border-box;background-clip:border-box;}
.si-estimate b {color:#0B3D2E;background:none;-webkit-background-clip:border-box;background-clip:border-box;}
.si-tip {background:#FFFFFF;border:2px solid #000;} .si-tip p,.si-tip small {color:#000;}
.stApp *,.stApp *::before,.stApp *::after {animation:none!important;}
</style>"""


def apply_styles(high_contrast=False):
    theme = theme_name()
    light = {"bg": "#F3FBF7", "surface": "rgba(255,255,255,.82)", "solid": "#FFFFFF", "muted": "#4B6358",
             "ink": "#0F2E25", "line": "rgba(15,94,72,.13)", "sidebar": "rgba(240,250,245,.88)"}
    st.markdown(BASE_CSS.substitute(light), unsafe_allow_html=True)
    if high_contrast:
        st.markdown(CONTRAST_CSS, unsafe_allow_html=True)
    elif theme == "Night":
        st.markdown(NIGHT_CSS, unsafe_allow_html=True)
    elif theme == "Day":
        st.markdown(DAY_CSS, unsafe_allow_html=True)
    if high_contrast:
        st.markdown('<style>.si-scenery {display:none;}</style>', unsafe_allow_html=True)


def html(markup):
    st.markdown(markup, unsafe_allow_html=True)


def sidebar_brand(username, level):
    initial = escape((username or "?")[:1].upper())
    html(f"""<div class="si-side-brand"><div class="si-logo" aria-hidden="true">🌿</div>
    <div><b>ShopImpact</b><small>Small choices. Thoughtful habits.</small></div></div>
    <div class="si-user"><div class="si-avatar" aria-hidden="true">{initial}</div>
    <div><b>{escape(username)}</b><small>{level['icon']} Level {level['number']} · {escape(level['name'])}</small></div></div>""")


def _arc(progress, size, stroke, gradient_id, colors):
    radius = (size - stroke) / 2
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - max(0.0, min(progress, 1.0)))
    stops = "".join(f'<stop offset="{i / (len(colors) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(colors))
    return (f'<svg viewBox="0 0 {size} {size}" aria-hidden="true"><defs><linearGradient id="{gradient_id}" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient></defs>'
            f'<circle class="si-track" cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="{stroke}"/>'
            f'<circle class="si-arc" cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="url(#{gradient_id})" stroke-width="{stroke}" '
            f'stroke-linecap="round" style="--c:{circumference:.1f};stroke-dasharray:{circumference:.1f};stroke-dashoffset:{offset:.1f}"/></svg>')


def hero(username, level, streak, skips, month_label):
    orb = _arc(level["progress"], 150, 12, "si-orb-grad", ["#FDE68A", "#F9A8D4", "#A7F3D0"])
    nxt = f"{level['to_next']} pts to {escape(level['next_name'])}" if level["next_name"] else "Top level reached"
    html(f"""<section class="si-hero">
<div>
<span class="si-chip"><i class="si-dot"></i> {escape(month_label)}</span><span class="si-chip">🌿 2026 refresh</span><span class="si-chip">🔒 Private journal</span>
<p class="si-greet">Welcome back, {escape(username)} 👋</p>
<h1>A little more <span class="si-shine">mindful</span>, every month.</h1>
<p>Know where your money goes. Explore your estimated impact. Pause before you buy, and celebrate every thoughtful choice.</p>
</div>
<div class="si-hero-side">
<div class="si-orb">{orb}<div class="si-orb-in"><span aria-hidden="true">{level['icon']}</span><b>Level {level['number']} · {escape(level['name'])}</b><small>{nxt}</small></div></div>
<div class="si-mini">
<div><b class="si-count" style="--to:{level['points']}"></b><small>eco points</small></div>
<div><b class="si-count" style="--to:{streak}"></b><small>🔥 month streak</small></div>
<div><b class="si-count" style="--to:{skips}"></b><small>⏸️ mindful skips</small></div>
</div></div>
</section>""")


def section(icon, title, subtitle=""):
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    html(f'<div class="si-section"><div class="si-ico" aria-hidden="true">{icon}</div><div><h3>{escape(title)}</h3>{sub}</div></div>')


def estimate_pill(kg, factor, category, lower, equivalent):
    tag = '<span class="si-tag">♻️ Reuse / repair choice</span>' if lower else '<span class="si-tag si-new">🛍️ New purchase</span>'
    html(f"""<div class="si-estimate" role="status"><span>Live preview</span><b>{kg:,.2f} kg CO₂e</b>{tag}
<span>{CATEGORY_ICONS.get(category, '🛒')} reference factor {factor:.6f} per INR · ≈ {equivalent['value']:,} {escape(equivalent['label'])}</span></div>""")


def goal_rings(items):
    cards = []
    for index, (icon, label, used, goal, unit) in enumerate(items):
        share = used / goal if goal else 0
        over = share > 1
        colors = ["#F59E0B", "#F43F5E", "#EC4899"] if over else (["#10B981", "#14B8A6", "#3B82F6"] if index == 0 else ["#06B6D4", "#6366F1", "#8B5CF6"])
        ring = _arc(share, 96, 10, f"si-ring-{index}", colors)
        status = '<em class="si-over">Above goal</em>' if over else '<em class="si-ok">Within goal</em>'
        cards.append(f"""<div class="si-ring"><div class="si-ring-svg">{ring}<b>{share:.0%}</b></div>
<div class="si-ring-txt"><strong>{icon} {escape(label)}</strong><span>{unit} {used:,.2f} of {unit} {goal:,.2f}</span><br>{status}</div></div>""")
    html(f'<div class="si-rings">{"".join(cards)}</div>')


def equivalents_cards(rows):
    cards = "".join(f'<div><i aria-hidden="true">{r["icon"]}</i><b>{r["value"]:,}</b><span>{escape(r["label"])}</span></div>' for r in rows)
    html(f'<div class="si-equiv">{cards}</div>')


def alternatives_cards(ideas):
    cards = "".join(f'<div class="si-alt"><div class="si-num" aria-hidden="true">{i}</div><p>{escape(text)}</p></div>' for i, text in enumerate(ideas, 1))
    html(f'<div class="si-alts">{cards}</div>')


def tip_card(tip):
    html(f'<div class="si-tip"><small>✨ A SMALL IDEA</small><p>{escape(tip)}</p></div>')


def story_card(text):
    html(f'<div class="si-story"><span aria-hidden="true">📖</span><p><b>Your month in a sentence:</b> {escape(text)}</p></div>')


def empty_state(icon, text):
    html(f'<div class="si-empty"><span aria-hidden="true">{icon}</span>{escape(text)}</div>')


def level_card(level, levels):
    width = max(level["progress"], 0.02) * 100
    nxt = f"{level['to_next']} points to {escape(level['next_icon'])} {escape(level['next_name'])}" if level["next_name"] else "You've reached the top level — keep growing your forest!"
    path = "".join(f'<span class="{"si-here" if n == level["name"] else ""}">{i} {escape(n)}</span>' for _, n, i in levels)
    html(f"""<div class="si-level"><div class="si-big" aria-hidden="true">{level['icon']}</div>
<div><p>LEVEL {level['number']} · {level['points']} ECO POINTS</p><h2>{escape(level['name'])}</h2><p>{nxt}</p>
<div class="si-bar" role="img" aria-label="{level['progress']:.0%} of the way to the next level"><i style="width:{width:.1f}%"></i></div>
<div class="si-path">{path}</div></div></div>""")


def points_grid(breakdown):
    cells = "".join(f'<div><b class="si-count" style="--to:{value}"></b><small>{escape(label)}</small></div>' for label, value in breakdown.items())
    html(f'<div class="si-points">{cells}</div>')


def medal_grid(items):
    cards = []
    for item in items:
        state = "si-got" if item["earned"] else "si-locked"
        tag = '<em class="si-ok">Unlocked</em>' if item["earned"] else '<em class="si-over" style="opacity:.8">Locked</em>'
        cards.append(f'<div class="si-medal {state}"><span aria-hidden="true">{item["icon"]}</span><b>{escape(item["name"])}</b>'
                     f'<small>{escape(item.get("rule", ""))}</small>{tag}</div>')
    html(f'<div class="si-grid">{"".join(cards)}</div>')


def wish_card(wish, days, cool_off):
    icon = CATEGORY_ICONS.get(wish["product_type"], "🛒")
    if wish["status"] == "waiting":
        badge = '<span class="si-ready">Cool-off complete — decide calmly</span>' if days >= cool_off else f'<span class="si-cool">Cooling off · {cool_off - days} days to go</span>'
    elif wish["status"] == "skipped":
        badge = '<span class="si-ready">⏸️ Skipped</span>'
    else:
        badge = '<span class="si-cool">🛍️ Bought</span>'
    html(f"""<div class="si-wish"><div class="si-wi" aria-hidden="true">{icon}</div>
<div><b>{escape(wish['name'])}</b><p>{escape(wish['product_type'])} · INR {float(wish['price']):,.2f} · {float(wish['estimated_co2']):,.2f} kg CO₂e estimated</p>{badge}</div>
<div class="si-days"><strong>{days}</strong><small>{'day' if days == 1 else 'days'} waited</small></div></div>""")


def brand_panel():
    html("""<section class="si-brand">
<div class="si-wordmark"><i aria-hidden="true">🌿</i> ShopImpact</div>
<h2>Small choices.<br><span class="si-shine">A clearer picture.</span></h2>
<p>Your colourful shopping journal for thoughtful spending, everyday habits and a little perspective.</p>
<div class="si-feats"><span>📊 Monthly dashboard</span><span>☁️ CO₂e estimates</span><span>⏸️ Mindful wishlist</span><span>🏆 Eco levels & badges</span></div>
<div class="si-globe" aria-hidden="true">🌍</div>
</section>""")
