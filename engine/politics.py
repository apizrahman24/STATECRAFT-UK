import random

def create_uk_parties():
    return {
        "Labour Party": {
            "ideology": "Social Democratic",
            "seats": 348,
            "popularity": 42,
            "loyalty": 75,
            "radicalism": 15
        },
        "Conservative Party": {
            "ideology": "Conservative",
            "seats": 121,
            "popularity": 28,
            "loyalty": 60,
            "radicalism": 20
        },
        "Liberal Democrats": {
            "ideology": "Centrist / Liberal",
            "seats": 72,
            "popularity": 12,
            "loyalty": 50,
            "radicalism": 10
        },
        "Reform UK": {
            "ideology": "Right-Wing Populist",
            "seats": 5,
            "popularity": 14,
            "loyalty": 30,
            "radicalism": 45
        },
        "Scottish National Party": {
            "ideology": "Regional Nationalist",
            "seats": 9,
            "popularity": 4,
            "loyalty": 40,
            "radicalism": 30
        }
    }

def simulate_party_politics(state, inflation, unemployment):
    for party in state["parties"].values():
        if inflation > 4.5 and party["ideology"] in ["Conservative", "Right-Wing Populist"]:
            party["popularity"] += 0.6
        elif inflation <= 3.0 and party["ideology"] == "Social Democratic":
            party["popularity"] += 0.4
        
        party["popularity"] += random.uniform(-0.5, 0.5)
        party["popularity"] = max(0, min(100, party["popularity"]))
