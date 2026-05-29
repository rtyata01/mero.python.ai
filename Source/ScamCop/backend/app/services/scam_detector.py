from app.services.retriever import retrieve_similar_scams

def analyze_message(message: str):
    retrieved = retrieve_similar_scams(message)

    suspicious_words = [
        "urgent",
        "verify",
        "password",
        "bank",
        "click here",
        "crypto"
    ]

    score = 0

    for word in suspicious_words:
        if word.lower() in message.lower():
            score += 1

    risk = "LOW"

    if score >= 4:
        risk = "HIGH"
    elif score >= 2:
        risk = "MEDIUM"

    return {
        "risk_level": risk,
        "score": score,
        "retrieved_examples": retrieved,
        "recommendation": (
            "Do not click unknown links."
            if risk != "LOW"
            else "No major threats detected."
        )
    }
