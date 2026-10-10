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
                "pros": "Boosts **Military Readiness (+12.0)**.",
                "cons": "Spikes **National Debt (+8.0)** and cuts **FDI (-5.0)**.",
                "effects": {"metrics.military_readiness": 12.0, "metrics.debt": 8.0, "metrics.international_tension": 15.0, "metrics.media_sentiment": 6.0}
            },
            {
                "label": "Provide Limited Hardware & Mediate",
                "elaboration": "Restrict Whitehall's response to supplying non-lethal hardware, intelligence-sharing, and FCDO diplomatic mediation.",
                "pros": "Maintains public support (**Public Support +3.0**).",
                "cons": "Degrades international clout (**Diplomacy -6.0**).",
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
                "pros": "Clears emergency backlogs (**NHS Backlog -12.0**).",
                "cons": "Increases public borrowing (**National Debt +5.0**).",
                "effects": {"metrics.nhs_backlog": -12.0, "metrics.debt": 5.0, "metrics.public_support": 8.0, "cabinet.Health Secretary.loyalty": 15}
            },
            {
                "label": "Enforce Minimum Service & Hold Pay Caps",
                "elaboration": "Invoke statutory Minimum Service Levels (MSLs), threatening union leadership with high court injunctions if pickets block emergency cover.",
                "pros": "Defends fiscal rules and reassures bond markets.",
                "cons": "Craters **Government Stability (-6.0)** and public support.",
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
                "pros": "Boosts international **Legitimacy (+5.0)**.",
                "cons": "Fractures **Government Stability (-8.0)**.",
                "effects": {"metrics.legitimacy": 5.0, "devolved_nations.Scotland (Holyrood).relations": 20, "metrics.government_stability": -8.0}
            },
            {
                "label": "Issue Definitive Constitutional Veto",
                "elaboration": "Reject the request outright at the dispatch box, declaring the 2014 vote a once-in-a-generation event.",
                "pros": "Reinforces domestic order (**Government Stability +6.0**).",
                "cons": "Spikes **Scotland Unrest (+30)**.",
                "effects": {"metrics.government_stability": 6.0, "devolved_nations.Scotland (Holyrood).unrest": 30}
            }
        ]
    },
    {
        "id": "uk_dil_sovereign_grant",
        "title": "Royal Friction: Sovereign Grant & Palatial Retrofit",
        "description": "Buckingham Palace formally submits a request for an emergency 40% uplift to the Sovereign Grant to fund critical asbestos removal and green energy retrofits.",
        "choices": [
            {
                "label": "Approve Full Sovereign Grant Increase",
                "elaboration": "Instruct the Treasury to sign off on the increased royal funding settlement without parliamentary delay.",
                "pros": "Preserves royal goodwill and institutional harmony.",
                "cons": "Sparks public anger amid cost-of-living pressures (**Public Support -6.0**, **Headroom -£1.5bn**).",
                "effects": {"metrics.public_support": -6.0, "metrics.fiscal_headroom": -1.5, "metrics.media_sentiment": -4.0}
            },
            {
                "label": "Reject Increase & Demand Cost-Cutting",
                "elaboration": "Block the funding request at the Treasury dispatch box, advising the Royal Household to draw from private estate reserves.",
                "pros": "Appases anti-monarchist backbenchers and protects Treasury funds.",
                "cons": "Strains relations with the Sovereign, leading to constitutional friction.",
                "effects": {"metrics.fiscal_headroom": 1.0, "metrics.public_support": 3.0, "metrics.media_sentiment": -5.0}
            }
        ]
    },
    {
        "id": "uk_dil_royal_assent_veto",
        "title": "Constitutional Crisis: Controversial Bill & Royal Assent",
        "description": "Your flagship public order bill passes through Parliament, but rumors leak that the King harbors deep reservations and might withhold Royal Assent.",
        "choices": [
            {
                "label": "Issue Strict Constitutional Ultimatum to the Palace",
                "elaboration": "Dispatch the Cabinet Secretary to remind Palace officials that the convention of binding Royal Assent has remained absolute since 1707.",
                "pros": "Defends parliamentary sovereignty and executive primacy (**Government Stability +5.0**).",
                "cons": "Alienates the monarch and sparks establishment media panic (**Media Sentiment -10.0**).",
                "effects": {"metrics.government_stability": 5.0, "metrics.media_sentiment": -10.0, "metrics.legitimacy": -4.0}
            },
            {
                "label": "Amend the Bill to Accommodate Royal Concerns",
                "elaboration": "Quietly pause the legislation's final stages to negotiate compromise amendments satisfying royal legal advisers.",
                "pros": "Averts a historic constitutional showdown.",
                "cons": "Weakens political authority and enrages radical backbenchers (**Government Stability -8.0**).",
                "effects": {"metrics.government_stability": -8.0, "metrics.public_support": -3.0}
            }
        ]
    },
    {
        "id": "uk_dil_civil_service_leak",
        "title": "Whitehall Leak: Permanent Secretary Open Resistance",
        "description": "A hostile memo from a senior Whitehall Permanent Secretary is leaked to the BBC, accusing Number 10 of demanding unlawful policy shortcuts.",
        "choices": [
            {
                "label": "Suspend the Permanent Secretary and Launch Inquiry",
                "elaboration": "Order the Cabinet Office to suspend the official immediately and launch an internal security investigation.",
                "pros": "Asserts political control over Whitehall (**Government Stability +6.0**).",
                "cons": "Triggers corporate warfare across administrative desks (**Legitimacy -5.0**).",
                "effects": {"metrics.government_stability": 6.0, "metrics.legitimacy": -5.0, "metrics.media_sentiment": -4.0}
            },
            {
                "label": "Absorb the Blow and Issue Conciliatory Statement",
                "elaboration": "Publicly downplay the memo as routine policy debate and invite senior civil servants to consultation.",
                "pros": "Restores internal departmental harmony.",
                "cons": "Makes Number 10 look weak before the press lobby (**Media Sentiment -8.0**).",
                "effects": {"metrics.media_sentiment": -8.0, "metrics.government_stability": 2.0, "metrics.public_support": -2.0}
            }
        ]
    },
    {
        "id": "uk_dil_local_council_bankruptcy",
        "title": "Municipal Emergency: Major Council Section 114 Notice",
        "description": "A major metropolitan council formally issues a Section 114 bankruptcy notice, threatening immediate collapse of local social care and schools.",
        "choices": [
            {
                "label": "Bailout the Council with Emergency Treasury Grant",
                "elaboration": "Instruct the Chancellor to provide an immediate unringfenced cash injection to clear the structural deficit.",
                "pros": "Saves essential local services and avoids regional riots (**Public Support +5.0**).",
                "cons": "Eats heavily into fiscal headroom (**Fiscal Headroom -£2.0bn**).",
                "effects": {"metrics.fiscal_headroom": -2.0, "metrics.public_support": 5.0, "metrics.debt": 1.0}
            },
            {
                "label": "Impose Commissioners and Force Asset Sales",
                "elaboration": "Send in government-appointed commissioners to take over municipal operations and sell off public assets.",
                "pros": "Signals strict financial discipline to bond markets (**Government Stability +4.0**).",
                "cons": "Provokes fierce local protests and union backlash (**Unrest +15**).",
                "effects": {"metrics.government_stability": 4.0, "metrics.public_support": -6.0, "metrics.media_sentiment": -5.0}
            }
        ]
    },
    {
        "id": "uk_dil_bbc_impartiality_row",
        "title": "Culture War: BBC Impartiality & Licence Fee Row",
        "description": "Leading backbenchers accuse the BBC of institutional bias on current affairs broadcasts, demanding an immediate freeze to the licence fee.",
        "choices": [
            {
                "label": "Freeze Licence Fee and Order Governance Overhaul",
                "elaboration": "Announce a two-year statutory freeze on the licence fee and call for an independent review of editorial boards.",
                "pros": "Thrills right-leaning backbenchers and populists (**Government Stability +7.0**).",
                "cons": "Triggers international condemnation regarding press freedom (**Media Sentiment -8.0**).",
                "effects": {"metrics.government_stability": 7.0, "metrics.media_sentiment": -8.0, "metrics.diplomacy": -4.0}
            },
            {
                "label": "Defend BBC Independence and Protect Funding",
                "elaboration": "Release a Downing Street statement firmly backing the BBC charter and rebuking attacks from backbenchers.",
                "pros": "Preserves international standing and media goodwill (**Media Sentiment +6.0**).",
                "cons": "Enrages your party's traditionalist wing (**Government Stability -6.0**).",
                "effects": {"metrics.media_sentiment": 6.0, "metrics.government_stability": -6.0, "metrics.public_support": 2.0}
            }
        ]
    },
    {
        "id": "uk_dil_by_election_defeat",
        "title": "By-Election Shock: Safe Seat Collapse",
        "description": "A stunning swing against your party results in a historic by-election defeat in a previously safe heartland seat.",
        "choices": [
            {
                "label": "Announce Cabinet Reshuffle & Policy Pivot",
                "elaboration": "Acknowledge voter frustration by sacking underperforming ministers and pivoting your manifesto.",
                "pros": "Seizes control of news agenda and pacifies MPs (**Government Stability +5.0**).",
                "cons": "Projects internal panic to the electorate (**Public Support -4.0**).",
                "effects": {"metrics.government_stability": 5.0, "metrics.public_support": -4.0, "metrics.majority_seats": -1}
            },
            {
                "label": "Stay the Course and Blame Mid-Term Blues",
                "elaboration": "Dismiss the result at the Despatch Box as standard mid-term fatigue, insisting your long-term plan is unchanged.",
                "pros": "Demonstrates unshakeable personal resolve.",
                "cons": "Deepens backbench despair and rebellion (**Government Stability -8.0**).",
                "effects": {"metrics.government_stability": -8.0, "metrics.media_sentiment": -6.0, "metrics.majority_seats": -1}
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
                "pros": "Averts legislative defeat (**Government Stability +5.0**).",
                "cons": "Eats into **Fiscal Headroom (-3.0bn)**.",
                "effects": {"metrics.government_stability": 5.0, "metrics.fiscal_headroom": -3.0}
            },
            {
                "label": "Threaten Deselection & Whip Withdrawal",
                "elaboration": "Warn rebels that anyone voting against the government will immediately have the party whip withdrawn.",
                "pros": "Asserts ruthless executive dominance.",
                "cons": "Crashes **Media Sentiment (-8.0)**.",
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
                    "pros": "Boosts baseline **Government Stability (+15.0)**.",
                    "cons": "Weakens executive grip and bleeds headroom.",
                    "effects": {"metrics.government_stability": 15.0, "metrics.public_support": 5.0, "metrics.fiscal_headroom": -4.0}
                },
                {
                    "label": "Dissolve Parliament & Call Snap Election",
                    "elaboration": "Request a parliamentary dissolution at Buckingham Palace to take your case directly to voters.",
                    "pros": "Resets the political clock.",
                    "cons": "Risks catastrophic electoral defeat.",
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
