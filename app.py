import io
import random
from math import sin, cos, pi

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, Polygon

# ---------- Page setup ----------
st.set_page_config(page_title="bubu & dud proposal", page_icon="💍", layout="centered")

# ---------- Session state ----------
if "accepted" not in st.session_state:
    st.session_state.accepted = False
if "round" not in st.session_state:
    st.session_state.round = 1
if "shuffle_seed" not in st.session_state:
    st.session_state.shuffle_seed = random.randint(0, 10_000)
if "playful_line" not in st.session_state:
    st.session_state.playful_line = "Choose wisely 😊"

PLAYFUL_LINES = [
    "Think again 😜",
    "Are you suuure? 🤭",
    "Hehe… try again 💞",
    "bubu & dud whisper… say YES! 🐻💗🐻",
    "Destiny says yes ✨",
    "Nice try 😏",
]

# ---------- Cute drawing (bubu & dud) ----------
def draw_heart(ax, cx, cy, size, color="#FFC0CB"):
    pts = []
    for t in [i * pi / 100 for i in range(201)]:  # 0..π*2-ish shape; dense for smoothness
        x = 16 * (sin(t) ** 3)
        y = 13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
        pts.append((cx + x * size / 20, cy - y * size / 20))
    heart = Polygon(pts, closed=True, fc=color, ec="none")
    ax.add_patch(heart)

def draw_bear(ax, x, y, scale=1.0, face="#FDEBD0", ear_in="#F7D9B8", line="#6B3F21", blush="#F9AFAF"):
    r = 0.60 * scale
    ear = 0.26 * scale

    # Ears
    ax.add_patch(Circle((x - r*0.85, y + r*0.90), ear, fc=face, ec=line, lw=2))
    ax.add_patch(Circle((x + r*0.85, y + r*0.90), ear, fc=face, ec=line, lw=2))
    ax.add_patch(Circle((x - r*0.85, y + r*0.90), ear*0.7, fc=ear_in, ec="none"))
    ax.add_patch(Circle((x + r*0.85, y + r*0.90), ear*0.7, fc=ear_in, ec="none"))

    # Face
    ax.add_patch(Circle((x, y), r, fc=face, ec=line, lw=2))

    # Eyes
    eye_dx = 0.18 * scale
    eye_r = 0.06 * scale
    ax.add_patch(Circle((x - eye_dx, y + 0.06 * scale), eye_r, fc="#2F2F2F", ec="none"))
    ax.add_patch(Circle((x + eye_dx, y + 0.06 * scale), eye_r, fc="#2F2F2F", ec="none"))

    # Nose
    ax.add_patch(Circle((x, y - 0.02 * scale), 0.08 * scale, fc="#613A1F", ec="none"))

    # Mouth (two small arcs)
    ax.add_patch(Arc((x - 0.04 * scale, y - 0.12 * scale), 0.18 * scale, 0.16 * scale, theta1=270, theta2=360, ec="#613A1F", lw=2))
    ax.add_patch(Arc((x + 0.04 * scale, y - 0.12 * scale), 0.18 * scale, 0.16 * scale, theta1=180, theta2=270, ec="#613A1F", lw=2))

    # Blush
    ax.add_patch(Circle((x - 0.32 * scale, y - 0.04 * scale), 0.11 * scale, fc=blush, ec="none"))
    ax.add_patch(Circle((x + 0.32 * scale, y - 0.04 * scale), 0.11 * scale, fc=blush, ec="none"))

    # Tiny paws
    ax.add_patch(Circle((x - 0.48 * scale, y - 0.42 * scale), 0.10 * scale, fc=face, ec=line, lw=2))
    ax.add_patch(Circle((x + 0.48 * scale, y - 0.42 * scale), 0.10 * scale, fc=face, ec=line, lw=2))

def render_cute_header():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.axis("off")

    # Background heart + duo
    draw_heart(ax, 0, 1.1, size=4.5)
    draw_bear(ax, -1.2, 1.2, scale=1.6, face="#FDEBD0")   # bubu
    draw_bear(ax,  1.2, 1.2, scale=1.6, face="#EAF2F8")   # dud

    # Titles
    ax.text(0, 2.6, "bubu & dud", ha="center", va="center", fontsize=24, weight="bold", family="DejaVu Sans")
    ax.text(0, 0.35, "Will you be mine?", ha="center", va="center", fontsize=22, weight="bold", family="DejaVu Sans")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    st.image(buf, use_column_width=True)

# ---------- UI ----------
def yes_screen():
    st.markdown("<h2 style='text-align:center'>She said YES! 💖</h2>", unsafe_allow_html=True)
    st.caption("bubu & dud are doing a happy dance!")
    st.balloons()

    # simple floating hearts line
    hearts = " ".join(["💗", "💖", "💞", "💘", "💕", "💓"])
    st.markdown(f"<div style='text-align:center;font-size:32px'>{hearts}</div>", unsafe_allow_html=True)

def prompt_screen():
    render_cute_header()
    st.write(f"**Round {st.session_state.round}** — {st.session_state.playful_line}")

    # Shuffle the layout each render so the 'Think again' button 'runs away'
    random.seed(st.session_state.shuffle_seed + st.session_state.round)
    slots = list(range(3))
    random.shuffle(slots)

    colA, colB, colC = st.columns(3)

    # Decide where each button goes this round
    yes_slot = slots[0]
    think_slot = slots[1]

    cols = [colA, colB, colC]

    with cols[yes_slot]:
        yes = st.button("Yes 💘", use_container_width=True, type="primary", key=f"yes-{st.session_state.round}")

    with cols[think_slot]:
        think = st.button("Think again 🤔", use_container_width=True, key=f"think-{st.session_state.round}")

    # Footer
    st.markdown("<div style='text-align:center;opacity:0.75'>(bubu & dud are rooting for YES!)</div>",
                unsafe_allow_html=True)

    # Button logic
    if yes:
        st.session_state.accepted = True
    elif think:
        st.session_state.round += 1
        st.session_state.playful_line = random.choice(PLAYFUL_LINES)
        st.experimental_rerun()  # redraw with new layout to "dodge"

# ---------- App flow ----------
st.title("💍 The Proposal")

if st.session_state.accepted:
    yes_screen()
else:
    prompt_screen()
