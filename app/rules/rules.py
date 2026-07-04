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
    Rule(

        name="Stopped Vehicle",

        severity="MEDIUM",

        description="A vehicle has remained stationary for an extended period.",

        condition=lambda analytics:

            len(
                analytics.stopped_vehicle_ids
            ) > 0,

    ),
    Rule(

        name="Emergency Vehicle",

        severity="HIGH",

        description="Emergency vehicle detected.",

        condition=lambda analytics:

            len(
                analytics.emergency_vehicles
            ) > 0,

    ),

]