import streamlit as st
from engine.game import create_uk_game, advance_turn, apply_policy, POLICIES
from engine.events import resolve_dilemma

# ==========================================================
# CONFIG & THEME
# ==========================================================

st.set_page_config(
    page_title="STATECRAFT: 10 Downing Street",
    page_icon="🇬🇧",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(214,179,106,.07), transparent 35%),
        linear-gradient(180deg, #070a0f 0%, #0c121d 100%);
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: #05070a;
    border-right: 1px solid #1e293b;
}
.sc-hero {
    padding: 1.8rem 2rem;
    border: 1px solid rgba(214,179,106,0.2);
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(20,27,45,0.85));
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.sc-kicker {
    color: #e2b764;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    font-weight: 700;
}
.sc-title { 
    font-family: 'Cinzel', serif !important;
    font-size: 2.2rem; 
    font-weight: 900; 
    color: #f8fafc; 
}
.sc-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.6rem;
}
.sc-value { font-size: 1.45rem; font-weight: 800; color: #f1f5f9; }
.sc-caption { color: #64748b; font-size: 0.75rem; }
.sc-alert {
    border-left: 4px solid #ef4444;
    background: linear-gradient(90deg, rgba(239,68,68,0.12), rgba(15,23,42,0.9));
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION INIT
# ==========================================================

if "game" not in st.session_state:
    st.session_state.game = None

if st.session_state.game is None:
    st.title("🇬🇧 STATECRAFT: 10 Downing Street")
    st.subheader("The Election is over. You have entered Number 10.")
    st.markdown("""
    The red boxes are stacked on your desk. Public services are stretched, 
    inflation is persistent, and the country expects immediate action.
    """)
    st.divider()

    pm_name = st.text_input("Prime Minister Name", "Andy Burnham")
    party_name = st.selectbox("Ruling Party", ["Labour Party"])
    
    if st.button("🏛️ TAKE OFFICE AT NUMBER 10", type="primary", use_container_width=True):
        st.session_state.game = create_uk_game(pm_name, party_name)
        st.rerun()
    st.stop()


# ==========================================================
# ACTIVE GAME STATE
# ==========================================================

game = st.session_state.game
state = game["state"]
metrics = state["metrics"]


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown("### 🇬🇧 Downing Street HQ")
    st.markdown(f"**PM:** {game['leader']}")
    st.markdown(f"**Party:** {game['ruling_party']}")
    st.markdown(f"**Majority:** {state['majority_seats']} seats")
    st.caption(f"📅 Month {state['month']}, Year {state['year']} (Turn {state['turn']})")
    
    st.divider()
    if st.button("🔄 Call Snap Election / Restart", use_container_width=True):
        st.session_state.game = None
        st.rerun()


# ==========================================================
# MAIN DASHBOARD
# ==========================================================

st.markdown(f"""
<div class="sc-hero">
    <div class="sc-kicker">Executive Command • Month {state["month"]}, Year {state["year"]}</div>
    <div class="sc-title">🇬🇧 {game["country_name"]}</div>
    <div class="sc-subtitle">Prime Minister {game['leader']} &nbsp;•&nbsp; {game['ruling_party']} Administration</div>
</div>
""", unsafe_allow_html=True)

# 1. Dilemma Banner
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert">
        <div style="font-weight: 800; font-size: 1.05rem; color: #f87171;">🚨 IMMEDIATE CABINET CRISIS: {active_dilemma["title"]}</div>
        <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 0.3rem;">{active_dilemma["description"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Executive Cabinet Response:")
    cols = st.columns(len(active_dilemma["choices"]))
    for idx, (col, choice) in enumerate(zip(cols, active_dilemma["choices"])):
        with col:
            if st.button(f"👉 {choice['label']}", key=f"dil_{idx}", use_container_width=True):
                resolve_dilemma(state, idx)
                st.rerun()
    st.divider()

# 2. Key Metrics Grid
snapshot = [
    ("GDP Growth", f"{metrics['growth']:.1f}%", "Annualized Rate"),
    ("Inflation (CPI)", f"{metrics['inflation']:.1f}%", "Target: 2.0%"),
    ("Unemployment", f"{metrics['unemployment']:.1f}%", "Labor Force"),
    ("National Debt / GDP", f"{metrics['debt']:.1f}%", "Public Deficit"),
    ("Government Stability", f"{metrics['government_stability']:.1f}", "Cabinet Support"),
    ("Public Approval", f"{metrics['public_support']:.1f}%", "Opinion Polls"),
    ("NHS Pressure", f"{metrics.get('nhs_backlog', 50):.1f}", "Waiting List Index"),
    ("International Tension", f"{metrics['international_tension']:.1f}", "Global Security"),
]

m_cols = st.columns(4)
for i, (label, value, caption) in enumerate(snapshot):
    with m_cols[i % 4]:
        st.markdown(f"""
        <div class="sc-card">
            <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">{label}</div>
            <div class="sc-value">{value}</div>
            <div class="sc-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

# 3. Policy Execution
st.subheader("🎯 Direct Cabinet Action")
act_col1, act_col2 = st.columns([3, 1])
with act_col1:
    policy_name = st.selectbox("Choose Cabinet Directive", list(POLICIES.keys()), label_visibility="collapsed")
with act_col2:
    if st.button("⚡ ENACT DIRECTIVE", type="primary", use_container_width=True):
        apply_policy(game, policy_name)
        st.rerun()

st.divider()

# 4. Turn Advancement
if state.get("active_dilemma") is not None:
    st.warning("⚠️ You must resolve the active cabinet crisis above before advancing the month!")
else:
    if st.button("⏩ ADVANCE MONTH", type="primary", use_container_width=True):
        state["month"] += 1
        if state["month"] > 12:
            state["month"] = 1
            state["year"] += 1
        advance_turn(game)
        st.rerun()

# 5. News Feed
st.subheader("📰 Downing Street Dispatch")
for ev in reversed(state["events"][-5:]):
    st.write(f"**[{ev['year']} / Month {state['month']}] {ev['title']}**")
    st.caption(ev["description"])
