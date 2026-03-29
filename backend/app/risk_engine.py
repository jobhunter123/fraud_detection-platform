from app.ml_model import get_anomaly_score


def calculate_risk(data: dict) -> dict:
    risk = 0
    reasons = []

    if data.get("amount", 0) > 10000:
        risk += 30
        reasons.append("Large transaction amount detected")

    if data.get("device_new"):
        risk += 20
        reasons.append("New device detected")

    if data.get("location_change"):
        risk += 25
        reasons.append("Location mismatch from usual area")

    if data.get("rapid_transactions"):
        risk += 25
        reasons.append("Rapid successive transactions detected")

    frequency = 5 if data.get("rapid_transactions") else 2
    ml_score = get_anomaly_score(data.get("amount", 0), frequency)
    risk += ml_score

    if ml_score > 0:
        reasons.append("ML model flagged unusual behavioral pattern")

    return {
        "score": min(risk, 100),
        "reasons": reasons,
    }