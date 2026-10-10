import random

COMPLEX_UK_DILEMMAS = [
    {
        "id": "uk_dil_eastern_flank",
        "title": "Geopolitical Crisis: Eastern European Escalation",
        "description": "An aggressive power has launched an offensive on the eastern NATO border, triggering demands for immediate military deployment and defense manufacturing surges.",
        "choices": [
            {
                "label": "Deploy Expeditionary Force & Commit £15bn Aid",
                "elaboration": "Dispatch 12,000 troops from the 3rd (UK) Division to the eastern frontier, backed by a £15bn supplementary defense estimate funded through gilts.",
                "pros": "Strengthens security ties with Washington and Brussels, boosting **Military Readiness (+12.0)**.",
                "cons": "Surging debt issuance spikes gilt yields (**National Debt +8.0**) and contracts foreign capital (**FDI -5.0**).",
                "effects": {"metrics.military_readiness": 12.0, "metrics.debt": 8.0, "metrics.international_tension": 15.0, "metrics.media_sentiment": 6.0}
            },
            {
                "label": "Provide Limited Hardware & Mediate",
                "elaboration": "Restrict Whitehall's response to supplying non-lethal hardware, intelligence-sharing, and FCDO diplomatic mediation.",
                "pros": "Protects fragile fiscal headroom and maintains public support by avoiding foreign entanglements (**Public Support +3.0**).",
                "cons": "Alienates key NATO allies who view Britain as shirking defense duties (**Diplomacy -6.0**).",
                "effects": {"metrics.diplomacy": -6.0, "metrics.military_readiness": 2.0, "metrics.public_support": 3.0}
            }
        ]
    },
    {
        "id": "uk_dil_nhs_strike",
        "title": "NHS General Strike & Hospital Gridlock",
        "description": "BMA and RCN unions launch synchronized 72-hour strikes across acute hospital trusts, severely crippling national waiting lists.",
        "choices": [
            {
                "label": "Meet Full Union Pay Demands",
                "elaboration": "Instruct the Department of Health to bypass Pay Review Bodies and negotiate a fully funded 12% multi-year clinical staff pay settlement.",
                "pros": "Instantly halts strikes, clears emergency ward backlogs (**NHS Backlog -12.0**), and builds union goodwill.",
                "cons": "Creates a £6bn hole in departmental spending caps, forcing immediate public borrowing (**National Debt +5.0**).",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Enforce Minimum Service & Hold Pay Caps",
                "elaboration": "Invoke statutory Minimum Service Levels (MSLs), threatening union leadership with high court injunctions if pickets block emergency cover.",
                "pros": "Defends fiscal rules, avoids inflationary public pay precedents, and reassures bond markets.",
                "cons": "Provokes industrial bitterness, cratering **Government Stability (-6.0)** and public approval.",
                "effects": {"metrics.government_stability": -6.0, "metrics.nhs_backlog": 8.0, "metrics.public_support": -10.0}
            }
        ]
    },
    {
        "id": "uk_dil_scots_indy",
        "title": "Holyrood Independence Referendum Demand",
        "description": "The First Minister formally requests a Section 30 order to hold a legally binding second Scottish independence referendum.",
        "choices": [
            {
                "label": "Grant Section 30 Referendum Mandate",
                "elaboration": "Sign the constitutional instrument transferring legislative competence back to the Scottish Parliament.",
                "pros": "Demonstrates absolute commitment to democratic self-determination, boosting **Legitimacy (+5.0)**.",
                "cons": "Triggers open revolt among Unionist MPs, fracturing **Government Stability (-8.0)** and threatening UK integrity.",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood).relations": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Veto",
                "elaboration": "Reject the request outright at the dispatch box, declaring the 2014 vote a once-in-a-generation event.",
                "pros": "Appases patriotic and unionist wings, reinforcing domestic political order (**Government Stability +6.0**).",
                "cons": "Galvanizes nationalist sentiment and tanks diplomatic relations with Holyrood (**Scotland Unrest +30**).",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood).unrest": 30}
            }
        ]
    }
]

CHAINED_UK_FOLLOW_UPS = {
    "uk_rebel_backbench": {
        "title": "Backbench Rebellion on Finance Bill",
        "description": "Dozens of your own party's backbenchers threaten to vote against the government's flagship Finance Bill over tax thresholds.",
        "choices": [
            {
                "label": "Compromise and Amend Tax Clauses",
                "elaboration": "Water down tax clauses and carve out targeted exemptions for rural and suburban constituencies.",
                "pros": "Secures parliamentary numbers, averting legislative defeat (**Government Stability +5.0**).",
                "cons": "Eats into available **Fiscal Headroom (-3.0bn)** and compromises your fiscal program.",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection & Whip Withdrawal",
                "elaboration": "Warn rebels that anyone voting against the government will immediately have the party whip withdrawn.",
                "pros": "Asserts ruthless executive dominance and shows absolute leadership authority.",
                "cons": "Triggers fierce lobby hostility, crashing **Media Sentiment (-8.0)** amidst internal party civil war.",
                "effects": {"metrics.government_stability": -10.0, "metrics.media_sentiment": -8.0}
            }
        ]
    }
}

def trigger_era_event(state, game):
    metrics = state["metrics"]
    
    if metrics["government_stability"] < 35.0 or state["majority_seats"] < 320:
        state["active_dilemma"] = {
            "id": "vote_of_no_confidence",
            "title": "🚨 VOTE OF NO CONFIDENCE",
            "description": "With stability and backbench support collapsing, the Opposition tables an emergency motion of no confidence.",
            "choices": [
                {
                    "label": "Surrender Key Cabinet Posts to Rebels",
                    "elaboration": "Offer senior ministerial posts to factional leaders to buy their survival votes in division lobbies.",
                    "pros": "Prevents government collapse and boosts baseline **Government Stability (+15.0)**.",
                    "cons": "Transforms your Cabinet into a camp of rivals, weakening executive grip and bleeding headroom.",
                    "effects": {"metrics.government_stability": 15.0, "metrics.public_support": 5.0, "metrics.fiscal_headroom": -4.0}
                },
                {
                    "label": "Dissolve Parliament & Call Snap Election",
                    "elaboration": "Request a parliamentary dissolution at Buckingham Palace to take your case directly to voters.",
                    "pros": "Resets the political clock and offers a chance to secure a fresh mandate.",
                    "cons": "Carries immense electoral risk: a poorly timed campaign could decimate your party at the polls.",
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
        ("Whitehall Cyber Alert", "MI5 reports heightened state-sponsored cyber probing against national critical infrastructure."),
        ("Bank of England Briefing", "Governor maintains benchmark interest rates amid sticky service-sector inflation."),
        ("BBC Newsnight", "Political editors scrutinize Number 10 over upcoming legislative priorities.")
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
        "title": f"Cabinet Order: {dilemma['title']}",
        "description": f"Executed Strategy: '{choice['label']}'."
    })
    state["active_dilemma"] = None
