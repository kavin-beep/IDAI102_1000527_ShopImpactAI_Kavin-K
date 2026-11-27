"""Shared presentation: the ShopImpact "Conscious Market Journal" design system.

A cinematic, editorial layer: slow crossfading market and forest footage behind
warm glass panels, serif headlines, mono kickers and gentle motion. Native
Streamlit controls keep their semantics; decorative HTML is aria-hidden or carries
plain text so meaning never depends on colour or motion. Nothing here changes how
purchases, estimates, goals or accounts work.
"""
import json
from html import escape
import streamlit as st
import streamlit.components.v1 as components

# Earthy category palette shared by every chart (text labels always accompany colour).
CATEGORY_COLORS = {
    "New clothing": "#E07A5F",
    "Second-hand clothing": "#A3C585",
    "Leather footwear": "#D4A373",
    "New electronics": "#9D8DF1",
    "Refurbished electronics": "#6CC4C9",
    "Single-use household goods": "#F2C14E",
    "Reusable household goods": "#81B29A",
    "Repair services": "#8AB4F8",
}
CATEGORY_ICONS = {
    "New clothing": "👕", "Second-hand clothing": "🧥", "Leather footwear": "👞",
    "New electronics": "💻", "Refurbished electronics": "🔋", "Single-use household goods": "🧴",
    "Reusable household goods": "🫙", "Repair services": "🧵",
}

# Mixkit (free licence) footage that fits the theme: second-hand market, clothes racks, produce, forest light.
CLIPS = [4147, 33167, 23327, 991, 50847, 27163]
BRAND_VIDEO = "https://assets.mixkit.co/videos/33167/33167-720.mp4"
HERO_VIDEO = "https://assets.mixkit.co/videos/4147/4147-720.mp4"


def theme_name():
    """Return the selected visual theme, defaulting to the standard appearance."""
    return st.session_state.get("visual_theme", "Normal")


def motion_on():
    """Return whether animated scenery is enabled for this browser session."""
    return st.session_state.get("scenery_motion", True)


def chart_ink(high_contrast=False):
    """Chart text colour for the dark cinematic surfaces (white in high contrast)."""
    return "#FFFFFF" if high_contrast else "#F4EDE1"


def theme_controls():
    """Theme and animation choices remain in this browser session."""
    with st.sidebar:
        with st.expander("🎨 Theme & animation", expanded=False):
            theme = st.selectbox("Theme", ["Normal", "Day", "Night"], key="visual_theme",
                                 help="Normal: market footage · Day: golden sun and clouds · Night: stars and falling stars")
            motion = st.checkbox("Animated scenery", value=True, key="scenery_motion",
                                 help="Turns off background video and interface animations. Your device's reduced-motion setting is respected too.")
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
        content = '<i class="si-blob si-blob-1"></i><i class="si-blob si-blob-2"></i>'
        scene = "aurora"
    leaves = "".join(f'<i class="si-leaf si-leaf-{n}">{"🍃" if n % 2 else "🌿"}</i>' for n in range(1, 7)) if scene != "night" else ""
    st.markdown(f'<div class="si-scenery si-{scene}{paused}" aria-hidden="true">{content}{leaves}</div>', unsafe_allow_html=True)
    if not motion:
        st.markdown("<style>.stApp *,.stApp *::before,.stApp *::after{animation:none!important;transition:none!important;}</style>",
                    unsafe_allow_html=True)
    _inject_fx()


