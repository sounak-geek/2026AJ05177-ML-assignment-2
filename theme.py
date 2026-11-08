"""Look & feel for the Streamlit app: blue / peacock / teal / cyan / green palette."""
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap

NAVY = "#0A1F44"
BLUE = "#1456C8"
PEACOCK = "#0B7A99"
TEAL = "#0FB5AE"
CYAN = "#22E4DD"
GREEN = "#2BD99F"

# white -> cyan -> teal -> peacock -> blue -> navy, used for the confusion matrix
HEATMAP_CMAP = LinearSegmentedColormap.from_list(
    "peacock", ["#F4FAFC", CYAN, TEAL, PEACOCK, BLUE, NAVY]
)

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {{
  --navy:{NAVY}; --blue:{BLUE}; --peacock:{PEACOCK};
  --teal:{TEAL}; --cyan:{CYAN}; --green:{GREEN};
}}

html, body, .stApp, [data-testid="stMarkdownContainer"], button, input {{
  font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
}}
.stApp {{
  background:
    radial-gradient(1100px 480px at 88% -8%, rgba(34,228,221,.20), transparent 60%),
    radial-gradient(900px 520px at -8% 12%, rgba(20,86,200,.10), transparent 60%),
    radial-gradient(700px 400px at 50% 110%, rgba(43,217,159,.12), transparent 60%),
    #F4FAFC;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.6rem; max-width: 1180px; }}

/* ---------- hero ---------- */
.hero {{
  position: relative; overflow: hidden; border-radius: 22px;
  padding: 2.8rem 3rem; margin-bottom: 1.8rem; color: #fff;
  background: linear-gradient(120deg, var(--navy) 0%, #0B3C8C 48%, var(--peacock) 100%);
  box-shadow: 0 24px 48px -22px rgba(10,31,68,.65);
}}
.hero::before {{                       /* the diagonal wedge */
  content: ""; position: absolute; top: 0; right: 0; bottom: 0; width: 50%;
  background: linear-gradient(135deg, var(--cyan) 0%, var(--teal) 42%, var(--blue) 100%);
  clip-path: polygon(34% 0, 100% 0, 100% 100%, 0 100%);
}}
.hero::after {{                        /* soft green glow */
  content: ""; position: absolute; width: 340px; height: 340px; right: -90px; bottom: -170px;
  background: radial-gradient(circle, rgba(43,217,159,.55), transparent 65%);
}}
.hero > * {{ position: relative; z-index: 1; max-width: 58%; }}
.hero .eyebrow {{
  display: inline-block; padding: .28rem .85rem; border-radius: 999px;
  font-size: .72rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
  background: rgba(34,228,221,.16); border: 1px solid rgba(34,228,221,.55); color: var(--cyan);
}}
.hero .hero-title {{
  font-size: 2.55rem; line-height: 1.12; font-weight: 800; margin: .9rem 0 .6rem;
  letter-spacing: -.02em;
}}
.hero .hero-title span {{
  background: linear-gradient(90deg, var(--cyan), var(--green));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}}
.hero p {{ font-size: 1rem; line-height: 1.6; color: rgba(255,255,255,.86); margin: 0 0 1.2rem; }}
.hero .chips {{ display: flex; flex-wrap: wrap; gap: .5rem; }}
.hero .chip {{
  padding: .32rem .8rem; border-radius: 10px; font-size: .8rem; font-weight: 600;
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
}}
@media (max-width: 800px) {{
  .hero {{ padding: 2rem 1.4rem; }}
  .hero > * {{ max-width: 100%; }}
  .hero::before {{ width: 100%; opacity: .25; }}
  .hero .hero-title {{ font-size: 1.8rem; }}
}}

/* ---------- headings ---------- */
.stApp h2, .stApp h3 {{ color: var(--navy); font-weight: 700; letter-spacing: -.01em; }}
.stApp h3::after {{
  content: ""; display: block; width: 48px; height: 4px; border-radius: 4px; margin-top: 6px;
  background: linear-gradient(90deg, var(--cyan), var(--blue));
}}

/* ---------- uploader ---------- */
[data-testid="stFileUploader"] section {{
  border: 2px dashed var(--teal); border-radius: 18px;
  background: linear-gradient(135deg, rgba(34,228,221,.10), rgba(20,86,200,.06));
}}
[data-testid="stFileUploader"] button, .stButton > button {{
  border: 0; border-radius: 12px; color: #fff; font-weight: 600;
  background: linear-gradient(90deg, var(--teal), var(--blue));
  box-shadow: 0 8px 18px -8px rgba(20,86,200,.7);
}}
[data-testid="stFileUploader"] button:hover {{ filter: brightness(1.08); color: #fff; }}

/* ---------- select box ---------- */
[data-baseweb="select"] > div {{
  border-radius: 14px; border: 1.5px solid rgba(11,122,153,.35); background: #fff;
  box-shadow: 0 6px 16px -10px rgba(10,31,68,.4);
}}
[data-baseweb="select"] > div:focus-within {{ border-color: var(--teal); }}

/* ---------- metric cards ---------- */
[data-testid="stMetric"] {{
  position: relative; overflow: hidden; background: #fff; border-radius: 18px;
  padding: 1.1rem .5rem 1rem; border: 1px solid rgba(11,122,153,.14);
  box-shadow: 0 16px 30px -20px rgba(10,31,68,.55);
  transition: transform .18s ease, box-shadow .18s ease;
}}
[data-testid="stMetric"]:hover {{ transform: translateY(-3px); box-shadow: 0 22px 36px -18px rgba(11,122,153,.55); }}
[data-testid="stMetric"]::before {{
  content: ""; position: absolute; left: 0; top: 0; right: 0; height: 5px;
  background: linear-gradient(90deg, var(--cyan), var(--teal), var(--blue));
}}
[data-testid="stMetricLabel"] p {{
  font-size: .78rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--peacock);
}}
[data-testid="stMetricValue"] div {{
  overflow: visible; text-overflow: clip; white-space: nowrap;
  font-size: 1.45rem; font-weight: 800; background: linear-gradient(90deg, var(--blue), var(--teal));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}}

/* ---------- tables, alerts ---------- */
[data-testid="stDataFrame"] {{
  border-radius: 16px; overflow: hidden; border: 1px solid rgba(11,122,153,.16);
  box-shadow: 0 14px 28px -22px rgba(10,31,68,.6);
}}
[data-testid="stAlert"] {{ border-radius: 16px; border: 1px solid rgba(15,181,174,.4); background: rgba(34,228,221,.10); }}
[data-testid="stImage"] img, [data-testid="stImageContainer"] img {{ border-radius: 16px; }}

.app-footer {{ margin-top: 2.5rem; text-align: center; font-size: .8rem; color: var(--peacock); opacity: .85; }}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title_plain: str, title_accent: str, subtitle: str, chips: list[str]) -> None:
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    st.markdown(
        f"""
        <div class="hero">
          <span class="eyebrow">Machine Learning &middot; Assignment 2</span>
          <div class="hero-title">{title_plain} <span>{title_accent}</span></div>
          <p>{subtitle}</p>
          <div class="chips">{chip_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown('<div class="app-footer">Pre-trained scikit-learn models &middot; nothing is retrained on upload</div>',
                unsafe_allow_html=True)
