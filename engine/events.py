import random

COMPLEX_UK_DILEMMAS = [
    {
        "id": "uk_dil_eastern_flank",
        "title": "Geopolitical Crisis: Eastern European Conflict Escalation",
        "description": "An aggressive regional power has launched a major offensive on the eastern European border. NATO allies demand immediate British military deployment and a massive surge in defense manufacturing.",
        "choices": [
            {
                "label": "Deploy Expeditionary Force & Commit £15bn Aid Package",
                "elaboration": "You order the Ministry of Defence to dispatch 12,000 troops from the 3rd (UK) Division to the eastern NATO frontier, accompanied by an emergency £15bn supplementary defense estimate funded through gilt issuance.",
                "pros": "Deepens special security alignment with Washington and Brussels, solidifies international standing, and massively increases **Military Readiness (+12.0)**.",
                "cons": "Triggers a severe Treasury flashpoint: gilt yields spike due to surging debt issuance (**National Debt +8.0**), forcing private investment and foreign capital (**FDI -5.0**) to contract.",
                "effects": {"metrics.military_readiness": 12.0, "metrics.debt": 8.0, "metrics.international_tension": 15.0, "metrics.media_sentiment": 6.0}
            },
            {
                "label": "Provide Limited Hardware & Plead for De-escalation",
                "elaboration": "You restrict Whitehall's response to supplying non-lethal defensive hardware, intelligence-sharing, and diplomatic mediation via the Foreign, Commonwealth & Development Office (FCDO).",
                "pros": "Protects your fragile fiscal headroom and keeps public support stable by avoiding expensive foreign entanglements (**Public Support +3.0**).",
                "cons": "Alienates key NATO partners who view Britain as shirking its continental defense obligations, degrading your international clout (**Diplomacy -6.0**).",
                "effects": {"metrics.diplomacy": -6.0, "metrics.military_readiness": 2.0, "metrics.public_support": 3.0}
            }
        ]
    },
    {
        "id": "uk_dil_nhs_strike",
        "title": "NHS General Strike & Hospital Gridlock",
        "description": "The British Medical Association (BMA) and Royal College of Nursing (RCN) reject a pay offer and launch synchronized 72-hour strikes across acute hospital trusts, crippling waiting lists.",
        "choices": [
            {
                "label": "Meet Full Union Pay Demands (Full Settlement)",
                "elaboration": "You instruct the Department of Health and Social Care to bypass the Pay Review Bodies and negotiate a fully funded 12% multi-year settlement for clinical staff.",
                "pros": "Instantly halts industrial action, clears emergency ward bottlenecks (**NHS Backlog -12.0**), and builds immense goodwill with public sector trade unions.",
                "cons": "Blasts a £6bn hole through the Chancellor's departmental spending caps, forcing immediate public borrowing increases (**National Debt +5.0**).",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Enforce Minimum Service Legislation & Hold Pay Caps",
                "elaboration": "You invoke statutory Minimum Service Levels (MSLs), threatening union leadership with high court injunctions and asset seizures if picket lines block emergency cover.",
                "pros": "Defends the Treasury's fiscal rules, avoids inflationary public pay precedents, and signals fiscal orthodoxy to the bond markets.",
                "cons": "Provokes prolonged industrial bitterness, cratering **Government Stability (-6.0)** and driving public approval downward as elective surgeries are canceled en masse.",
                "effects": {"metrics.government_stability": -6.0, "metrics.nhs_backlog": 8.0, "metrics.public_support": -10.0}
            }
        ]
    },
    {
        "id": "uk_dil_scots_indy",
        "title": "Holyrood Independence Referendum Demand",
        "description": "The First Minister at Holyrood formally requests a Section 30 order to hold a legally binding second independence referendum, citing divergence over economic policy.",
        "choices": [
            {
                "label": "Grant Section 30 Referendum Mandate",
                "elaboration": "You sign the constitutional instrument transferring legislative competence back to the Scottish Parliament, validating Edinburgh's path to an independence vote.",
                "pros": "Demonstrates absolute commitment to democratic self-determination, restoring constitutional trust and boosting international **Legitimacy (+5.0)**.",
                "cons": "Triggers open revolt among Unionist MPs and Conservative backbenchers, fracturing **Government Stability (-8.0)** and threatening the territorial integrity of the UK.",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood).relations": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Veto",
                "elaboration": "You reject the request outright at the dispatch box, declaring that the 2014 referendum was a 'once-in-a-generation' event and closing the door on any transfer of powers.",
                "pros": "Appases the patriotic and unionist wings of parliament, reinforcing domestic political order and short-term stability (**Government Stability +6.0**).",
                "cons": "Galvanizes nationalist sentiment, sparking large-scale protests in George Square and tanking diplomatic relations with Holyrood (**Scotland Unrest +30**).",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood).unrest": 30}
            }
        ]
    }
]

CHAINED_UK_FOLLOW_UPS = {
    "uk_rebel_backbench": {
        "title": "Backbench MP Rebellion on the Finance Bill",
        "description": "Dozens of your own party's backbenchers threaten to walk through the lobby against the government's flagship Finance Bill over proposed property and tax thresholds.",
        "choices": [
            {
                "label": "Compromise and Amend the Bill to Satisfy Rebels",
                "elaboration": "You summon rebel ringleaders to Number 10, watering down the tax clauses and carving out exemptions for their rural and suburban constituencies.",
                "pros": "Secures parliamentary numbers, averting a humiliating legislative defeat and maintaining **Government Stability (+5.0)**.",
                "cons": "Compromises the integrity of your fiscal program and eats into your available **Fiscal Headroom (-3.0bn)**.",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection & Whip Withdrawal",
                "elaboration": "You let loose the Chief Whip to warn rebels that anyone voting against the government will immediately have the party whip withdrawn and be barred from standing at the next election.",
                "pros": "Asserts ruthless executive dominance, showing the parliamentary party that the Prime Minister commands absolute authority.",
                "cons": "Triggers fierce hostility from lobby journalists, crashing **Media Sentiment (-8.0)** as civil war inside your party dominates the news cycle.",
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
            "description": "With government stability and backbench support collapsing, the Opposition leader tables an emergency motion of no confidence under the Fixed-Term Parliaments framework.",
            "choices": [
                {
                    "label": "Surrender Key Cabinet Portfolios to Rebel Factions",
                    "elaboration": "You offer senior ministerial posts to factional leaders, reshaping your top team to buy their survival votes in the division lobbies.",
                    "pros": "Stops the government from falling, preserves your parliamentary tenure, and shores up baseline **Government Stability (+15.0)**.",
                    "cons": "Transforms your Cabinet into a divided camp of rivals, weakening your executive grip and bleeding fiscal leeway.",
                    "effects": {"metrics.government_stability": 15.0, "metrics.public_support": 5.0, "metrics.fiscal_headroom": -4.0}
                },
                {
                    "label": "Dissolve Parliament & Call Snap General Election",
                    "elaboration": "You head to Buckingham Palace to request a dissolution of Parliament, taking your political fate directly to the British electorate.",
                    "pros": "Resets the political clock and gives you a fighting chance to secure a fresh mandate if your public ratings rebound.",
                    "cons": "Carries an immense electoral risk: a poorly timed campaign could see your party decimated at the ballot box.",
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
        ("Whitehall Intelligence Briefing", "MI5 reports heightened state-sponsored cyber probing against national critical infrastructure."),
        ("Bank of England Rate Notice", "Governor maintains benchmark interest rates amid sticky service-sector inflation readings."),
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
