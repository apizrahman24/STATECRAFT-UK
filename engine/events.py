import random

COMPLEX_UK_DILEMMAS = [
    {
        "id": "uk_dil_eastern_flank",
        "title": "Geopolitical Crisis: Eastern European Conflict Escalation",
        "description": "An aggressive regional power has launched a major offensive on the eastern European border. NATO allies demand British troop deployments.",
        "choices": [
            {
                "label": "Deploy Expeditionary Force & Commit £15bn Aid",
                "effects": {"metrics.military_readiness": 12.0, "metrics.debt": 8.0, "metrics.international_tension": 15.0, "metrics.media_sentiment": 6.0}
            },
            {
                "label": "Provide Limited Defensive Hardware Only",
                "effects": {"metrics.diplomacy": -6.0, "metrics.military_readiness": 2.0, "metrics.public_support": 3.0}
            }
        ]
    },
    {
        "id": "uk_dil_nhs_strike",
        "title": "NHS General Strike & Hospital Gridlock",
        "description": "Healthcare syndicates have rejected pay offers and started synchronized walkouts, threatening severe A&E delays.",
        "choices": [
            {
                "label": "Meet Full Union Pay Demands",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Enforce Minimum Staffing Legislation",
                "effects": {"metrics.government_stability": -6.0, "metrics.nhs_backlog": 8.0, "metrics.public_support": -10.0}
            }
        ]
    },
    {
        "id": "uk_dil_scots_indy",
        "title": "Holyrood Independence Referendum Demand",
        "description": "The First Minister of Scotland formally requests Section 30 powers to hold a second independence referendum.",
        "choices": [
            {
                "label": "Grant Section 30 Referendum Mandate",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood).relations": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Veto",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood).unrest": 30}
            }
        ]
    }
]

CHAINED_UK_FOLLOW_UPS = {
    "uk_rebel_backbench": {
        "title": "Backbench MP Rebellion on the Finance Bill",
        "description": "Dozens of your own backbench MPs threaten to vote down the Government's finance bill.",
        "choices": [
            {
                "label": "Compromise and Amend the Bill",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection and Whip Withdrawal",
                "effects": {"metrics.government_stability": -10.0, "metrics.media_sentiment": -8.0}
            }
        ]
    }
}

def trigger_era_event(state, game):
    metrics = state["metrics"]
    
    # Check for Vote of No Confidence trigger if stability or majority collapses
    if metrics["government_stability"] < 35.0 or state["majority_seats"] < 320:
        state["active_dilemma"] = {
            "id": "vote_of_no_confidence",
            "title": "🚨 PARLIAMENTARY VOTE OF NO CONFIDENCE",
            "description": "With government stability and backbench backing collapsing, the Opposition has tabled an emergency motion of no confidence in the House of Commons!",
            "choices": [
                {
                    "label": "Fight and Surrender Key Cabinet Portfolios to Rebel Factions",
                    "effects": {"metrics.government_stability": 15.0, "metrics.public_support": 5.0, "metrics.fiscal_headroom": -4.0}
                },
                {
                    "label": "Call Snap General Election (Risk Campaign Defeat)",
                    "effects": {"metrics.government_stability": 25.0, "metrics.public_support": 10.0}
                }
            ]
        }
        return

    if not state.get("active_dilemma") and state.get("queued_dilemma"):
        follow_id = state.pop("queued_dilemma")
        if follow_id in CHAINED_UK_FOLLOW_UPS:
            state["active_dilemma"] = CHAINED_UK_FOLLOW_UPS[follow_id]
            return

    if not state.get("active_dilemma") and random.random() < 0.50:
        state["active_dilemma"] = random.choice(COMPLEX_UK_DILEMMAS)

    news_items = [
        ("Whitehall Intelligence Briefing", "MI5 reports heightened cyber probing against national critical infrastructure."),
        ("Bank of England Rate Notice", "Governor maintains benchmark interest rates amid sticky service-sector inflation."),
        ("BBC Today Programme", "Political editors scrutinize Number 10 over upcoming legislative priorities.")
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

    if random.random() < 0.35:
        state["queued_dilemma"] = "uk_rebel_backbench"

    state["events"].append({
        "year": state["year"],
        "title": f"Cabinet Executive Order: {dilemma['title']}",
        "description": f"Executed Strategy: '{choice['label']}'."
    })
    state["active_dilemma"] = None
