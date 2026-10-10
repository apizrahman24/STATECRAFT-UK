import copy
import random
from engine.events import trigger_era_event
from engine.politics import initialize_factions, simulate_faction_drift, check_leadership_challenge

POLICIES = {
    "Comprehensive Spending Review Cuts": {
        "description": "Enforce strict spending freezes across Whitehall to preserve fiscal headroom.",
        "elaboration": "Implement across-the-board 3% departmental budget freezes for non-ringfenced ministries.",
        "pros": "Lowers debt (**Debt -5.0%**).",
        "cons": "Damages services (**NHS Backlog +4.0**) and support (**Public Support -6.0**).",
        "effects": {"debt": -5.0, "public_support": -6.0, "nhs_backlog": 4.0, "media_sentiment": -8.0}
    },
    "Emergency NHS Capital Injection": {
        "description": "Direct emergency funding into hospital waiting lists and surgical backlogs.",
        "elaboration": "Authorize a £4bn emergency Treasury grant to NHS acute trusts for weekend overtime and waiting list clearance.",
        "pros": "Clears waiting lists (**NHS Backlog -10.0**) and builds goodwill (**Public Support +7.0**).",
        "cons": "Increases short-term borrowing (**Debt +4.0%**).",
        "effects": {"nhs_backlog": -10.0, "public_support": 7.0, "debt": 4.0, "media_sentiment": 5.0}
    },
    "Green Industrial Transition Subsidy": {
        "description": "Subsidize renewable grid infrastructure and clean-tech startups to boost productivity.",
        "elaboration": "Deploy capital grants and tax allowances to private developers building offshore wind and battery networks.",
        "pros": "Drives growth (**GDP +3.2%**) and green jobs (**Unemployment -1.0%**).",
        "cons": "Requires state borrowing (**Debt +3.5%**).",
        "effects": {"gdp": 3.2, "fdi": 5.0, "unemployment": -1.0, "debt": 3.5}
    },
    "Bank of England Rate Defense": {
        "description": "Coordinate with Threadneedle Street to signal tighter monetary policy.",
        "effects": {"inflation": -2.2, "growth": -1.0, "public_support": -2.0},
        "elaboration": "Issue formal Treasury guidance endorsing tight interest rate targets to tame core inflation.",
        "pros": "Cools inflation (**Inflation -2.2%**).",
        "cons": "Dampens growth (**GDP Growth -1.0%**).",
    },
    "Launch Media Defense Campaign": {
        "description": "Deploy government spin doctors to saturate broadcast and print media.",
        "elaboration": "Mobilize Downing Street communications staff to coordinate media appearances defending policies.",
        "pros": "Improves media sentiment (**Media Sentiment +15.0**).",
        "cons": "Consumes fiscal headroom (**Fiscal Headroom -£1.5bn**).",
        "effects": {"media_sentiment": 15.0, "fiscal_headroom": -1.5, "public_support": 4.0}
    }
}

DEVOLVED_ACTIONS = {
    "Increase Block Grant Allocation": {
        "description": "Bypass local friction by increasing the Barnett formula block grant allocation.",
        "cost_headroom": 2.0,
        "effects": {"relations": 12, "unrest": -10}
    },
    "Bilateral Constitutional Summit": {
        "description": "Invite First Ministers to 10 Downing Street for direct negotiations to defuse tensions.",
        "cost_headroom": 0.5,
        "effects": {"relations": 8, "unrest": -5}
    },
    "Invoke Westminster Override / Veto": {
        "description": "Assert parliamentary sovereignty to override contentious local legislation.",
        "cost_headroom": 0.0,
        "effects": {"relations": -15, "unrest": 10}
    }
}

def apply_devolved_action(game, nation_name, action_name):
    state = game["state"]
    action = DEVOLVED_ACTIONS.get(action_name)
    if not action:
        return False
    
    if state["metrics"]["fiscal_headroom"] < action["cost_headroom"]:
        return False
        
    state["metrics"]["fiscal_headroom"] -= action["cost_headroom"]
    nation = state["devolved_nations"][nation_name]
    
    nation["relations"] = max(0, min(100, nation["relations"] + action["effects"]["relations"]))
    nation["unrest"] = max(0, min(100, nation["unrest"] + action["effects"]["unrest"]))
    
    state["events"].append({
        "year": state["year"],
        "title": f"Devolved Policy: {nation_name} - {action_name}",
        "description": action["description"]
    })
    return True

