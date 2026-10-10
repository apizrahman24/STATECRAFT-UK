import random

COMPLEX_UK_DILEMMAS = [
    {
        "id": "uk_dil_eastern_flank",
        "title": "Geopolitical Crisis: Eastern European Conflict Escalation",
        "description": "An aggressive regional power has launched a major offensive on the eastern European border. NATO allies are demanding immediate British military deployments and a massive increase in security guarantees.",
        "choices": [
            {
                "label": "Deploy Expeditionary Force & Commit £15bn Aid",
                "elaboration": "You authorize the deployment of heavy armored brigades and air defense units to the NATO frontline while committing billions in defense packages.",
                "pros": "Drastically boosts **Military Readiness** and secures deep strategic alignment with Western international allies.",
                "cons": "Severely strains public finances (**National Debt** increases sharply) and redirects capital away from domestic infrastructure and foreign direct investment.",
                "effects": {"metrics.military_readiness": 12.0, "metrics.debt": 8.0, "metrics.international_tension": 15.0, "metrics.media_sentiment": 6.0}
            },
            {
                "label": "Provide Limited Defensive Hardware Only",
                "elaboration": "You opt for a middle-ground approach, sending anti-tank missiles and small arms without committing active British combat troops.",
                "pros": "Protects the national budget from massive borrowing spikes and keeps public support relatively stable.",
                "cons": "Damages diplomatic standing with key allies who expected heavier intervention, slightly reducing international trust.",
                "effects": {"metrics.diplomacy": -6.0, "metrics.military_readiness": 2.0, "metrics.public_support": 3.0}
            }
        ]
    },
    {
        "id": "uk_dil_nhs_strike",
        "title": "NHS General Strike & Hospital Gridlock",
        "description": "Healthcare syndicates have rejected the latest pay offers and initiated synchronized walkouts across acute care trusts, threatening severe A&E delays ahead of winter.",
        "choices": [
            {
                "label": "Meet Full Union Pay Demands",
                "elaboration": "You concede to union pressure and fully fund above-inflation pay settlements for doctors, nurses, and allied health professionals.",
                "pros": "Clears hospital waiting lists (**NHS Backlog** drops significantly) and instantly restores high goodwill among public sector workers and voters.",
                "cons": "Triggers an immediate multi-billion-pound hole in the national budget, causing **National Debt** to climb.",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Enforce Minimum Staffing Legislation",
                "elaboration": "You stand firm against union demands, using statutory powers to enforce strict minimum service levels and outlaw strikes in critical hospital departments.",
                "pros": "Preserves fiscal headroom and signals strong budgetary discipline to the Treasury and bond markets.",
                "cons": "Provokes prolonged industrial bitterness, cratering **Government Stability** and alienating public support as waiting lists grow.",
                "effects": {"metrics.government_stability": -6.0, "metrics.nhs_backlog": 8.0, "metrics.public_support": -10.0}
            }
        ]
    },
    {
        "id": "uk_dil_scots_indy",
        "title": "Holyrood Independence Referendum Demand",
        "description": "The First Minister of Scotland has formally requested Section 30 powers from Westminster to hold a second independence referendum, citing sharp policy divergences.",
        "choices": [
            {
                "label": "Grant Section 30 Referendum Mandate",
                "elaboration": "You choose a democratic accommodation path, formally granting Edinburgh the legal authority to stage an independence vote.",
                "pros": "Massively improves relations with devolved Scottish authorities and bolsters your international reputation for respecting constitutional democracy (**Legitimacy** rises).",
                "cons": "Deeply alarms unionist factions within your party, eroding **Government Stability** and risking the potential breakup of the United Kingdom.",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood).relations": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Veto",
                "elaboration": "You issue a flat rejection, stating that the matter was settled for a generation and refusing to grant the transfer of powers.",
                "pros": "Solidifies domestic political stability among unionist hardliners and prevents constitutional chaos in the short term.",
                "cons": "Sparks severe nationalist protests in Edinburgh, driving up regional unrest and tanking diplomatic relations with Holyrood.",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood).unrest": 30}
            }
        ]
    }
]

CHAINED_UK_FOLLOW_UPS = {
    "uk_rebel_backbench": {
        "title": "Backbench MP Rebellion on the Finance Bill",
        "description": "Dozens of your own backbench MPs threaten to vote down the Government's landmark finance bill over disagreement with tax and spending thresholds.",
        "choices": [
            {
                "label": "Compromise and Amend the Bill",
                "elaboration": "You invite rebel leaders into Number 10 to redraft key clauses of the legislation to satisfy their local constituency demands.",
                "pros": "Rebuilds party unity, averting a parliamentary defeat and securing immediate **Government Stability**.",
                "cons": "Dilutes the original fiscal package, eating into your available **Fiscal Headroom**.",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection and Whip Withdrawal",
                "elaboration": "You play hardball, threatening to strip any rebelling MP of the party whip and block them from running in future elections.",
                "pros": "Asserts absolute executive dominance and prevents backbenchers from holding the premiership hostage.",
                "cons": "Triggers fierce hostility in the press and deeply damages **Media Sentiment** as internal party warfare plays out publicly.",
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
            "title": "🚨 PARLIAMENTARY VOTE OF NO CONFIDENCE",
            "description": "With government stability and backbench support collapsing, the Opposition has tabled an emergency motion of no confidence in the House of Commons!",
            "choices": [
                {
                    "label": "Fight and Surrender Key Cabinet Portfolios to Rebel Factions",
                    "elaboration": "You concede major ministerial seats to internal factions to buy their survival votes in Parliament.",
                    "pros": "Keeps you in 10 Downing Street and restores baseline **Government Stability**.",
                    "cons": "Compromises your executive control and drains fiscal breathing room.",
                    "effects": {"metrics.government_stability": 15.0, "metrics.public_support": 5.0, "metrics.fiscal_headroom": -4.0}
                },
                {
                    "label": "Call Snap General Election (Risk Campaign Defeat)",
                    "elaboration": "You dissolve parliament and take your case directly to the British electorate.",
                    "pros": "Resets the political board and offers a chance to win a fresh mandate if public approval bounces back.",
                    "cons": "Carries a high risk of electoral defeat and ejection from office.",
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
