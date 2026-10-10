import random

def simulate_economy(state):
    m = state["metrics"]

    # Random economic noise
    economic_noise = random.uniform(-0.25, 0.25)
    m["growth"] += economic_noise

    # Inflation dynamics (driven by debt and growth)
    inflation_pressure = (m["growth"] * 0.04) + random.uniform(-0.15, 0.15)
    m["inflation"] += inflation_pressure

    # Unemployment reaction
    m["unemployment"] -= (m["growth"] * 0.06)
    m["unemployment"] += random.uniform(-0.1, 0.1)

    # GDP compound updates
    m["gdp"] += m["gdp"] * (m["growth"] / 100.0)

    # NHS and Public Services backlog pressure
    if m["inflation"] > 4.0:
        m["nhs_backlog"] += 1.5
        m["public_support"] -= 1.0
    else:
        m["nhs_backlog"] -= 0.5

    # Clamp values to logical boundaries
    m["inflation"] = max(0.0, min(20.0, m["inflation"]))
    m["unemployment"] = max(1.0, min(25.0, m["unemployment"]))
    m["growth"] = max(-10.0, min(10.0, m["growth"]))
    m["debt"] = max(20.0, min(200.0, m["debt"]))
    m["nhs_backlog"] = max(10.0, min(100.0, m["nhs_backlog"]))
