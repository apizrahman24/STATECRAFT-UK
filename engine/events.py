import random

COMPLEX_UK_DILEMMAS = [
    {
        "id": "uk_dil_nhs_strike",
        "title": "National Health Service General Strike Coordination",
        "description": "Consultants, junior doctors, and nursing syndicates have rejected the latest pay offer and announced a synchronized 72-hour all-out hospital strike.",
        "choices": [
            {
                "label": " capitulate to Union Demands: Fully fund pay parity demands",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Invoke Emergency Service Legislation: Mandate minimum staffing levels",
                "effects": {"metrics.government_stability": -6.0, "metrics.nhs_backlog": 8.0, "metrics.public_support": -10.0, "cabinet.Health Secretary.loyalty": -12}
            }
        ]
    },
    {
        "id": "uk_dil_scots_indy",
        "title": "Holyrood Independence Referendum Demand",
        "description": "The First Minister of Scotland has formally requested Section 30 powers to hold a second independence referendum, citing divergence over economic policies.",
        "choices": [
            {
                "label": "Grant Section 30 Referendum Mandate: Uphold democratic self-determination",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood.relations)": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Refusal: Veto referendum outright",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood.unrest)": 30, "devolved_nations.Scotland (Holyrood.relations)": -25}
            }
        ]
    },
    {
        "id": "uk_dil_defense_procurement",
        "title": "Carrier Strike Group & Defense Procurement Scandal",
        "description": "A Parliamentary Public Accounts Committee report reveals severe budget overruns and equipment delays in the Ministry of Defence's next-generation frigate program.",
        "choices": [
            {
                "label": "Axe Underperforming Defense Contracts: Reallocate funds to NHS and housing",
                "effects": {"metrics.military_readiness": -10.0, "metrics.fiscal_headroom": 5.0, "cabinet.Foreign Secretary.loyalty": -15}
            },
            {
                "label": "Bail Out Defense Contractors: Protect strategic shipbuilding jobs and military readiness",
                "effects": {"metrics.military_readiness": 8.0, "metrics.debt": 4.0, "metrics.fiscal_headroom": -4.0}
            }
        ]
    }
]

CHAINED_UK_FOLLOW_UPS = {
    "uk_rebel_backbench": {
        "title": "Backbench MP Rebellion on the Finance Bill",
        "description": "Dozens of your own party MPs are threatening to vote down the Government's flagship finance bill over proposed tax and spending adjustments.",
        "choices": [
            {
                "label": "Compromise and Amend the Bill to Satisfy Rebels",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection and Whip Withdrawal",
                "effects": {"metrics.government_stability": -10.0, "metrics.public_support": -5.0}
            }
        ]
    }
}

def trigger_era_event(state, game):
    if not state.get("active_dilemma") and state.get("queued_dilemma"):
        follow_id = state.pop("queued_dilemma")
        if follow_id in CHAINED_UK_FOLLOW_UPS:
            state["active_dilemma"] = CHAINED_UK_FOLLOW_UPS[follow_id]
            return

    if not state.get("active_dilemma") and random.random() < 0.50:
        state["active_dilemma"] = random.choice(COMPLEX_UK_DILEMMAS)

    news_items = [
        ("Whitehall Intelligence Briefing", "MI5 reports heightened state-sponsored cyber probing against national critical infrastructure."),
        ("Bank of England Rate Notice", "Governor maintains benchmark interest rates amid sticky service-sector inflation readings."),
        ("Cross-Channel Migration Talks", "Home Office finalizes new intelligence-sharing framework with continental European partners.")
    ]
    title, desc = random.choice(news_items)
    state["events"].append({
        "year": state["year"],
        "title": title,
        "description": desc
    })

def resolve_dilemma(state, choice_idx):
    dilemma = state.get("active_dilemma")
    if not dilemma:
        return
    
    choice = dilemma["choices"][choice_idx]
    for path_str, delta in choice["effects"].items():
        parts = path_str.split(".")
        if len(parts) == 2 and parts[0] == "metrics":
            if parts[1] in state["metrics"]:
                state["metrics"][parts[1]] += delta
        elif len(parts) == 3 and parts[0] == "cabinet":
            cab_role, cab_attr = parts[1], parts[2]
            if cab_role in state["cabinet"] and cab_attr in state["cabinet"][cab_role]:
                state["cabinet"][cab_role][cab_attr] += delta
        elif len(parts) == 3 and parts[0] == "devolved_nations":
            nation, attr = parts[1], parts[2]
            if nation in state["devolved_nations"] and attr in state["devolved_nations"][nation]:
                state["devolved_nations"][nation][attr] += delta

    # Chance to trigger a follow-up backbench crisis
    if random.random() < 0.4:
        state["queued_dilemma"] = "uk_rebel_backbench"

    state["events"].append({
        "year": state["year"],
        "title": f"Cabinet Executive Order: {dilemma['title']}",
        "description": f"Executed Strategy: '{choice['label']}'."
    })
    state["active_dilemma"] = None