def create_uk_game(pm_name, ruling_party):
    if ruling_party == "Labour Party":
        seats = 348
        stability = 75.0
        approval = 54.0
    elif ruling_party == "Conservative Party":
        seats = 121
        stability = 58.0
        approval = 42.0
    elif ruling_party == "Liberal Democrats":
        seats = 72
        stability = 62.0
        approval = 46.0
    elif ruling_party == "Reform UK":
        seats = 5
        stability = 50.0
        approval = 48.0
    else:
        seats = 4
        stability = 55.0
        approval = 45.0

    return {
        "country_name": "United Kingdom",
        "leader": pm_name,
        "ruling_party": ruling_party,
        "era": "Modern Era (Westminster Simulation)",
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
                "media_sentiment": 50.0,
                "legitimacy": 68.0,
                "nhs_backlog": 62.0,
                "fdi": 25.0,
                "diplomacy": 65.0,
                "military_readiness": 58.0,
                "international_tension": 35.0
            },
            "cabinet": {
                "Chancellor of the Exchequer": {"name": "Rachel Reeves", "loyalty": 75, "competence": 80, "ambition": 60},
                "Foreign Secretary": {"name": "David Lammy", "loyalty": 70, "competence": 72, "ambition": 65},
                "Health Secretary": {"name": "Wes Streeting", "loyalty": 65, "competence": 78, "ambition": 85},
                "Home Secretary": {"name": "Yvette Cooper", "loyalty": 78, "competence": 74, "ambition": 50}
            },
            "factions": initialize_factions(ruling_party),
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
                "description": "The OBR warns that pay settlements and energy volatility have squeezed fiscal headroom down to £7bn. Treasury officials present three paths.",
                "choices": [
                    {
                        "label": "Introduce Targeted Wealth and CGT Adjustments",
                        "elaboration": "Raise rates on Capital Gains Tax and dividend yields to fund frontline public services.",
                        "pros": "Protects core departments and unlocks **£8.0bn Fiscal Headroom**.",
                        "cons": "Triggers City backlash (**Public Support -8.0**, **Media -10.0**).",
                        "effects": {"metrics.fiscal_headroom": 8.0, "metrics.debt": -3.0, "metrics.public_support": -8.0, "metrics.media_sentiment": -10.0}
                    },
                    {
                        "label": "Implement Severe Whitehall Spending Freezes",
                        "elaboration": "Enforce strict nominal budget freezes across non-protected departments.",
                        "pros": "Lowers public debt (**Debt -4.0**).",
                        "cons": "Worsens waiting lists (**NHS Backlog +6.0**, **Media -12.0**).",
                        "effects": {"metrics.fiscal_headroom": 6.0, "metrics.debt": -4.0, "metrics.nhs_backlog": 6.0, "metrics.media_sentiment": -12.0}
                    },
                    {
                        "label": "Accept Deficit Expansion & Gilt Yield Risk",
                        "elaboration": "Bypass fiscal tightening by increasing gilt sales through the Debt Management Office.",
                        "pros": "Provides short-term political relief (**Public Support +4.0**).",
                        "cons": "Spikes borrowing (**Debt +5.0**) and inflation (**Inflation +1.2%**).",
                        "effects": {"metrics.debt": 5.0, "metrics.inflation": 1.2, "metrics.public_support": 4.0, "metrics.media_sentiment": 5.0}
                    }
                ]
            }
        }
    }

def advance_turn(game):
    state = game["state"]
    metrics = state["metrics"]
    
    simulate_faction_drift(state)
    
    if check_leadership_challenge(state):
        state["active_dilemma"] = {
            "id": "leadership_challenge",
            "title": "🚨 INTERNAL PARTY LEADERSHIP CHALLENGE",
            "description": "Deep backbench dissatisfaction reaches a boiling point as ambitious rivals circulate letters of no confidence.",
            "choices": [
                {
                    "label": "Offer Major Policy Concessions & Cabinet Upgrades",
                    "effects": {"metrics.government_stability": 10.0, "metrics.fiscal_headroom": -3.0, "metrics.public_support": 3.0}
                },
                {
                    "label": "Fight Challenge Head-On & Expel Rebels",
                    "effects": {"metrics.government_stability": -15.0, "metrics.media_sentiment": -10.0, "metrics.majority_seats": -12}
                }
            ]
        }
        return

    growth_drift = (metrics["government_stability"] - 50) * 0.015 - (metrics["inflation"] * 0.05)
    metrics["growth"] = round(max(-4.0, min(6.0, 1.3 + growth_drift)), 2)
    metrics["gdp"] *= (1.0 + metrics["growth"] / 100.0)
    metrics["fiscal_headroom"] = round(metrics["fiscal_headroom"] + (metrics["growth"] * 1.5) - (metrics["debt"] * 0.02), 1)
    metrics["media_sentiment"] = round(metrics["media_sentiment"] * 0.9 + metrics["public_support"] * 0.1, 1)

    state["turn"] += 1
    
    if state["turn"] % 12 == 0:
        state["active_dilemma"] = {
            "id": "annual_budget_review",
            "title": f"Annual Chancellor's Budget Review ({state['year']})",
            "description": "It is time for the Chancellor's major fiscal statement under OBR scrutiny.",
            "choices": [
                {
                    "label": "Expansionary Tax Cuts & Public Investment",
                    "effects": {"metrics.debt": 8.0, "metrics.growth": 2.0, "metrics.public_support": 10.0, "metrics.media_sentiment": 8.0}
                },
                {
                    "label": "Orthodox Fiscal Balance & Deficit Reduction",
                    "effects": {"metrics.debt": -7.0, "metrics.growth": -1.0, "metrics.public_support": -9.0, "metrics.media_sentiment": -5.0}
                }
            ]
        }

    if random.random() < 0.3:
        seat_change = random.choice([-2, -1, 1, 2])
        state["majority_seats"] += seat_change
        state["events"].append({
            "year": state["year"],
            "title": "Parliamentary By-Election Result",
            "description": f"Net change in working majority seats: {seat_change:+d}."
        })

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
