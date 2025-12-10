def compute_profile(activities):
    """
    Analyse simple mais utile :
    - charge d'entraînement
    - intensités
    - CP max
    - tendance progression
    """

    total_hours = 0
    total_distance = 0
    z2_hours = 0
    z3_hours = 0
    z4_hours = 0
    z5_hours = 0

    for act in activities:
        h = act.get("moving_time", 0) / 3600
        total_hours += h
        total_distance += act.get("distance", 0) / 1000

        if "power_zones" in act:
            z2_hours += act["power_zones"].get("Z2", 0) / 3600
            z3_hours += act["power_zones"].get("Z3", 0) / 3600
            z4_hours += act["power_zones"].get("Z4", 0) / 3600
            z5_hours += act["power_zones"].get("Z5", 0) / 3600

    profile = {
        "total_hours": round(total_hours, 1),
        "total_distance": round(total_distance, 1),
        "z2_hours": round(z2_hours, 1),
        "z3_hours": round(z3_hours, 1),
        "z4_hours": round(z4_hours, 1),
        "z5_hours": round(z5_hours, 1),
    }

    return profile
