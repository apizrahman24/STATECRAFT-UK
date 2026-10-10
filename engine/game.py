import copy
from engine.events import trigger_era_event

POLICIES = {
    "Austerity & Spending Cuts": {
        "description": "Reduce public sector spending to lower national debt, at the cost of public services and NHS capacity.",
        "effects": {"debt": -4.0, "public_support": -5.0, "nhs_backlog": 5.0, "government_stability": -2.0}
    },
    "NHS Emergency Funding": {
        "description": "Inject targeted funding into hospitals to cut waiting lists.",
        "effects": {"nhs_backlog": -6.0, "public_support": 5.0, "debt": 3.0}
    },
    "Green Energy Infrastructure": {
        "description": "Subsidize renewable energy grid projects to boost long-term productivity.",
        "effects": {"gdp": 3.0, "unemployment": -1.0, "debt": 3.0, "inflation": 0.5}
    },
    "Bank of England Rate Pressure": {
        "description": "Signal tighter monetary discipline to restrain persistent inflation.",
        "effects": {"inflation": -2.0, "growth": -1.0, "public_support": -2.0}
    }
}

def create_uk_game(pm_name, ruling_party):
    return {
        "country_name": "United Kingdom",
        "leader": pm_name,
        "ruling_party": ruling_party,
        "era": "Modern Era (UK Post-Election)",
        "state": {
            "turn": 1,
            "year": 2026,
            "month": 7,
            "majority_seats": 348,
            "metrics": {
                "gdp": 100.0,
                "growth": 1.2,
                "inflation": 3.8,
                "unemployment": 4.2,
                "debt": 98.0,
                "government_stability": 70.0,
                "public_support": 52.0,
                "legitimacy": 65.0,
                "nhs_backlog": 65.0,
                "diplomacy": 60.0,
                "military_readiness": 55.0,
                "international_tension": 30.0
            },
            "events": [
                {
                    "year": 2026,
                    "title": "General Election Victory",
                    "description": f"{pm_name} leads the {ruling_party} into 10 Downing Street following a major electoral breakthrough."
                }
            ],
            "history": [],
            "active_dilemma": {
                "title": "The Treasury Autumn Fiscal Statement",
                "description": "The Chancellor warns that public sector pay demands and NHS backlogs have created a multi-billion pound shortfall in the upcoming budget.",
                "choices": [
                    {
                        "label": "Increase Wealth and Corporate Levies",
                        "effects": {"metrics.debt": -3.0, "metrics.public_support": 3.0, "metrics.growth": -1.0}
                    },
                    {
                        "label": "Enforce Strict Departmental Spending Freezes",
                        "effects": {"metrics.debt": -4.0, "metrics.public_support": -6.0, "metrics.nhs_backlog": 4.0}
                    },
                    {
                        "label": "Borrow to Finance Public Infrastructure Growth",
                        "effects": {"metrics.debt": 5.0, "metrics.inflation": 1.2, "metrics.gdp": 2.0}
                    }
                ]
            }
        }
    }

def advance_turn(game):
    state = game["state"]
    metrics = state["metrics"]
    
    metrics["growth"] = round(max(-5.0, min(8.0, metrics["growth"] + (metrics["government_stability"] - 50) * 0.01)), 2)
    state["turn"] += 1
    
    trigger_era_event(state, game)

def apply_policy(game, policy_name):
    policy = POLICIES.get(policy_name)
    if not policy:
        return
    
    metrics = game["state"]["metrics"]
    for key, delta in policy["effects"].items():
        if key in metrics:
            metrics[key] += delta
            
    game["state"]["events"].append({
        "year": game["state"]["year"],
        "title": f"Cabinet Directive: {policy_name}",
        "description": policy["description"]
    })