BASE_CSS = r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
@property --si-n {syntax:'<integer>';initial-value:0;inherits:false;}
html,body {background:#0E0C09;}
.stApp {
  --si-ink:#F4EDE1; --si-muted:#BDB3A3; --si-dim:#8C8273; --si-line:rgba(244,237,225,.12); --si-line-2:rgba(244,237,225,.22);
  --si-surface:rgba(20,18,14,.62); --si-solid:#17140F; --si-raise:rgba(32,28,22,.72);
  --si-moss:#A3C585; --si-amber:#E8B04A; --si-clay:#E07A5F;
  --si-grad:linear-gradient(110deg,#A3C585,#E8B04A 55%,#E07A5F);
  --si-grad-soft:linear-gradient(135deg,rgba(163,197,133,.16),rgba(232,176,74,.10));
  --si-shadow:0 30px 60px -36px rgba(0,0,0,.85);
  --si-radius:22px; --si-ease:cubic-bezier(.16,1,.3,1);
  --si-serif:'Fraunces',Georgia,serif; --si-sans:'Inter',ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;
  --si-mono:'JetBrains Mono',ui-monospace,monospace;
  background:transparent!important; color:var(--si-ink); font-family:var(--si-sans); counter-reset:sisec;
}
.stApp [data-testid="stAppViewContainer"],.stApp [data-testid="stMain"],.stApp [data-testid="stBottom"] > div {background:transparent!important;}
.stApp p,.stApp li,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp [data-baseweb="tab"] p {font-family:var(--si-sans);}
.stApp h1,.stApp h2,.stApp h3 {font-family:var(--si-serif);font-weight:600;letter-spacing:-.02em;color:var(--si-ink);}
.stApp h1 {font-size:clamp(2.2rem,4vw,3.6rem);line-height:1.02;}
.stApp [data-testid="stHeader"] {background:transparent;}
.stApp [data-testid="stMainBlockContainer"] {max-width:1380px;padding-top:2.2rem;padding-bottom:5rem;position:relative;z-index:2;}
.stApp [data-testid="stCaptionContainer"] {opacity:1;}
.stApp [data-testid="stCaptionContainer"] p {color:var(--si-muted);line-height:1.6;}
.stApp a {color:var(--si-amber);}
::selection {background:#E8B04A;color:#17140F;}

/* Sidebar: a dark glass ledger */
.stApp [data-testid="stSidebar"] {background:rgba(14,12,9,.78);border-right:1px solid var(--si-line);backdrop-filter:blur(22px) saturate(1.2);}
.stApp [data-testid="stSidebar"] [data-testid="stExpander"] {background:rgba(255,255,255,.03);}
.si-side-brand {display:flex;align-items:center;gap:12px;margin:4px 0 6px;}
.si-logo {width:46px;height:46px;border-radius:14px;display:grid;place-items:center;font-size:1.35rem;
  background:radial-gradient(circle at 30% 25%,#3B4A2C,#17140F 70%);border:1px solid var(--si-line-2);box-shadow:0 0 0 1px rgba(232,176,74,.12),0 12px 26px -12px #A3C58566;}
.si-side-brand b {font-family:var(--si-serif);font-size:1.45rem;font-weight:600;color:var(--si-ink);display:block;line-height:1.05;}
.si-side-brand small {color:var(--si-dim);font-family:var(--si-mono);font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;}
.si-user {display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:16px;background:rgba(255,255,255,.04);
  border:1px solid var(--si-line);margin:14px 0 10px;}
.si-avatar {width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-family:var(--si-serif);font-weight:700;font-size:1.1rem;color:#17140F;
  background:var(--si-grad);flex:none;}
.si-user b {color:var(--si-ink);display:block;font-size:.95rem;}
.si-user small {color:var(--si-muted);font-size:.78rem;}

/* Glass surfaces */
.stApp [data-testid="stMetric"] {background:var(--si-surface);border:1px solid var(--si-line);border-radius:var(--si-radius);
  padding:22px 24px;min-height:132px;box-shadow:var(--si-shadow);position:relative;overflow:hidden;backdrop-filter:blur(18px) saturate(1.2);}
.stApp [data-testid="stMetric"]::before {content:"";position:absolute;left:24px;right:24px;top:0;height:1px;background:var(--si-grad);opacity:.9;}
.stApp [data-testid="stMetricLabel"] p {color:var(--si-dim);font-family:var(--si-mono);font-size:.7rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;}
.stApp [data-testid="stMetricValue"],.stApp [data-testid="stMetricValue"] div,.stApp [data-testid="stMetricValue"] p {font-family:var(--si-serif);font-size:clamp(1.7rem,2.6vw,2.5rem);font-weight:600;letter-spacing:-.02em;color:var(--si-ink);}
.st-key-kpis [data-testid="stMetric"]::after {position:absolute;right:18px;top:16px;font-size:1.3rem;width:44px;height:44px;
  border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.05);border:1px solid var(--si-line);}
.st-key-kpis [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"]::after {content:"💸";}
.st-key-kpis [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"]::after {content:"☁️";}
.st-key-kpis [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"]::after {content:"♻️";}
.stApp [data-testid="stForm"] {padding:26px;background:var(--si-surface);border:1px solid var(--si-line);border-radius:var(--si-radius);
  box-shadow:var(--si-shadow);backdrop-filter:blur(18px);}
.stApp [data-testid="stExpander"] {border:1px solid var(--si-line);border-radius:16px;background:var(--si-surface);overflow:hidden;backdrop-filter:blur(14px);}
.stApp [data-testid="stExpander"] summary:hover {background:rgba(232,176,74,.06);}
.stApp [class*="st-key-card"] {background:var(--si-surface);border:1px solid var(--si-line);border-radius:26px;padding:26px 28px;
  box-shadow:var(--si-shadow);backdrop-filter:blur(18px) saturate(1.2);}
.stApp .st-key-card_add {background:linear-gradient(rgba(23,20,15,.78),rgba(23,20,15,.78)) padding-box,var(--si-grad) border-box;border:1px solid transparent;}
.stApp [data-testid="stAlert"] {border-radius:14px;backdrop-filter:blur(12px);}
.stApp [data-testid="stDataFrame"] {border-radius:16px;overflow:hidden;border:1px solid var(--si-line);}
.stApp [data-testid="stVegaLiteChart"],.stApp [data-testid="stArrowVegaLiteChart"] {background:transparent;}
.stApp [data-baseweb="input"],.stApp [data-baseweb="select"] > div,.stApp [data-baseweb="textarea"],.stApp [data-baseweb="base-input"] {
  border-radius:12px;background:rgba(10,9,7,.55);border-color:var(--si-line-2);}
.stApp [data-baseweb="input"]:focus-within,.stApp [data-baseweb="select"] > div:focus-within {border-color:var(--si-amber);box-shadow:0 0 0 3px rgba(232,176,74,.18);}

/* Buttons */
.stApp button {border-radius:999px;font-weight:600;transition:transform .3s var(--si-ease),box-shadow .3s ease,background-color .2s ease,border-color .2s ease,color .2s ease;}
.stApp [data-testid="stBaseButton-secondary"],.stApp [data-testid="stBaseButton-secondaryFormSubmit"] {background:rgba(255,255,255,.04);border:1px solid var(--si-line-2);color:var(--si-ink);}
.stApp [data-testid="stBaseButton-secondary"]:hover,.stApp [data-testid="stBaseButton-secondaryFormSubmit"]:hover {
  border-color:var(--si-amber);color:var(--si-amber);transform:translateY(-2px);}
.stApp [data-testid="stBaseButton-primary"],.stApp [data-testid="stBaseButton-primaryFormSubmit"],.stApp button[kind="primary"] {
  background:var(--si-ink);border:0;color:#17140F;box-shadow:0 14px 30px -16px rgba(232,176,74,.7);position:relative;overflow:hidden;}
.stApp [data-testid="stBaseButton-primary"] p,.stApp [data-testid="stBaseButton-primaryFormSubmit"] p,.stApp button[kind="primary"] p {color:#17140F;font-weight:700;position:relative;z-index:1;}
.stApp [data-testid="stBaseButton-primary"]::before,.stApp [data-testid="stBaseButton-primaryFormSubmit"]::before {
  content:"";position:absolute;inset:0;background:var(--si-amber);transform:translateY(101%);transition:transform .45s var(--si-ease);}
.stApp [data-testid="stBaseButton-primary"]:hover::before,.stApp [data-testid="stBaseButton-primaryFormSubmit"]:hover::before {transform:translateY(0);}
.stApp [data-testid="stBaseButton-primary"]:hover,.stApp [data-testid="stBaseButton-primaryFormSubmit"]:hover {transform:translateY(-2px);color:#17140F;}
.stApp button:active {transform:scale(.97);}
.stApp button:focus-visible,.stApp input:focus-visible,.stApp textarea:focus-visible,.stApp a:focus-visible {outline:3px solid var(--si-amber);outline-offset:3px;}

/* Tabs: an editorial index (BaseWeb tabs on 1.55, react-aria tabs on newer Streamlit) */
.stApp [data-baseweb="tab-list"],.stApp [role="tablist"] {gap:4px;padding:6px;background:rgba(14,12,9,.6);border-radius:999px;border:1px solid var(--si-line);
  backdrop-filter:blur(18px);overflow-x:auto;width:fit-content;max-width:100%;}
.stApp [data-baseweb="tab"],.stApp [role="tab"] {padding:9px 18px;border-radius:999px;height:auto;transition:background-color .3s ease,color .3s ease;}
.stApp [data-baseweb="tab"]:hover,.stApp [role="tab"]:hover {background:rgba(255,255,255,.06);}
.stApp [data-baseweb="tab"] p,.stApp [role="tab"] p {font-weight:600;font-size:.9rem;color:var(--si-muted);}
.stApp [data-baseweb="tab"][aria-selected="true"],.stApp [role="tab"][aria-selected="true"] {background:var(--si-ink);}
.stApp [data-baseweb="tab"][aria-selected="true"] p,.stApp [role="tab"][aria-selected="true"] p {color:#17140F;}
.stApp [data-baseweb="tab-highlight"],.stApp [data-baseweb="tab-border"],.stApp [role="tablist"] + [aria-hidden="true"] {display:none;}
.stApp [data-testid="stTabs"] [role="tabpanel"] {padding-top:24px;}

/* Hero: cinematic cover with footage */
.si-hero {position:relative;overflow:hidden;border-radius:32px;min-height:520px;margin-bottom:30px;color:#F4EDE1;isolation:isolate;
  border:1px solid var(--si-line);box-shadow:0 50px 90px -50px #000;display:flex;flex-direction:column;justify-content:space-between;}
.si-hero video,.si-hero .si-poster {position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;
  filter:sepia(.25) saturate(.95) brightness(.62) contrast(1.06);transform:scale(1.04);}
.si-hero .si-poster {background:radial-gradient(80% 90% at 80% 10%,#3B4A2C,#17140F 70%);}
.si-hero::before {content:"";position:absolute;inset:0;z-index:-1;
  background:linear-gradient(90deg,rgba(14,12,9,.88) 0%,rgba(14,12,9,.55) 48%,rgba(14,12,9,.2)),linear-gradient(0deg,rgba(14,12,9,.9),transparent 45%);}
.si-meta {display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:22px 34px;font-family:var(--si-mono);font-size:.68rem;
  letter-spacing:.16em;text-transform:uppercase;color:rgba(244,237,225,.72);border-bottom:1px solid rgba(244,237,225,.12);}
.si-hero-body {display:grid;grid-template-columns:1.55fr 1fr;gap:34px;align-items:end;padding:30px 34px 24px;}
.si-hero .si-greet {font-family:var(--si-mono);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--si-amber);margin:0 0 14px;}
.si-hero h1 {margin:0 0 18px;color:#F4EDE1;font-family:var(--si-serif);font-weight:400;font-size:clamp(2.6rem,5.4vw,5rem);line-height:.98;letter-spacing:-.035em;}
.si-hero h1 em,.si-brand h2 em {font-style:italic;color:var(--si-amber);}
.si-mask {display:block;overflow:hidden;padding-bottom:.06em;} .si-mask > span {display:block;}
.si-hero .si-lede {margin:0;color:rgba(244,237,225,.82);line-height:1.7;max-width:560px;font-size:1.02rem;}
.si-shine {font-style:italic;color:var(--si-amber);}
.si-chip {display:inline-flex;align-items:center;gap:7px;color:rgba(244,237,225,.86);}
.si-chip .si-dot {width:7px;height:7px;border-radius:50%;background:var(--si-moss);box-shadow:0 0 0 0 #A3C585;}
.si-hero-side {display:flex;flex-direction:column;align-items:stretch;gap:14px;padding:20px;border-radius:24px;
  background:rgba(14,12,9,.5);border:1px solid rgba(244,237,225,.14);backdrop-filter:blur(18px);}
.si-orb {position:relative;width:150px;height:150px;margin:0 auto;}
.si-orb svg {width:100%;height:100%;transform:rotate(-90deg);}
.si-orb .si-orb-in {position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;}
.si-orb .si-orb-in span {font-size:2.2rem;line-height:1;}
.si-orb .si-orb-in b {font-family:var(--si-serif);font-size:.95rem;font-weight:600;margin-top:6px;}
.si-orb .si-orb-in small {font-size:.68rem;color:rgba(244,237,225,.7);max-width:110px;}
.si-mini {display:grid;grid-template-columns:repeat(3,1fr);gap:8px;width:100%;}
.si-mini div {border-top:1px solid rgba(244,237,225,.16);padding:10px 4px 0;text-align:center;}
.si-mini b {display:block;font-family:var(--si-serif);font-size:1.7rem;font-weight:600;line-height:1.1;}
.si-mini small {font-family:var(--si-mono);font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:rgba(244,237,225,.66);}
.si-count {--si-n:var(--to);counter-reset:si var(--si-n);}
.si-count::after {content:counter(si);}
.si-ticker {overflow:hidden;border-top:1px solid rgba(244,237,225,.12);padding:14px 0;white-space:nowrap;
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);}
.si-ticker div {display:inline-flex;gap:0;}
.si-ticker span {font-family:var(--si-serif);font-style:italic;font-size:1.15rem;color:rgba(244,237,225,.78);padding:0 22px;}
.si-ticker i {font-style:normal;color:var(--si-amber);padding-left:44px;}

/* Section headings: numbered editorial kickers */
.si-section {display:grid;grid-template-columns:auto 1fr;column-gap:16px;align-items:end;margin:44px 0 18px;counter-increment:sisec;
  padding-bottom:14px;border-bottom:1px solid var(--si-line);}
.si-section .si-ico {grid-row:span 2;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;font-size:1.35rem;
  background:rgba(14,12,9,.55);border:1px solid var(--si-line-2);backdrop-filter:blur(10px);}
.si-section h3 {margin:0;padding:0;font-size:clamp(1.45rem,2.3vw,2rem);font-weight:500;line-height:1.1;}
.si-section h3::before {content:counter(sisec,decimal-leading-zero) "  —  ";font-family:var(--si-mono);font-size:.7rem;letter-spacing:.14em;
  color:var(--si-amber);vertical-align:middle;font-weight:600;}
.si-section p {margin:4px 0 0;color:var(--si-muted);font-size:.92rem;}

/* Live estimate: a receipt strip */
.si-estimate {display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;padding:16px 20px;border-radius:16px;margin:4px 0 14px;
  background:rgba(14,12,9,.55);border:1px dashed rgba(232,176,74,.45);color:var(--si-ink);}
.si-estimate > span:first-child {font-family:var(--si-mono);font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--si-amber);}
.si-estimate b {font-family:var(--si-serif);font-size:1.5rem;font-weight:600;color:var(--si-ink);}
.si-estimate span {color:var(--si-muted);font-size:.86rem;}
.si-estimate .si-tag {padding:4px 11px;border-radius:999px;font-size:.74rem;font-weight:700;color:#17140F;background:var(--si-moss);}
.si-estimate .si-tag.si-new {background:var(--si-clay);color:#17140F;}

/* Goal rings */
.si-rings {display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:8px 0 6px;}
.si-ring {display:flex;align-items:center;gap:16px;padding:18px;border-radius:22px;background:var(--si-surface);border:1px solid var(--si-line);backdrop-filter:blur(14px);}
.si-ring-svg {position:relative;width:96px;height:96px;flex:none;}
.si-ring-svg svg {width:100%;height:100%;transform:rotate(-90deg);}
.si-ring-svg .si-track {stroke:rgba(244,237,225,.1);}
.si-ring-svg b {position:absolute;inset:0;display:grid;place-items:center;font-family:var(--si-serif);font-size:1.2rem;font-weight:600;color:var(--si-ink);}
.si-ring-txt strong {display:block;color:var(--si-ink);font-size:1rem;}
.si-ring-txt span {color:var(--si-muted);font-size:.84rem;line-height:1.5;}
.si-ring-txt em {display:inline-block;margin-top:6px;font-style:normal;font-size:.72rem;font-weight:700;padding:3px 10px;border-radius:999px;}
.si-ok {background:rgba(163,197,133,.18);color:#CFE6B8;border:1px solid rgba(163,197,133,.4);}
.si-over {background:rgba(224,122,95,.18);color:#F6C1B1;border:1px solid rgba(224,122,95,.4);}

/* Equivalents: photo-like tiles */
.si-equiv {display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.si-equiv div {position:relative;overflow:hidden;padding:24px;min-height:150px;border-radius:22px;color:#F4EDE1;border:1px solid var(--si-line);
  background:var(--si-surface);backdrop-filter:blur(14px);}
.si-equiv div::before {content:"";position:absolute;inset:auto -30% -60% auto;width:220px;height:220px;border-radius:50%;filter:blur(30px);opacity:.35;}
.si-equiv div:nth-child(1)::before {background:#E07A5F;} .si-equiv div:nth-child(2)::before {background:#9D8DF1;} .si-equiv div:nth-child(3)::before {background:#A3C585;}
.si-equiv i {position:absolute;right:14px;bottom:4px;font-size:3.6rem;font-style:normal;opacity:.5;}
.si-equiv b {position:relative;display:block;font-family:var(--si-serif);font-size:2.6rem;font-weight:500;letter-spacing:-.02em;}
.si-equiv span {position:relative;font-size:.86rem;color:var(--si-muted);}

/* Alternatives */
.si-alts {display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.si-alt {padding:22px;border-radius:20px;background:var(--si-surface);border:1px solid var(--si-line);backdrop-filter:blur(14px);
  transition:transform .5s var(--si-ease),border-color .3s ease;}
.si-alt:hover {transform:translateY(-6px);border-color:rgba(232,176,74,.5);}
.si-alt .si-num {font-family:var(--si-serif);font-style:italic;font-size:2rem;color:var(--si-amber);line-height:1;margin-bottom:12px;}
.si-alt p {margin:0;color:var(--si-ink);font-weight:500;line-height:1.55;}

/* Tip, story, badges, empty */
.si-tip {position:relative;padding:22px 24px;border-radius:22px;background:linear-gradient(135deg,rgba(232,176,74,.16),rgba(14,12,9,.6));
  border:1px solid rgba(232,176,74,.3);backdrop-filter:blur(14px);}
.si-tip small {font-family:var(--si-mono);font-weight:600;letter-spacing:.16em;font-size:.64rem;color:var(--si-amber);}
.si-tip p {margin:10px 0 0;font-family:var(--si-serif);font-size:1.18rem;line-height:1.45;color:var(--si-ink);font-style:italic;}
.si-story {display:flex;gap:16px;align-items:flex-start;padding:20px 24px;border-radius:20px;background:var(--si-surface);border:1px solid var(--si-line);
  border-left:3px solid var(--si-amber);margin:6px 0 20px;backdrop-filter:blur(14px);}
.si-story span {font-size:1.4rem;}
.si-story p {margin:0;color:var(--si-ink);line-height:1.6;font-family:var(--si-serif);font-size:1.12rem;}
.si-story p b {font-family:var(--si-mono);font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--si-amber);display:block;margin-bottom:4px;font-weight:600;}
.st-key-badges [data-testid="stAlert"] {background:rgba(163,197,133,.12);border:1px solid rgba(163,197,133,.35);}
.st-key-badges [data-testid="stAlert"] p {color:#DCEFC9;font-weight:600;}
.si-empty {text-align:center;padding:30px 18px;border-radius:20px;border:1px dashed var(--si-line-2);color:var(--si-muted);background:rgba(14,12,9,.4);}
.si-empty span {display:block;font-size:2.2rem;margin-bottom:8px;}

/* Journey */
.si-level {position:relative;overflow:hidden;display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center;padding:30px;border-radius:28px;
  color:#F4EDE1;background:linear-gradient(120deg,rgba(59,74,44,.75),rgba(14,12,9,.7));border:1px solid var(--si-line);backdrop-filter:blur(18px);}
.si-level .si-big {font-size:3.6rem;width:116px;height:116px;border-radius:50%;display:grid;place-items:center;background:rgba(14,12,9,.5);border:1px solid var(--si-line-2);}
.si-level h2 {color:#F4EDE1;margin:2px 0;font-size:clamp(1.9rem,3vw,2.6rem);font-weight:500;}
.si-level p {margin:4px 0 0;color:rgba(244,237,225,.8);}
.si-level > div > p:first-child {font-family:var(--si-mono);font-size:.68rem;letter-spacing:.16em;color:var(--si-amber);}
.si-bar {height:6px;border-radius:999px;background:rgba(244,237,225,.12);overflow:hidden;margin-top:16px;}
.si-bar i {display:block;height:100%;border-radius:999px;background:var(--si-grad);}
.si-path {display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;}
.si-path span {padding:5px 12px;border-radius:999px;font-size:.76rem;font-weight:600;border:1px solid rgba(244,237,225,.16);color:rgba(244,237,225,.75);}
.si-path span.si-here {background:#F4EDE1;color:#17140F;border-color:#F4EDE1;}
.si-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px;}
.si-medal {padding:20px;border-radius:22px;text-align:center;background:var(--si-surface);border:1px solid var(--si-line);backdrop-filter:blur(14px);
  transition:transform .5s var(--si-ease),border-color .3s ease;}
.si-medal:hover {transform:translateY(-6px);border-color:rgba(232,176,74,.45);}
.si-medal span {display:grid;place-items:center;margin:0 auto 12px;width:64px;height:64px;border-radius:50%;font-size:1.8rem;
  background:rgba(255,255,255,.05);border:1px solid var(--si-line-2);}
.si-medal.si-got span {background:radial-gradient(circle at 30% 25%,#F4D28A,#B7791F 75%);border-color:#E8B04A;box-shadow:0 0 0 4px rgba(232,176,74,.14),0 14px 30px -12px #E8B04A;}
.si-medal b {display:block;color:var(--si-ink);font-family:var(--si-serif);font-weight:600;font-size:1.05rem;}
.si-medal small {color:var(--si-muted);line-height:1.45;display:block;margin-top:4px;}
.si-medal em {display:inline-block;margin-top:12px;font-style:normal;font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:999px;}
.si-medal.si-locked {opacity:.55;filter:grayscale(.7);}
.si-points {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.si-points div {padding:18px;border-radius:18px;background:var(--si-surface);border:1px solid var(--si-line);backdrop-filter:blur(14px);}
.si-points b {display:block;font-family:var(--si-serif);font-size:2rem;color:var(--si-ink);font-weight:500;}
.si-points small {color:var(--si-muted);}

/* Wishlist: tags on a rail */
.si-wish {display:flex;gap:16px;align-items:center;padding:16px 20px;border-radius:20px;background:var(--si-surface);border:1px solid var(--si-line);
  margin-bottom:8px;backdrop-filter:blur(14px);transition:border-color .3s ease,transform .5s var(--si-ease);}
.si-wish:hover {border-color:rgba(232,176,74,.4);transform:translateX(4px);}
.si-wish .si-wi {font-size:1.6rem;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.05);border:1px solid var(--si-line-2);flex:none;}
.si-wish b {color:var(--si-ink);font-family:var(--si-serif);font-size:1.15rem;font-weight:600;}
.si-wish p {margin:2px 0 6px;color:var(--si-muted);font-size:.84rem;}
.si-wish .si-days {margin-left:auto;text-align:right;}
.si-wish .si-days strong {display:block;font-family:var(--si-serif);font-size:1.8rem;font-weight:500;color:var(--si-ink);line-height:1;}
.si-wish .si-days small {color:var(--si-muted);font-family:var(--si-mono);font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;}
.si-ready {font-size:.72rem;font-weight:700;padding:3px 10px;border-radius:999px;background:rgba(163,197,133,.18);color:#CFE6B8;border:1px solid rgba(163,197,133,.4);}
.si-cool {font-size:.72rem;font-weight:700;padding:3px 10px;border-radius:999px;background:rgba(138,180,248,.15);color:#C7DAFB;border:1px solid rgba(138,180,248,.35);}

/* Sign-in cover */
.si-eyebrow,.si-brand .si-eyebrow {font-family:var(--si-mono);font-size:.68rem;letter-spacing:.16em;font-weight:600;color:var(--si-amber);margin-bottom:12px;text-transform:uppercase;}
.si-brand {border-radius:32px;padding:0;color:#F4EDE1;min-height:600px;position:relative;overflow:hidden;margin:0 10px 22px 0;isolation:isolate;
  border:1px solid var(--si-line);box-shadow:0 50px 90px -50px #000;display:flex;flex-direction:column;justify-content:space-between;}
.si-brand video,.si-brand .si-poster {position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;
  filter:sepia(.25) saturate(.95) brightness(.6) contrast(1.06);}
.si-brand .si-poster {background:radial-gradient(80% 90% at 80% 10%,#3B4A2C,#17140F 70%);}
.si-brand::before {content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(14,12,9,.95),rgba(14,12,9,.35) 60%,rgba(14,12,9,.55));}
.si-brand > div {padding:30px 36px;}
.si-brand h2 {color:#F4EDE1;font-family:var(--si-serif);font-weight:400;font-size:clamp(2.6rem,4.4vw,4.4rem);line-height:.98;margin:0 0 18px;letter-spacing:-.035em;}
.si-brand p {color:rgba(244,237,225,.84);font-size:1.02rem;line-height:1.7;max-width:460px;}
.si-brand .si-wordmark {display:flex;align-items:center;justify-content:space-between;gap:10px;color:#F4EDE1;font-family:var(--si-serif);font-size:1.35rem;font-weight:600;
  border-bottom:1px solid rgba(244,237,225,.14);}
.si-brand .si-wordmark small {font-family:var(--si-mono);font-size:.62rem;letter-spacing:.16em;font-weight:500;color:rgba(244,237,225,.7);}
.si-feats {display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:24px;border-top:1px solid rgba(244,237,225,.14);}
.si-feats span {padding:12px 4px;font-size:.86rem;font-weight:500;border-bottom:1px solid rgba(244,237,225,.1);color:rgba(244,237,225,.88);}
.si-brand .si-globe {display:none;}
.si-auth-note {font-size:.82rem;color:var(--si-muted);padding-top:12px;}

/* Scenery (over the footage) */
.si-scenery {position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:0;}
.si-hero,.si-brand,.si-level,.si-section,.si-alts,.si-equiv,.si-grid,.si-rings,.si-points {position:relative;z-index:1;}
.si-blob {position:absolute;border-radius:50%;filter:blur(90px);opacity:.18;}
.si-blob-1 {width:560px;height:560px;left:-160px;top:-160px;background:#A3C585;}
.si-blob-2 {width:480px;height:480px;right:-140px;bottom:-160px;background:#E8B04A;}
.si-leaf {position:absolute;top:-40px;font-style:normal;font-size:18px;opacity:0;}
.si-leaf-1 {left:8%;--d:0s;--t:21s;} .si-leaf-2 {left:24%;--d:6s;--t:25s;} .si-leaf-3 {left:46%;--d:11s;--t:23s;}
.si-leaf-4 {left:63%;--d:3s;--t:27s;} .si-leaf-5 {left:80%;--d:9s;--t:22s;} .si-leaf-6 {left:93%;--d:15s;--t:26s;}
.si-night {background-image:radial-gradient(1.5px 1.5px at 18% 15%,#E0EAFF 98%,transparent),radial-gradient(1px 1px at 62% 28%,#CCDFFF 98%,transparent),
  radial-gradient(1.2px 1.2px at 85% 60%,#CCDFFF 98%,transparent),radial-gradient(1px 1px at 40% 80%,#FDE68A 98%,transparent);background-size:270px 230px;}
.si-star {position:absolute;width:110px;height:2px;background:linear-gradient(90deg,transparent,#DAE8FF);opacity:0;transform:rotate(35deg);border-radius:50%;}
.si-star-1 {left:12%;top:8%;--delay:0s;} .si-star-2 {left:48%;top:16%;--delay:4s;} .si-star-3 {left:70%;top:4%;--delay:8s;}
.si-star-4 {left:25%;top:35%;--delay:12s;} .si-star-5 {left:55%;top:48%;--delay:16s;}
.si-moon {position:absolute;right:8%;top:9%;width:84px;height:84px;border-radius:50%;box-shadow:-18px 10px 0 0 #FDE68A;transform:rotate(-20deg);opacity:.8;}
.si-sun {position:absolute;right:9%;top:8%;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,#FFF4C7,#F4B940);
  box-shadow:0 0 120px 60px rgba(244,185,64,.35);opacity:.7;}
.si-cloud {position:absolute;width:190px;height:45px;border-radius:80px;background:#FFF8EA;opacity:.16;}
.si-cloud::before,.si-cloud::after {content:"";position:absolute;background:inherit;border-radius:50%;}
.si-cloud::before {width:80px;height:80px;left:30px;bottom:0;} .si-cloud::after {width:100px;height:100px;right:25px;bottom:0;}
.si-cloud-1 {left:8%;top:18%;} .si-cloud-2 {left:55%;top:64%;} .si-cloud-3 {left:30%;top:40%;transform:scale(.6);}

/* Background footage layer per theme (the layer itself is added by the motion script) */
body:has(.si-day) #si-video video {filter:sepia(.2) saturate(1.05) brightness(.78) contrast(1.04);}
body:has(.si-day) #si-veil {background:linear-gradient(180deg,rgba(40,26,8,.25),rgba(24,16,8,.55) 50%,rgba(14,12,9,.82)),radial-gradient(70% 60% at 85% 0%,rgba(244,185,64,.3),transparent 60%);}
body:has(.si-night) #si-video video {filter:saturate(.6) hue-rotate(185deg) brightness(.38) contrast(1.1);}
body:has(.si-night) #si-veil {background:linear-gradient(180deg,rgba(7,13,31,.55),rgba(7,13,31,.82) 50%,rgba(7,13,31,.95));}
body:has(.si-night) .stApp {--si-amber:#F2C66D;--si-surface:rgba(12,18,36,.66);}
body:has(.si-paused) #si-video,body:has(.si-paused) #si-webgl {display:none;}
body:has(.si-paused) {background:radial-gradient(80% 80% at 80% 0%,#2A2416,#0E0C09 70%);}

/* Motion */
@media (prefers-reduced-motion:no-preference) {
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"],
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  .stApp [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {animation:si-rise .9s var(--si-ease) backwards;}
  .stApp [data-testid="stVerticalBlock"] > :nth-child(2) {animation-delay:.05s;} .stApp [data-testid="stVerticalBlock"] > :nth-child(3) {animation-delay:.1s;}
  .stApp [data-testid="stVerticalBlock"] > :nth-child(4) {animation-delay:.15s;} .stApp [data-testid="stVerticalBlock"] > :nth-child(n+5) {animation-delay:.2s;}
  .stApp [data-testid="stMetric"] {transition:transform .5s var(--si-ease),border-color .3s ease;}
  .stApp [data-testid="stMetric"]:hover {transform:translateY(-6px);border-color:rgba(232,176,74,.4);}
  .stApp [data-testid="stMetricValue"] {animation:si-pop .9s var(--si-ease) backwards .25s;}
  .si-mask > span {animation:si-up 1.2s var(--si-ease) backwards;} .si-mask:nth-child(2) > span {animation-delay:.12s;} .si-mask:nth-child(3) > span {animation-delay:.24s;}
  .si-hero video,.si-brand video {animation:si-kenburns 24s ease-in-out infinite alternate;}
  .si-ticker div {animation:si-marquee 40s linear infinite;}
  .si-chip .si-dot {animation:si-ping 2.2s infinite;}
  .si-orb .si-arc,.si-ring-svg .si-arc {animation:si-draw 1.8s var(--si-ease) backwards .3s;}
  .si-orb .si-orb-in span {animation:si-bob 5s ease-in-out infinite;}
  .si-count {animation:si-count 2s var(--si-ease);}
  .si-mini div,.si-equiv div,.si-alt,.si-medal,.si-wish,.si-points div,.si-feats span,.si-hero-side {animation:si-rise .9s var(--si-ease) backwards;}
  .si-hero-side {animation-delay:.35s;}
  .si-mini div:nth-child(2),.si-equiv div:nth-child(2),.si-alt:nth-child(2),.si-medal:nth-child(2),.si-points div:nth-child(2),.si-feats span:nth-child(2) {animation-delay:.12s;}
  .si-mini div:nth-child(3),.si-equiv div:nth-child(3),.si-alt:nth-child(3),.si-medal:nth-child(3),.si-points div:nth-child(3),.si-feats span:nth-child(3) {animation-delay:.24s;}
  .si-medal:nth-child(4),.si-points div:nth-child(4),.si-feats span:nth-child(4) {animation-delay:.36s;}
  .si-medal:nth-child(n+5) {animation-delay:.48s;}
  .si-bar i {animation:si-grow 1.8s var(--si-ease) backwards .3s;transform-origin:left;}
  .st-key-badges [data-testid="stAlert"] {animation:si-pop .8s var(--si-ease) backwards;}
  .si-equiv i {animation:si-bob 6s ease-in-out infinite;}
  .si-blob {animation:si-blob 26s ease-in-out infinite alternate;} .si-blob-2 {animation-duration:32s;animation-delay:-10s;}
  .si-leaf {animation:si-leaf var(--t) linear infinite;animation-delay:var(--d);}
  .si-star {animation:si-fall 22s linear infinite;animation-delay:var(--delay);}
  .si-cloud {animation:si-drift 60s ease-in-out infinite alternate;} .si-cloud-2 {animation-delay:-25s;}
  .si-sun,.si-moon {animation:si-glow 12s ease-in-out infinite alternate;}
}
@keyframes si-rise {from {opacity:0;transform:translateY(26px);}}
@keyframes si-up {from {transform:translateY(110%);}}
@keyframes si-pop {from {opacity:0;transform:scale(.9);}}
@keyframes si-kenburns {from {transform:scale(1.04);} to {transform:scale(1.14) translate(-1.5%,-1%);}}
@keyframes si-marquee {to {transform:translateX(-50%);}}
@keyframes si-bob {0%,100% {transform:translateY(0);} 50% {transform:translateY(-6px);}}
@keyframes si-ping {0% {box-shadow:0 0 0 0 rgba(163,197,133,.9);} 80%,100% {box-shadow:0 0 0 10px rgba(163,197,133,0);}}
@keyframes si-draw {from {stroke-dashoffset:var(--c);}}
@keyframes si-count {from {--si-n:0;}}
@keyframes si-grow {from {transform:scaleX(0);}}
@keyframes si-blob {0% {transform:translate(0,0) scale(1);} 50% {transform:translate(80px,40px) scale(1.12);} 100% {transform:translate(-40px,90px) scale(.95);}}
@keyframes si-leaf {0% {opacity:0;transform:translate(0,0) rotate(0);} 8% {opacity:.45;} 92% {opacity:.35;} 100% {opacity:0;transform:translate(90px,110vh) rotate(540deg);}}
@keyframes si-fall {0%,6% {opacity:0;transform:translate(0,0) rotate(35deg);} 8% {opacity:.7;} 16% {opacity:0;transform:translate(340px,238px) rotate(35deg);} 100% {opacity:0;}}
@keyframes si-drift {to {transform:translateX(120px);}}
@keyframes si-glow {to {transform:scale(1.07);opacity:.95;}}
.si-paused *,.si-paused *::before,.si-paused *::after {animation:none!important;}
@media (prefers-reduced-motion:reduce) {.si-scenery * {animation:none!important;} .si-leaf {display:none;} #si-video,#si-webgl {display:none;}}

/* Responsive */
@media (max-width:1100px) {
  .stApp [data-testid="stMainBlockContainer"] {padding-left:1.4rem;padding-right:1.4rem;}
  .si-hero-body {grid-template-columns:1fr;} .si-alts,.si-equiv {grid-template-columns:1fr 1fr;} .si-points {grid-template-columns:1fr 1fr;}
}
@media (max-width:760px) {
  .stApp [data-testid="stMainBlockContainer"] {padding-top:4.5rem;padding-left:1rem;padding-right:1rem;}
  .stApp [data-testid="stHorizontalBlock"] {row-gap:1rem;}
  .si-hero {min-height:0;border-radius:24px;} .si-hero-body,.si-meta {padding-left:20px;padding-right:20px;}
  .si-meta span:nth-child(2) {display:none;}
  .si-brand {min-height:420px;margin-right:0;} .si-brand > div {padding:22px;} .si-feats {display:none;}
  .si-alts,.si-equiv,.si-rings {grid-template-columns:1fr;} .si-level {grid-template-columns:1fr;text-align:center;}
  .si-level .si-big {margin:0 auto;}
  .stApp [data-testid="stMetric"] {min-height:104px;padding:16px 18px;}
}
</style>"""

NIGHT_CSS = """<style>
.stApp {--si-surface:rgba(12,18,36,.66);--si-line:rgba(180,196,240,.14);--si-line-2:rgba(180,196,240,.24);--si-moss:#9FD0B8;}
.stApp [data-testid="stSidebar"] {background:rgba(7,12,28,.82);}
.si-hero video,.si-brand video {filter:saturate(.55) hue-rotate(185deg) brightness(.45) contrast(1.1);}
.si-hero::before,.si-brand::before {background:linear-gradient(90deg,rgba(7,13,31,.9),rgba(7,13,31,.5) 50%,rgba(7,13,31,.25)),linear-gradient(0deg,rgba(7,13,31,.9),transparent 45%);}
.si-level {background:linear-gradient(120deg,rgba(30,27,75,.75),rgba(7,13,31,.7));}
</style>"""

DAY_CSS = """<style>
.stApp {--si-amber:#F4B940;--si-surface:rgba(30,22,12,.58);}
.si-hero video,.si-brand video {filter:sepia(.15) saturate(1.1) brightness(.78) contrast(1.04);}
.si-hero::before {background:linear-gradient(90deg,rgba(30,20,8,.82),rgba(30,20,8,.4) 50%,rgba(244,185,64,.12)),linear-gradient(0deg,rgba(14,12,9,.85),transparent 45%);}
.si-level {background:linear-gradient(120deg,rgba(120,80,20,.6),rgba(14,12,9,.7));}
</style>"""

CONTRAST_CSS = """<style>
html,body {background:#000!important;}
.stApp {--si-ink:#FFFFFF;--si-muted:#FFFFFF;--si-dim:#FFFFFF;--si-line:#FFFFFF;--si-line-2:#FFFFFF;--si-surface:#000000;--si-solid:#000000;--si-raise:#000;
  --si-amber:#FFD400;--si-moss:#FFD400;--si-clay:#FFD400;--si-grad:linear-gradient(#FFD400,#FFD400);--si-shadow:none;background:#000!important;color:#FFF;}
.si-hero,.si-brand,.si-level,.si-equiv div,.si-tip,.si-hero-side {background:#000!important;box-shadow:none!important;border:2px solid #FFF!important;}
.si-hero video,.si-brand video,.si-hero::before,.si-brand::before,.si-equiv div::before {display:none!important;}
.si-hero p,.si-hero h1,.si-brand p,.si-brand h2,.si-mini small,.si-meta,.si-ticker span {color:#FFF!important;}
.stApp [data-testid="stBaseButton-primary"],.stApp [data-testid="stBaseButton-primaryFormSubmit"] {background:#FFD400;}
#si-video,#si-veil,#si-grain,#si-webgl {display:none!important;}
.stApp *,.stApp *::before,.stApp *::after {animation:none!important;backdrop-filter:none!important;}
</style>"""


def apply_styles(high_contrast=False):
    """Apply the base design plus the selected theme or high-contrast overrides."""
    theme = theme_name()
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    if high_contrast:
        st.markdown(CONTRAST_CSS, unsafe_allow_html=True)
    elif theme == "Night":
        st.markdown(NIGHT_CSS, unsafe_allow_html=True)
    elif theme == "Day":
        st.markdown(DAY_CSS, unsafe_allow_html=True)
    if high_contrast:
        st.markdown('<style>.si-scenery {display:none;}</style>', unsafe_allow_html=True)


# Runs in the Streamlit page's own window (injected once as a <script> element), so its timers survive reruns.
FX_CORE = r"""
(function(){
  const P = window, D = document;
  if (P.__shopFX) { P.__shopFX.refresh && P.__shopFX.refresh(); return; }
  P.__shopFX = { version: 1 };
  const reduce = P.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = P.matchMedia('(pointer: coarse)').matches;

  /* 1 ── colour-graded market & forest footage, crossfading ── */
  const CLIPS = __CLIPS__;
  const Q = touch ? 360 : 720;
  const st = D.createElement('style');
  st.textContent = `
    #si-video{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:radial-gradient(80% 80% at 80% 0%,#2A2416,#0E0C09 70%)}
    #si-video video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
      filter:sepia(.3) saturate(.9) brightness(.55) contrast(1.08);transform:scale(1.06);
      transition:opacity 2.6s cubic-bezier(.16,1,.3,1),transform 16s linear}
    #si-video video.on{opacity:1;transform:scale(1.14)}
    #si-veil{position:fixed;inset:0;z-index:0;pointer-events:none;
      background:linear-gradient(180deg,rgba(14,12,9,.35),rgba(14,12,9,.62) 45%,rgba(14,12,9,.9)),
                 radial-gradient(70% 60% at 85% 0%,rgba(163,197,133,.14),transparent 60%)}
    #si-grain{position:fixed;inset:-50%;z-index:1;pointer-events:none;opacity:.08;mix-blend-mode:overlay;
      background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
      animation:sigrain .9s steps(5) infinite}
    @keyframes sigrain{20%{transform:translate(-3%,2%)}40%{transform:translate(2%,-3%)}60%{transform:translate(-2%,-1%)}80%{transform:translate(3%,3%)}}`;
  D.head.appendChild(st);
  const vwrap = D.createElement('div'); vwrap.id = 'si-video';
  const veil = D.createElement('div'); veil.id = 'si-veil';
  const grain = D.createElement('div'); grain.id = 'si-grain';
  /* Two looping players: the next clip preloads after every swap and only swaps in once buffered;
     a watchdog restarts stalled playback, so the background never goes black. */
  const mk = () => { const v = D.createElement('video'); v.muted = true; v.defaultMuted = true; v.playsInline = true; v.loop = true;
    v.setAttribute('muted',''); v.setAttribute('playsinline',''); v.setAttribute('loop',''); v.preload = 'auto'; vwrap.appendChild(v); return v; };
  const A = mk(), B = mk(); let idx = 0, cur = A, nxt = B, busy = false, lastT = -1, stuck = 0;
  const src = i => `https://assets.mixkit.co/videos/${CLIPS[i]}/${CLIPS[i]}-${Q}.mp4`;
  const play = v => { const p = v.play(); if (p && p.catch) p.catch(()=>{}); };
  function preload(){ nxt.src = src((idx + 1) % CLIPS.length); nxt.load(); }
  A.src = src(0);
  A.addEventListener('playing', ()=>{ A.classList.add('on'); preload(); }, {once:true});
  play(A);
  function swap(force){
    if (busy || D.hidden) return;
    if (nxt.readyState < 3 && !force) return;
    busy = true;
    const incoming = nxt, outgoing = cur;
    incoming.currentTime = 0; play(incoming);
    incoming.classList.add('on'); outgoing.classList.remove('on');
    cur = incoming; nxt = outgoing; idx = (idx + 1) % CLIPS.length; lastT = -1; stuck = 0;
    setTimeout(()=>{ outgoing.pause(); preload(); busy = false; }, 2800);
  }
  [A,B].forEach(v=>v.addEventListener('error', ()=>{ if (v === nxt && !busy) { idx = (idx + 1) % CLIPS.length; preload(); } }));
  if (!reduce) P.setInterval(()=>swap(false), 13000);
  P.setInterval(()=>{
    if (D.hidden) return;
    if (cur.paused) play(cur);
    if (Math.abs(cur.currentTime - lastT) < 0.01) { if (++stuck >= 4 && nxt.readyState >= 2) swap(true); } else stuck = 0;
    lastT = cur.currentTime;
    if (!cur.classList.contains('on') && !busy) cur.classList.add('on');
  }, 2000);
  D.addEventListener('visibilitychange', ()=>{ if (D.hidden) { cur.pause(); } else { play(cur); } });
  ['pointerdown','touchstart','keydown'].forEach(ev=>D.addEventListener(ev, ()=>{ if (cur.paused) play(cur); }, {passive:true}));
  D.body.prepend(grain); D.body.prepend(veil); D.body.prepend(vwrap);

  /* 2 ── warm bokeh drifting through the light (Three.js) ── */
  const host = D.createElement('div'); host.id = 'si-webgl';
  host.style.cssText = 'position:fixed;inset:0;z-index:1;pointer-events:none;opacity:0;transition:opacity 2.5s cubic-bezier(.16,1,.3,1)';
  veil.after(host);
  const mod = D.createElement('script'); mod.type = 'module';
  mod.textContent = `
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
    const host = document.getElementById('si-webgl');
    const R = new THREE.WebGLRenderer({antialias:false, alpha:true, powerPreference:'low-power'});
    R.setPixelRatio(Math.min(devicePixelRatio, 1.5)); R.setSize(innerWidth, innerHeight); host.appendChild(R.domElement);
    const scene = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, .1, 100); cam.position.z = 12;
    const N = __N__, pos = new Float32Array(N*3), seed = new Float32Array(N);
    for (let i=0;i<N;i++){ pos[i*3]=(Math.random()-.5)*30; pos[i*3+1]=(Math.random()-.5)*18; pos[i*3+2]=(Math.random()-.5)*14; seed[i]=Math.random(); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos,3)); g.setAttribute('seed', new THREE.BufferAttribute(seed,1));
    const m = new THREE.ShaderMaterial({ transparent:true, depthWrite:false, blending:THREE.AdditiveBlending,
      uniforms:{t:{value:0}, px:{value:R.getPixelRatio()}, mouse:{value:new THREE.Vector2()}},
      vertexShader:\`attribute float seed; uniform float t; uniform float px; uniform vec2 mouse; varying float vS; varying float vZ;
        void main(){ vec3 p=position; float s=seed*6.2831;
          p.x += sin(t*.08+s)*1.6 + t*.1*(seed-.3); p.y += cos(t*.06+s*1.3)*1.1 + sin(t*.15+s)*.3;
          p.x = mod(p.x+15.,30.)-15.; p.xy += mouse*(.4+seed)*.6;
          vec4 mv = modelViewMatrix*vec4(p,1.); gl_Position = projectionMatrix*mv;
          gl_PointSize = (6. + 30.*seed*seed) * px / -mv.z; vS=seed; vZ=-mv.z; }\`,
      fragmentShader:\`varying float vS; varying float vZ; uniform float t;
        void main(){ float d=length(gl_PointCoord-.5); float soft=pow(smoothstep(.5,.0,d),2.2);
          float tw=.6+.4*sin(t*.9+vS*50.); vec3 c=mix(vec3(.64,.77,.52), vec3(1.,.82,.5), vS);
          float a = soft * tw * mix(.5,.16,smoothstep(.6,1.,vS)) * smoothstep(22.,6.,vZ);
          gl_FragColor=vec4(c, a); }\`});
    scene.add(new THREE.Points(g, m));
    let mx=0,my=0,tx=0,ty=0; addEventListener('pointermove',e=>{ tx=e.clientX/innerWidth-.5; ty=.5-e.clientY/innerHeight; },{passive:true});
    addEventListener('resize',()=>{ R.setSize(innerWidth,innerHeight); cam.aspect=innerWidth/innerHeight; cam.updateProjectionMatrix(); });
    let run=true; document.addEventListener('visibilitychange',()=>{ run=!document.hidden; if(run) loop(); });
    const clock = new THREE.Clock();
    function loop(){ if(!run) return; requestAnimationFrame(loop); mx+=(tx-mx)*.03; my+=(ty-my)*.03;
      m.uniforms.t.value=clock.getElapsedTime(); m.uniforms.mouse.value.set(mx,my); R.render(scene,cam); }
    loop(); requestAnimationFrame(()=>host.style.opacity=1);
  `.replace('__N__', touch ? 220 : 600);
  if (!reduce) D.head.appendChild(mod);

  /* 3 ── gentle 3D tilt on cards ── */
  const TILT = '.si-alt,.si-medal,.si-equiv div,.si-hero-side,[data-testid="stMetric"]';
  if (!touch && !reduce) D.addEventListener('pointermove', e=>{
    const c = e.target.closest && e.target.closest(TILT);
    D.querySelectorAll('[data-si-t]').forEach(t=>{ if(t!==c){ t.removeAttribute('data-si-t'); t.style.transform=''; } });
    if (!c) return; const r=c.getBoundingClientRect(); const x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
    c.dataset.siT=1; c.style.transform=`perspective(900px) rotateY(${x*6}deg) rotateX(${-y*6}deg) translateY(-4px)`; }, {passive:true});

  /* 4 ── keep inline footage (hero, sign-in cover) playing across reruns ── */
  function scan(){
    D.querySelectorAll('video[autoplay]:not([data-si])').forEach(v=>{ v.dataset.si=1; v.muted=true; v.defaultMuted=true; v.playsInline=true;
      const go=()=>v.play().catch(()=>{}); if(v.readyState>=2) go(); else v.addEventListener('canplay',go,{once:true}); });
    if (!D.hidden) D.querySelectorAll('video[autoplay][data-si]').forEach(v=>{ if (v.paused && v.readyState>=2) v.play().catch(()=>{}); }); }
  P.setInterval(()=>{ try { scan(); } catch (e) {} }, 800);
  P.__shopFX.refresh = scan;
  new P.MutationObserver(()=>{ clearTimeout(P.__siT); P.__siT=setTimeout(scan,60); }).observe(D.body,{childList:true,subtree:true});
  scan();
})();
""".replace("__CLIPS__", json.dumps(CLIPS))

# The helper iframe only hides itself and injects FX_CORE into the page once; it keeps no timers of its own.
FX_JS = """<script>
(function(){
  try { const fe = window.frameElement; if (fe) fe.style.cssText = 'position:fixed;width:0;height:0;border:0;opacity:0;pointer-events:none'; } catch (e) {}
  const P = window.parent, D = P.document;
  if (P.__shopFX) { try { P.__shopFX.refresh && P.__shopFX.refresh(); } catch (e) {} return; }
  const s = D.createElement('script'); s.id = 'shopimpact-fx-core'; s.textContent = __CORE__; D.head.appendChild(s);
})();
</script>""".replace("__CORE__", json.dumps(FX_CORE).replace("</", "<\\/"))


def _inject_fx():
    """Background footage, bokeh and tilt: injected once into the page, so it keeps running across reruns."""
    with st.container(key="fxloader", height=1, border=False):
        components.html(FX_JS, height=0)
    st.markdown("<style>.st-key-fxloader{position:absolute!important;width:0;height:0;overflow:hidden;opacity:0;pointer-events:none}</style>",
                unsafe_allow_html=True)


def html(markup):
    """Render app-generated HTML markup through Streamlit's markdown renderer."""
    st.markdown(markup, unsafe_allow_html=True)


def sidebar_brand(username, level):
    """Render the account identity and current eco level in the sidebar."""
    initial = escape((username or "?")[:1].upper())
    html(f"""<div class="si-side-brand"><div class="si-logo" aria-hidden="true">🌿</div>
    <div><b>ShopImpact</b><small>Conscious shopping journal</small></div></div>
    <div class="si-user"><div class="si-avatar" aria-hidden="true">{initial}</div>
    <div><b>{escape(username)}</b><small>{level['icon']} Level {level['number']} · {escape(level['name'])}</small></div></div>""")


def _arc(progress, size, stroke, gradient_id, colors):
    """Build an SVG progress ring, clamping displayed progress between zero and one."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - max(0.0, min(progress, 1.0)))
    stops = "".join(f'<stop offset="{i / (len(colors) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(colors))
    return (f'<svg viewBox="0 0 {size} {size}" aria-hidden="true"><defs><linearGradient id="{gradient_id}" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient></defs>'
            f'<circle class="si-track" cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="rgba(244,237,225,.14)" stroke-width="{stroke}"/>'
            f'<circle class="si-arc" cx="{size / 2}" cy="{size / 2}" r="{radius}" fill="none" stroke="url(#{gradient_id})" stroke-width="{stroke}" '
            f'stroke-linecap="round" style="--c:{circumference:.1f};stroke-dasharray:{circumference:.1f};stroke-dashoffset:{offset:.1f}"/></svg>')


def _ticker(words):
    """Build a decorative duplicated text ticker hidden from assistive technology."""
    items = "".join(f"<span>{escape(w)}<i>✳</i></span>" for w in words * 2)
    return f'<div class="si-ticker" aria-hidden="true"><div>{items}</div></div>'


def hero(username, level, streak, skips, month_label):
    """Render the welcome panel with the user's level and journey counters."""
    orb = _arc(level["progress"], 150, 8, "si-orb-grad", ["#A3C585", "#E8B04A", "#E07A5F"])
    nxt = f"{level['to_next']} pts to {escape(level['next_name'])}" if level["next_name"] else "Top level reached"
    ticker = _ticker(["Buy less, choose well", "Second-hand first", "Repair before replace", "Pause before you buy",
                      "Every receipt tells a story", "Small choices add up"])
    html(f"""<section class="si-hero">
<div class="si-poster"></div><video autoplay muted loop playsinline preload="metadata"><source src="{HERO_VIDEO}" type="video/mp4"></video>
<div class="si-meta"><span class="si-chip"><i class="si-dot"></i> {escape(month_label)}</span><span>ShopImpact · Conscious shopping journal</span><span>🔒 Private journal</span></div>
<div class="si-hero-body">
<div>
<p class="si-greet">Welcome back, {escape(username)} 👋</p>
<h1><span class="si-mask"><span>A little more</span></span><span class="si-mask"><span><span class="si-shine">mindful</span>,</span></span><span class="si-mask"><span>every month.</span></span></h1>
<p class="si-lede">Know where your money goes. Explore your estimated impact. Pause before you buy, and celebrate every thoughtful choice.</p>
</div>
<div class="si-hero-side">
<div class="si-orb">{orb}<div class="si-orb-in"><span aria-hidden="true">{level['icon']}</span><b>Level {level['number']} · {escape(level['name'])}</b><small>{nxt}</small></div></div>
<div class="si-mini">
<div><b class="si-count" style="--to:{level['points']}"></b><small>eco points</small></div>
<div><b class="si-count" style="--to:{streak}"></b><small>🔥 month streak</small></div>
<div><b class="si-count" style="--to:{skips}"></b><small>⏸️ mindful skips</small></div>
</div></div></div>
{ticker}
</section>""")


def section(icon, title, subtitle=""):
    """Render a consistent section heading, escaping user-visible text."""
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    html(f'<div class="si-section"><div class="si-ico" aria-hidden="true">{icon}</div><div><h3>{escape(title)}</h3>{sub}</div></div>')


def estimate_pill(kg, factor, category, lower, equivalent):
    """Show the live estimate, category factor, choice type, and everyday equivalent."""
    tag = '<span class="si-tag">♻️ Reuse / repair choice</span>' if lower else '<span class="si-tag si-new">🛍️ New purchase</span>'
    html(f"""<div class="si-estimate" role="status"><span>Live preview</span><b>{kg:,.2f} kg CO₂e</b>{tag}
<span>{CATEGORY_ICONS.get(category, '🛒')} reference factor {factor:.6f} per INR · ≈ {equivalent['value']:,} {escape(equivalent['label'])}</span></div>""")


def goal_rings(items):
    """Render spending and impact goal rings with a distinct over-goal state."""
    cards = []
    for index, (icon, label, used, goal, unit) in enumerate(items):
        share = used / goal if goal else 0
        over = share > 1
        colors = ["#E8B04A", "#E07A5F"] if over else (["#A3C585", "#E8B04A"] if index == 0 else ["#6CC4C9", "#9D8DF1"])
        ring = _arc(share, 96, 8, f"si-ring-{index}", colors)
        status = '<em class="si-over">Above goal</em>' if over else '<em class="si-ok">Within goal</em>'
        cards.append(f"""<div class="si-ring"><div class="si-ring-svg">{ring}<b>{share:.0%}</b></div>
<div class="si-ring-txt"><strong>{icon} {escape(label)}</strong><span>{unit} {used:,.2f} of {unit} {goal:,.2f}</span><br>{status}</div></div>""")
    html(f'<div class="si-rings">{"".join(cards)}</div>')


def equivalents_cards(rows):
    """Render sourced everyday equivalents as labelled visual cards."""
    cards = "".join(f'<div><i aria-hidden="true">{r["icon"]}</i><b>{r["value"]:,}</b><span>{escape(r["label"])}</span></div>' for r in rows)
    html(f'<div class="si-equiv">{cards}</div>')


def alternatives_cards(ideas):
    """Render numbered lower-impact alternatives as labelled visual cards."""
    cards = "".join(f'<div class="si-alt"><div class="si-num" aria-hidden="true">{i:02d}</div><p>{escape(text)}</p></div>' for i, text in enumerate(ideas, 1))
    html(f'<div class="si-alts">{cards}</div>')


def tip_card(tip):
    """Display one short shopping suggestion in the shared tip-card style."""
    html(f'<div class="si-tip"><small>✨ A SMALL IDEA</small><p>{escape(tip)}</p></div>')


def story_card(text):
    """Display the selected month's summary sentence in a story-card layout."""
    html(f'<div class="si-story"><span aria-hidden="true">📖</span><p><b>Your month in a sentence:</b> {escape(text)}</p></div>')


def empty_state(icon, text):
    """Explain an empty view with a decorative icon and escaped text."""
    html(f'<div class="si-empty"><span aria-hidden="true">{icon}</span>{escape(text)}</div>')


def level_card(level, levels):
    """Show current level progress and the ordered path of available levels."""
    width = max(level["progress"], 0.02) * 100
    nxt = f"{level['to_next']} points to {escape(level['next_icon'])} {escape(level['next_name'])}" if level["next_name"] else "You've reached the top level — keep growing your forest!"
    path = "".join(f'<span class="{"si-here" if n == level["name"] else ""}">{i} {escape(n)}</span>' for _, n, i in levels)
    html(f"""<div class="si-level"><div class="si-big" aria-hidden="true">{level['icon']}</div>
<div><p>LEVEL {level['number']} · {level['points']} ECO POINTS</p><h2>{escape(level['name'])}</h2><p>{nxt}</p>
<div class="si-bar" role="img" aria-label="{level['progress']:.0%} of the way to the next level"><i style="width:{width:.1f}%"></i></div>
<div class="si-path">{path}</div></div></div>""")


def points_grid(breakdown):
    """Render the labelled point totals that make up the user's eco score."""
    cells = "".join(f'<div><b class="si-count" style="--to:{value}"></b><small>{escape(label)}</small></div>' for label, value in breakdown.items())
    html(f'<div class="si-points">{cells}</div>')


def medal_grid(items):
    """Render earned and locked milestones with their names and unlocking rules."""
    cards = []
    for item in items:
        state = "si-got" if item["earned"] else "si-locked"
        tag = '<em class="si-ok">Unlocked</em>' if item["earned"] else '<em class="si-over" style="opacity:.8">Locked</em>'
        cards.append(f'<div class="si-medal {state}"><span aria-hidden="true">{item["icon"]}</span><b>{escape(item["name"])}</b>'
                     f'<small>{escape(item.get("rule", ""))}</small>{tag}</div>')
    html(f'<div class="si-grid">{"".join(cards)}</div>')


def wish_card(wish, days, cool_off):
    """Display wishlist status, estimated impact, and elapsed cool-off time."""
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
    """Render the sign-in page's visual introduction and brand message."""
    html(f"""<section class="si-brand">
<div class="si-poster"></div><video autoplay muted loop playsinline preload="metadata"><source src="{BRAND_VIDEO}" type="video/mp4"></video>
<div class="si-wordmark"><span>🌿 ShopImpact</span><small>CONSCIOUS SHOPPING JOURNAL</small></div>
<div>
<p class="si-eyebrow">Small choices · Thoughtful habits</p>
<h2>Small choices.<br><em>A clearer picture.</em></h2>
<p>Your shopping journal for thoughtful spending, everyday habits and a little perspective.</p>
<div class="si-feats"><span>📊 Monthly dashboard</span><span>☁️ CO₂e estimates</span><span>⏸️ Mindful wishlist</span><span>🏆 Eco levels & badges</span></div>
</div>
</section>""")
