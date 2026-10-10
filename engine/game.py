import copy
from engine.events import trigger_era_event

POLICIES = {
    "Comprehensive Spending Review Cuts": {
        "description": "Enforce strict departmental spending freezes across Whitehall to preserve fiscal headroom, severely angering public sector unions.",
        "effects": {"debt": -6.0, "public_support": -7.0, "nhs_backlog": 5.0, "government_stability": -4.0}
    },
    "Emergency NHS Capital Injection": {
        "description": "Direct emergency funding into hospital waiting lists and social care capacity, financed via short-term borrowing.",
        "effects": {"nhs_backlog": -9.0, "public_support": 6.0, "debt": 4.5, "inflation": 0.5}
    },
    "Green Industrial Transition Subsidy": {
        "description": "Subsidize renewable grid infrastructure and green tech startups to stimulate long-term productivity and foreign direct investment.",
        "effects": {"gdp": 3.5, "fdi": 5.0, "unemployment": -1.2, "debt": 4.0}
    },
    "Bank of England Rate Defense": {
        "description": "Coordinate closely with Threadneedle Street to signal tighter monetary policy and suppress persistent energy-driven inflation.",
        "effects": {"inflation": -2.5, "growth": -1.2, "public_support": -3.0}
    },
    "Defense & Cyber Security Boost": {
        "description": "Raise defense expenditure to counter rising international tensions and forge joint cybersecurity agreements with European allies.",
        "effects": {"military_readiness": 8.0, "international_tension": -4.0, "debt": 4.0}
    }
}

def create_uk_game(pm_name, ruling_party):
    # Set party-specific baseline metrics & majorities based on 2024–2026 data
    if ruling_party == "Labour Party":
        seats = 348
        stability = 75.0
        approval = 54.0
        cabinet = {
            "Chancellor of the Exchequer": {"name": "Rachel Reeves", "loyalty": 75, "competence": 80},
            "Foreign Secretary": {"name": "David Lammy", "loyalty": 70, "competence": 72},
            "Health Secretary": {"name": "Wes Streeting", "loyalty": 65, "competence": 78},
            "Home Secretary": {"name": "Yvette Cooper", "loyalty": 78, "competence": 74}
        }
    elif ruling_party == "Conservative Party":
        seats = 121
        stability = 58.0
        approval = 42.0
        cabinet = {
            "Shadow Chancellor / Treasury": {"name": "Mel Stride", "loyalty": 70, "competence": 72},
            "Foreign Affairs": {"name": "Priti Patel", "loyalty": 65, "competence": 68},
            "Health": {"name": "Victoria Atkins", "loyalty": 68, "competence": 70},
            "Home Department": {"name": "James Cleverly", "loyalty": 72, "competence": 75}
        }
    elif ruling_party == "Liberal Democrats":
        seats = 72
        stability = 62.0
        approval = 46.0
        cabinet = {
            "Treasury Spokesperson": {"name": "Daisy Cooper", "loyalty": 80, "competence": 74},
            "Foreign Affairs": {"name": "Layla Moran", "loyalty": 75, "competence": 70},
            "Health Spokesperson": {"name": "Helen Morgan", "loyalty": 78, "competence": 72},
            "Home Spokesperson": {"name": "Alistair Carmichael", "loyalty": 70, "competence": 75}
        }
    elif ruling_party == "Reform UK":
        seats = 5
        stability = 50.0
        approval = 48.0
        cabinet = {
            "Chief Treasury Strategist": {"name": "Richard Tice", "loyalty": 85, "competence": 65},
            "Foreign Affairs Lead": {"name": "Nigel Farage", "loyalty": 90, "competence": 70},
            "Public Services Lead": {"name": "Rupert Lowe", "loyalty": 80, "competence": 60},
            "Security Lead": {"name": "Lee Anderson", "loyalty": 85, "competence": 55}
        }
    else: # Green Party
        seats = 4
        stability = 55.0
        approval = 45.0
        cabinet = {
            "Treasury & Climate Finance": {"name": "Carla Denyer", "loyalty": 85, "competence": 72},
            "Foreign & Global Justice": {"name": "Adrian Ramsay", "loyalty": 82, "competence": 70},
            "Public Services & NHS": {"name": "Zack Polanski", "loyalty": 80, "competence": 68},
            "Home & Communities": {"name": "Ellie Chowns", "loyalty": 82, "competence": 70}
        }

    return {
        "country_name": "United Kingdom",
        "leader": pm_name,
        "ruling_party": ruling_party,
        "era": "Modern Era (UK Westminster)",
        "state": {
            "turn": 1,
            "year": 2026,
            "month": 7,
            "majority_seats": seats,
            "metrics": {
                "gdp": 102.5,
                "growth": 1.3,
                "inflation": 3.2,
                "unemployment": 4.1,
                "debt": 98.5,
                "fiscal_headroom": 11.0,
                "government_stability": stability,
                "public_support": approval,
                "legitimacy": 68.0,
                "nhs_backlog": 62.0,
                "fdi": 25.0,
                "diplomacy": 65.0,
                "military_readiness": 58.0,
                "international_tension": 35.0
            },
            "cabinet": cabinet,
            "devolved_nations": {
                "Scotland (Holyrood)": {"relations": 55, "unrest": 25},
                "Wales (Senedd)": {"relations": 65, "unrest": 15},
                "Northern Ireland (Stormont)": {"relations": 45, "unrest": 40}
            },
            "events": [
                {
                    "year": 2026,
                    "title": "Government Formed",
                    "description": f"{pm_name} leads the {ruling_party} administration into Number 10 Downing Street."
                }
            ],
            "history": [],
            "active_dilemma": {
                "id": "uk_dil_autumn_budget",
                "title": "The Autumn Budget & Fiscal Headroom Crisis",
                "description": "The Office for Budget Responsibility (OBR) warns that public pay settlements and energy price volatility have squeezed fiscal headroom down to £7bn.",
                "choices": [
                    {
                        "label": "Introduce Targeted Wealth and Capital Gains Adjustments",
                        "effects": {"metrics.fiscal_headroom": 8.0, "metrics.debt": -3.0, "metrics.public_support": -8.0}
                    },
                    {
                        "label": "Implement Severe Whitehall Departmental Spending Freezes",
                        "effects": {"metrics.fiscal_headroom": 6.0, "metrics.debt": -4.0, "metrics.nhs_backlog": 6.0, "metrics.public_support": -10.0}
                    },
                    {
                        "label": "Accept Deficit Expansion & Gilt Yield Risk",
                        "effects": {"metrics.debt": 5.0, "metrics.inflation": 1.2, "metrics.public_support": 4.0}
                    }
                ]
            }
        }
    }

def advance_turn(game):
    state = game["state"]
    metrics = state["metrics"]
    
    growth_drift = (metrics["government_stability"] - 50) * 0.015 - (metrics["inflation"] * 0.05)
    metrics["growth"] = round(max(-4.0, min(6.0, 1.3 + growth_drift)), 2)
    metrics["gdp"] *= (1.0 + metrics["growth"] / 100.0)
    metrics["fiscal_headroom"] = round(metrics["fiscal_headroom"] + (metrics["growth"] * 1.5) - (metrics["debt"] * 0.02), 1)
    
    state["turn"] += 1
    state["history"].append({
        "year": state["year"],
        "gdp": metrics["gdp"],
        "debt": metrics["debt"],
        "inflation": metrics["inflation"],
        "stability": metrics["government_stability"]
    })
    
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
