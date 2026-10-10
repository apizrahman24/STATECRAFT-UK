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
.sc-alert { border-left: 4px solid #ef4444; background: rgba(239,68,68,0.12); padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; }
.sc-choice-box { background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

if "game" not in st.session_state:
    st.session_state.game = None

if st.session_state.game is None:
    st.title("🇬🇧 STATECRAFT: Westminster Executive")
    st.subheader("Win the election, manage factions, and survive Downing Street.")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        pm_name = st.text_input("Prime Minister Name", "Andy Burnham")
        party = st.selectbox("Ruling Party", ["Labour Party", "Conservative Party", "Liberal Democrats", "Reform UK", "Green Party"])
    with col2:
        st.markdown("### 🏛️ Mandate Preview")
        st.caption("Manage backbench MP factions, cabinet loyalty, media scrutiny, devolved administrations, and geostrategic crises.")

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
    st.write(f"**Working Majority:** {state['majority_seats']} seats")
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

# Dilemma Prompt with Visual Cards & Aligned Layout
active_dilemma = state.get("active_dilemma")
if active_dilemma:
    st.markdown(f"""
    <div class="sc-alert">
        <div style="font-weight: 800; font-size: 1.15rem; color: #f87171;">🚨 {active_dilemma["title"]}</div>
        <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 0.4rem; line-height: 1.4;">{active_dilemma["description"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚖️ Executive Options & Strategic Trade-offs")
    cols = st.columns(len(active_dilemma["choices"]))
    for idx, (col, choice) in enumerate(zip(cols, active_dilemma["choices"])):
        with col:
            elaboration = choice.get("elaboration", "Execute this directive to navigate current fiscal pressures.")
            pros = choice.get("pros", "Helps stabilize specific national metrics.")
            cons = choice.get("cons", "Carries hidden political or economic tradeoffs.")
            
            st.markdown(f"""
            <div class="sc-card" style="min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-weight: 700; font-size: 1rem; color: #38bdf8; margin-bottom: 0.4rem;">Option {idx+1}: {choice['label']}</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.6rem;">{elaboration}</div>
                    <div style="font-size: 0.82rem; margin-bottom: 0.3rem;">🟢 <b>Pros:</b> {pros}</div>
                    <div style="font-size: 0.82rem; margin-bottom: 0.6rem;">🔴 <b>Cons:</b> {cons}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"👉 Select Option {idx+1}", key=f"d_btn_{idx}", use_container_width=True):
                resolve_dilemma(state, idx)
                st.rerun()
    st.divider()

# Metrics Grid
snapshot = [
    ("GDP Growth", f"{metrics['growth']:.1f}%"),
    ("Inflation (CPI)", f"{metrics['inflation']:.1f}%"),
    ("Fiscal Headroom", f"£{metrics['fiscal_headroom']:.1f}bn"),
    ("National Debt", f"{metrics['debt']:.1f}%"),
    ("Government Stability", f"{metrics['government_stability']:.1f}"),
    ("Public Approval", f"{metrics['public_support']:.1f}%"),
    ("Media Sentiment", f"{metrics['media_sentiment']:.1f}/100"),
    ("NHS Backlog Index", f"{metrics['nhs_backlog']:.1f}")
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

# Tabs with Visual UIs (Cabinet Bars, Faction Happiness Meters, Trend Charts)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Executive Cabinet", "👥 Backbench Factions", "🗺️ Devolved Administrations", "📈 Economic Trends", "📰 Dispatch Archive"])

with tab1:
    st.subheader("Cabinet Ministers, Loyalty & Ambition")
    st.caption("Manage key government departments and ministerial loyalty to prevent public resignations.")
    
    for role, data in state["cabinet"].items():
        col_a, col_b, col_c = st.columns([2, 2, 3])
        with col_a:
            st.markdown(f"**{role}**")
            st.caption(f"Minister: {data['name']}")
        with col_b:
            loyalty_color = "🟢" if data['loyalty'] > 60 else "🔴"
            st.markdown(f"{loyalty_color} **Loyalty:** {data['loyalty']}%")
            st.progress(max(0, min(100, data['loyalty'])) / 100)
        with col_c:
            st.markdown(f"⚡ **Competence:** {data['competence']}% | 🔥 **Ambition:** {data['ambition']}%")
        st.divider()
    
    st.markdown("### 🔄 Execute Cabinet Reshuffle")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        target_minister = st.selectbox("Select Minister to Reassign", list(state["cabinet"].keys()))
    with res_col2:
        if st.button("⚖️ Realign Portfolio (+5 Loyalty, -5 Ambition)", use_container_width=True):
            state["cabinet"][target_minister]["loyalty"] = min(100, state["cabinet"][target_minister]["loyalty"] + 5)
            state["cabinet"][target_minister]["ambition"] = max(0, state["cabinet"][target_minister]["ambition"] - 5)
            st.success(f"Successfully restructured {target_minister}'s portfolio.")
            st.rerun()

with tab2:
    st.subheader("Ruling Party Factional Breakdown & Happiness")
    st.caption("Keep faction happiness above 45% to prevent coordinated backbench rebellions and leadership threats.")
    
    for faction_name, data in state["factions"].items():
        h_val = data['happiness']
        status_icon = "🟢 Secure" if h_val > 60 else ("🟡 Restless" if h_val > 45 else "🔴 Rebellious")
        
        st.markdown(f"**{faction_name}** ({data['size_MPs']} MPs) — *Key Demand: {data['key_demand']}*")
        f_col1, f_col2 = st.columns([4, 1])
        with f_col1:
            st.progress(max(0, min(100, h_val)) / 100)
        with f_col2:
            st.markdown(f"**{h_val:.0f}%** ({status_icon})")
        st.write("")

with tab3:
    st.subheader("Devolved Nations & Relations")
    for nation, data in state["devolved_nations"].items():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{nation}**")
            st.metric("Relations Score", f"{data['relations']}/100")
        with col2:
            st.metric("Unrest Index", f"{data['unrest']}%", delta_color="inverse")
        st.divider()

with tab4:
    st.subheader("National Economic & Stability Trends")
    if len(state["history"]) > 0:
        history_df = pd.DataFrame(state["history"])
        st.line_chart(history_df.set_index("year")[["gdp", "debt", "inflation", "stability"]])
    else:
        st.info("Advance past turn 1 to begin recording historical trend charts.")

with tab5:
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
