import pandas as pd
import streamlit as st
from engine.game import create_uk_game, advance_turn, apply_policy, POLICIES
from engine.events import resolve_dilemma

st.set_page_config(
    page_title="STATECRAFT: Westminster Executive",
    page_icon="🇬🇧",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Inter:wght@400;500;600;700&display=swap');
.stApp { background: linear-gradient(180deg, #070a0f 0%, #0c121d 100%); font-family: 'Inter', sans-serif; color: #f1f5f9; }
[data-testid="stSidebar"] { background: #05070a; border-right: 1px solid #1e293b; }
.sc-hero { padding: 1.5rem 2rem; border: 1px solid rgba(214,179,106,0.2); border-radius: 12px; background: rgba(15,23,42,0.9); margin-bottom: 1.2rem; }
.sc-card { background: rgba(15, 23, 42, 0.75); border: 1px solid #1e293b; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }
.sc-value { font-size: 1.4rem; font-weight: 800; color: #f1f5f9; }
.sc-alert { border-left: 4px solid #ef4444; background: rgba(239,68,68,0.12); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

if "game" not in st.session_state:
    st.session_state.game = None

if st.session_state.game is None:
    st.title("🇬🇧 STATECRAFT: Westminster Executive")
    st.subheader("Win the election, form your government, and steer the United Kingdom.")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        pm_name = st.text_input("Prime Minister Name", "Andy Burnham")
        party = st.selectbox("Ruling Party / Political Alignment", [
            "Labour Party",
            "Conservative Party",
            "Liberal Democrats",
            "Reform UK",
            "Green Party"
        ])
    with col2:
        st.markdown("### 🏛️ Government Mandate")
        if party == "Labour Party":
        # Based on 2024 UK general election composition
            st.caption("Center-Left • Large Parliamentary Majority (348 seats) • Focus on Public Services & Growth")
        elif party == "Conservative Party":
            st.caption("Centre-Right • Opposition / Reduced Seats (121 seats) • Focus on Tax Cuts & Free Enterprise")
        elif party == "Liberal Democrats":
            st.caption("Centrist / Social Liberal • Third Party (72 seats) • Focus on Electoral Reform & Public Investment")
        elif party == "Reform UK":
            st.caption("Right-Wing Populist • Insurgent Force (5 seats) • Focus on Border Control & State Sovereignty")
        else:
            st.caption("Eco-Socialist / Left-Wing • Progressive Bloc (4 seats) • Focus on Green Transition & Wealth Redistribution")

    if st.button("🏛️ ENTER 10 DOWNING STREET", type="primary", use_container_width=True):
        st.session_state.game = create_uk_game(pm_name, party)
        st.rerun()
    st.stop()

game = st.session_state.game
state = game["state"]
metrics = state["metrics"]

# Sidebar
with st.sidebar:
    st.markdown("### 🏛️ 10 Downing Street")
    st.write(f"**PM:** {game['leader']}")
    st.write(f"**Party:** {game['ruling_party']}")
    st.write(f"**Majority Seats:** {state['majority_seats']}")
    st.caption(f"📅 Month {state['month']}, Year {state['year']}")
    st.divider()
    if st.button("🔄 Reset Campaign", use_container_width=True):
        st.session_state.game = None
        st.rerun()

# Main Header
st.markdown(f"""
<div class="sc-hero">
    <div style="color: #e2b764; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Turn {state['turn']} • Strategic Command</div>
    <div style="font-family: 'Cinzel', serif; font-size: 2rem; font-weight: 900;">United Kingdom Government ({game['ruling_party']})</div>
</div>
""", unsafe_allow_html=True)

# Dilemma Prompt
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert">
        <div style="font-weight: 800; font-size: 1.05rem; color: #f87171;">🚨 CABINET CRISIS: {active_dilemma["title"]}</div>
        <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 0.3rem;">{active_dilemma["description"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(active_dilemma["choices"]))
    for idx, (col, choice) in enumerate(zip(cols, active_dilemma["choices"])):
        with col:
            if st.button(f"👉 {choice['label']}", key=f"d_btn_{idx}", use_container_width=True):
                resolve_dilemma(state, idx)
                st.rerun()
    st.divider()

# Metrics Grid
snapshot = [
    ("GDP Growth", f"{metrics['growth']:.1f}%"),
    ("Inflation (CPI)", f"{metrics['inflation']:.1f}%"),
    ("Fiscal Headroom", f"£{metrics['fiscal_headroom']:.1f}bn"),
    ("National Debt", f"{metrics['debt']:.1f}%"),
    ("Government Stability", f"{metrics['stability'] if 'stability' in metrics else metrics['government_stability']:.1f}"),
    ("Public Approval", f"{metrics['public_support']:.1f}%"),
    ("NHS Backlog Index", f"{metrics['nhs_backlog']:.1f}"),
    ("Foreign Direct Investment", f"£{metrics['fdi']}bn")
]

m_cols = st.columns(4)
for i, (label, val) in enumerate(snapshot):
    with m_cols[i % 4]:
        st.markdown(f"""
        <div class="sc-card">
            <div style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase; font-weight: 700;">{label}</div>
            <div class="sc-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🏛️ Executive Cabinet", "🗺️ Devolved Administrations", "📰 Dispatch Archive"])

with tab1:
    st.subheader("Cabinet Ministers & Loyalty")
    cab_df = pd.DataFrame(state["cabinet"]).T
    st.dataframe(cab_df, use_container_width=True)

with tab2:
    st.subheader("Devolved Nations & Relations")
    dev_df = pd.DataFrame(state["devolved_nations"]).T
    st.dataframe(dev_df, use_container_width=True)

with tab3:
    st.subheader("Historical Dispatch Log")
    for ev in reversed(state["events"][-6:]):
        st.markdown(f"**[{ev['year']}] {ev['title']}**")
        st.caption(ev["description"])
        st.divider()

# Policy Deck & Turn Advancement
st.subheader("🎯 Direct Cabinet Action")
p_col1, p_col2 = st.columns([3, 1])
with p_col1:
    selected_pol = st.selectbox("Select Directive", list(POLICIES.keys()), label_visibility="collapsed")
with p_col2:
    if st.button("⚡ ENACT POLICY", type="primary", use_container_width=True):
        apply_policy(game, selected_pol)
        st.rerun()

st.divider()

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
