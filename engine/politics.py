import random

WESTMINSTER_FACTIONS = {
    "Labour Party": {
        "Socialist Campaign Group": {"size_MPs": 85, "happiness": 70, "key_demand": "Nationalize Utilities & Wealth Taxes"},
        "Soft Left / Leadership Core": {"size_MPs": 180, "happiness": 80, "key_demand": "Pragmatic Public Service Reform"},
        "Labour First / Centrists": {"size_MPs": 83, "happiness": 75, "key_demand": "Fiscal Discipline & Pro-Business Growth"}
    },
    "Conservative Party": {
        "One Nation Conservatives": {"size_MPs": 45, "happiness": 65, "key_demand": "Protect Public Spending & Green Targets"},
        "Free Market Right / ERG": {"size_MPs": 50, "happiness": 60, "key_demand": "Aggressive Deregulation & Tax Cuts"},
        "National Conservatives": {"size_MPs": 26, "happiness": 55, "key_demand": "Strict Border Controls & Sovereignty"}
    },
    "Liberal Democrats": {
        "Social Liberals": {"size_MPs": 40, "happiness": 75, "key_demand": "Public Investment & Social Justice"},
        "Orange Book Centrists": {"size_MPs": 32, "happiness": 70, "key_demand": "Market Efficiency & Free Trade"}
    },
    "Reform UK": {
        "Populist Hardliners": {"size_MPs": 5, "happiness": 65, "key_demand": "Drastic Immigration Controls"}
    },
    "Green Party": {
        "Eco-Socialists": {"size_MPs": 4, "happiness": 70, "key_demand": "Aggressive Net Zero Mandates"}
    }
}

def initialize_factions(ruling_party_name):
    """Initializes factional breakdown for the chosen ruling party."""
    if ruling_party_name in WESTMINSTER_FACTIONS:
        # Return a deep copy so state mutation works independently per game
        import copy
        return copy.deepcopy(WESTMINSTER_FACTIONS[ruling_party_name])
    return {
        "Core Loyalists": {"size_MPs": 50, "happiness": 75, "key_demand": "Party Loyalty"}
    }

def simulate_faction_drift(state):
    """Calculates factional happiness shifts based on national conditions and debt."""
    factions = state.get("factions", {})
    metrics = state["metrics"]
    
    for faction_name, data in factions.items():
        # Penalize happiness if debt or inflation gets too high
        if metrics["debt"] > 105.0:
            data["happiness"] = max(0, data["happiness"] - 2)
        if metrics["public_support"] < 40.0:
            data["happiness"] = max(0, data["happiness"] - 3)
            
        # Natural drift toward baseline
        data["happiness"] = min(100, max(0, data["happiness"] + random.uniform(-1.5, 1.5)))

def check_leadership_challenge(state):
    """Checks if disgruntled MPs exceed the threshold to trigger a leadership challenge."""
    factions = state.get("factions", {})
    total_mps = sum(data["size_MPs"] for data in factions.values())
    if total_mps == 0:
        return False
        
    disgruntled_mps = sum(data["size_MPs"] for data in factions.values() if data["happiness"] < 45)
    
    # If over 35% of the party MPs are deeply unhappy, trigger an internal challenge
    if disgruntled_mps > (total_mps * 0.35):
        return True
    return False
