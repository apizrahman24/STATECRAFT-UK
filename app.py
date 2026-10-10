import pandas as pd
import streamlit as st
from engine.game import create_uk_game, advance_turn, apply_policy, POLICIES, DEVOLVED_ACTIONS, apply_devolved_action
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
.sc-hero { padding: 1.5rem 2rem; border: 1px solid rgba(214,179,106,0.2); border-radius: 12px; background: rgba(15,23,42,0.9); margin-bottom: 1rem; }
.sc-card { background: rgba(15, 23, 42, 0.75); border: 1px solid #1e293b; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }
.sc-value { font-size: 1.4rem; font-weight: 800; color: #f1f5f9; }
.sc-alert { border-left: 4px solid #ef4444; background: rgba(239,68,68,0.12); padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; }
.sc-ticker { background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8; border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 1.2rem; display: flex; align-items: center; font-size: 0.85rem; }
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

# Live Downing Street Breaking News Ticker
latest_event = state["events"][-1] if state["events"] else {"title": "Number 10 Briefing", "description": "Government settles into executive command."}
st.markdown(f"""
<div class="sc-ticker">
    <div style="color: #38bdf8; font-weight: 800; margin-right: 0.8rem; text-transform: uppercase; font-size: 0.75rem; border-right: 1px solid #334155; padding-right: 0.8rem;">🚨 Breaking News</div>
    <div style="color: #cbd5e1;"><b>{latest_event['title']}:</b> {latest_event['description']}</div>
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
            
            with st.container(border=True):
                st.markdown(f"**Option {idx+1}: {choice['label']}**")
                st.caption(elaboration)
                st.markdown(f"🟢 **Pros:** {pros}")
                st.markdown(f"🔴 **Cons:** {cons}")
                
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

st.divider()

# Direct Cabinet Action (Collapsible & Moved Above Tabs)
with st.expander("🎯 Direct Cabinet Action (Executive Directives)", expanded=True):
    st.caption("Select and execute executive directives to manage national metrics.")

    if "active_policies" not in state:
        state["active_policies"] = set()

    pol_items = list(POLICIES.items())
    p_cols = st.columns(len(pol_items))

    for idx, (p_name, p_data) in enumerate(pol_items):
        with p_cols[idx]:
            is_active = p_name in state["active_policies"]
            
            border_color = "#22c55e" if is_active else "#1e293b"
            bg_color = "rgba(34, 197, 94, 0.12)" if is_active else "rgba(15, 23, 42, 0.75)"
            status_badge = "<div style='color: #22c55e; font-weight: 800; font-size: 0.72rem; margin-bottom: 0.3rem;'>✅ ACTIVE DIRECTIVE</div>" if is_active else "<div style='height: 1rem;'></div>"
            
            elaboration = p_data.get("elaboration", p_data.get("description", ""))
            pros = p_data.get("pros", "Improves policy metrics.").replace("**", "")
            cons = p_data.get("cons", "Carries metric tradeoffs.").replace("**", "")
            
            st.markdown(f"""
            <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 10px; padding: 0.85rem; min-height: 380px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 0.5rem;">
                <div>
                    {status_badge}
                    <div style="font-weight: 800; font-size: 0.95rem; color: #38bdf8; margin-bottom: 0.4rem; line-height: 1.2;">{p_name}</div>
                    <div style="font-size: 0.78rem; color: #cbd5e1; margin-bottom: 0.6rem; line-height: 1.3;">{elaboration}</div>
                    <div style="font-size: 0.74rem; color: #f1f5f9; margin-bottom: 0.4rem; line-height: 1.3;">🟢 <b>Pros:</b> {pros}</div>
                    <div style="font-size: 0.74rem; color: #f1f5f9; margin-bottom: 0.6rem; line-height: 1.3;">🔴 <b>Cons:</b> {cons}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_label = "✅ ACTIVE" if is_active else "⚡ ENACT"
            if st.button(btn_label, key=f"pol_btn_{idx}", use_container_width=True, type="secondary" if is_active else "primary"):
                if is_active:
                    state["active_policies"].remove(p_name)
                else:
                    state["active_policies"].add(p_name)
                    apply_policy(game, p_name)
                st.rerun()

st.divider()

# Tabs with Visual UIs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Executive Cabinet", "👥 Backbench Factions", "🗺️ Devolved Administrations", "📈 Economic Trends", "📰 Dispatch Archive"])

with tab1:
    st.subheader("Cabinet Ministers, Loyalty & Ambition")
    st.caption("Manage key government departments and ministerial loyalty to prevent public resignations.")
    
    cab_items = list(state["cabinet"].items())
    cab_cols = st.columns(len(cab_items))
    
    for idx, (role, data) in enumerate(cab_items):
        with cab_cols[idx]:
            loyalty_color = "🟢" if data['loyalty'] > 60 else "🔴"
            
            with st.container(border=True):
                st.markdown(f"**{role}**")
                st.caption(f"Minister: **{data['name']}**")
                st.markdown(f"{loyalty_color} **Loyalty:** {data['loyalty']}%")
                st.progress(max(0, min(100, data['loyalty'])) / 100)
                st.markdown(f"⚡ **Competence:** {data['competence']}%\n\n🔥 **Ambition:** {data['ambition']}%")

    st.divider()
    
    st.markdown("### 🔄 Execute Cabinet Reshuffle")
    res_col1, res_col2 = st.columns([2, 1])
    with res_col1:
        target_minister = st.selectbox("Select Minister to Reassign", list(state["cabinet"].keys()))
    with res_col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
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
    st.subheader("Devolved Administrations & Intergovernmental Relations")
    st.caption("Manage relations and unrest with Holyrood, the Senedd, and Stormont to prevent regional crises.")
    
    dev_items = list(state["devolved_nations"].items())
    d_cols = st.columns(len(dev_items))
    
    for idx, (nation, data) in enumerate(dev_items):
        with d_cols[idx]:
            with st.container(border=True):
                st.markdown(f"### 🗺️ {nation}")
                
                col1, col2 = st.columns(2)
                with col1:
                    rel_val = data['relations']
                    rel_color = "🟢 Stable" if rel_val > 60 else ("🟡 Strained" if rel_val > 40 else "🔴 Hostile")
                    st.metric("Relations", f"{rel_val}/100", delta=rel_color)
                    st.progress(max(0, min(100, rel_val)) / 100)
                with col2:
                    unrest_val = data['unrest']
                    unrest_color = "🟢 Calm" if unrest_val < 30 else ("🟡 Restless" if unrest_val < 60 else "🔴 Critical")
                    st.metric("Unrest", f"{unrest_val}%", delta=unrest_color, delta_color="inverse")
                    st.progress(max(0, min(100, unrest_val)) / 100)
                
                st.markdown("---")
                st.markdown("#### ⚡ Intergovernmental Actions")
                
                for a_idx, (act_name, act_data) in enumerate(DEVOLVED_ACTIONS.items()):
                    st.caption(f"**{act_name}** • Cost: £{act_data['cost_headroom']}bn")
                    if st.button(f"Execute", key=f"dev_{idx}_{a_idx}", use_container_width=True):
                        success = apply_devolved_action(game, nation, act_name)
                        if success:
                            st.success(f"Executed for {nation}.")
                            st.rerun()
                        else:
                            st.error("Insufficient Fiscal Headroom!")
                    st.write("")

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
