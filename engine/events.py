import random

UK_DILEMMAS = [
    {
        "id": "uk_dil_nhs_strike",
        "title": "Junior Doctors & Nurses Balloting for National Strike",
        "description": "Healthcare unions demand an immediate above-inflation pay settlement. Hospital wait times are spiraling, and health sector leaders warn winter pressures will break A&E departments unless terms are met.",
        "choices": [
            {
                "label": "Meet Full Union Demands: Fund immediate public sector pay increases",
                "effects": {"metrics.debt": 4.5, "metrics.nhs_backlog": -8.0, "metrics.public_support": 6.0}
            },
            {
                "label": "Hold the Pay Cap Line: Enforce strict Treasury budgetary restraint",
                "effects": {"metrics.debt": -2.0, "metrics.nhs_backlog": 7.0, "metrics.public_support": -8.0}
            }
        ]
    },
    {
        "id": "uk_dil_bond_market",
        "title": "Gilt Yield Spike & Bond Market Volatility",
        "description": "International bond investors are spooked by rising national debt projections, pushing UK government borrowing costs (gilt yields) sharply upward.",
        "choices": [
            {
                "label": "Announce Emergency Fiscal Consolidation & Spending Cuts",
                "effects": {"metrics.debt": -5.0, "metrics.growth": -1.5, "metrics.public_support": -7.0}
            },
            {
                "label": "Reassure Markets and Commit to Growth-First Borrowing",
                "effects": {"metrics.growth": 1.5, "metrics.debt": 4.0, "metrics.inflation": 1.0}
            }
        ]
    }
]

def trigger_era_event(state, game):
    if not state.get("active_dilemma") and random.random() < 0.45:
        state["active_dilemma"] = random.choice(UK_DILEMMAS)
    
    # Generic news ticker generation
    events_pool = [
        ("Treasury Forecast Update", "Office for Budget Responsibility releases revised mid-term growth figures."),
        ("Green Energy Grid Transition", "Private investment flows into offshore wind and grid interconnectors."),
        ("Transport Infrastructure", "Devolved regional mayors lobby Westminster for expanded mass-transit funding.")
    ]
    title, desc = random.choice(events_pool)
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
        if path_str.startswith("metrics."):
            metric_key = path_str.split(".")[1]
            if metric_key in state["metrics"]:
                state["metrics"][metric_key] += delta
                
    state["events"].append({
        "year": state["year"],
        "title": f"Cabinet Decision: {dilemma['title']}",
        "description": f"Enacted Strategy: '{choice['label']}'."
    })
    state["active_dilemma"] = None
