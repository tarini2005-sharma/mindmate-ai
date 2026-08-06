# src/safety_layer.py


HIGH_RISK_PATTERNS = [
    "kill myself",
    "suicide",
    "end my life",
    "take my own life",
    "want to die",
    "don't want to live",
    "do not want to live",
    "hurt myself",
    "harm myself",
    "self harm",
    "self-harm",
]


def check_safety(text: str) -> dict:

    text_lower = text.lower().strip()

    matched_patterns = []

    for pattern in HIGH_RISK_PATTERNS:

        if pattern in text_lower:

            matched_patterns.append(pattern)

    if matched_patterns:

        return {
            "risk_detected": True,
            "risk_level": "high",
            "matched_patterns": matched_patterns
        }

    return {
        "risk_detected": False,
        "risk_level": "low",
        "matched_patterns": []
    }
