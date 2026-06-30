from app.rules.rule import Rule

RULES = [

    Rule(
        name="Heavy Traffic",
        severity="MEDIUM",
        description="Heavy traffic detected.",
        condition=lambda analytics:
            analytics.congestion_level == "HEAVY",
    ),

    Rule(
        name="Traffic Jam",
        severity="HIGH",
        description="Severe congestion detected.",
        condition=lambda analytics:
            analytics.congestion_level == "SEVERE",
    ),

    Rule(
        name="Empty Road",
        severity="INFO",
        description="No vehicles detected.",
        condition=lambda analytics:
            analytics.current_vehicle_count == 0,
    ),

]