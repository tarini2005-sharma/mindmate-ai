CRISIS_PATTERNS = [
    "kill myself",
    "killing myself",
    "suicide",
    "want to die",
    "wanna die",
    "end my life",
    "ending my life",
    "take my own life",
    "hurt myself",
    "harm myself",
    "self harm",
    "self-harm",
    "don't want to live",
    "do not want to live",
    "no reason to live",
]


def check_safety(text):
    """
    Basic crisis-language check.

    Returns a dictionary describing whether
    potentially high-risk language was detected.
    """

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    normalized_text = text.lower().strip()

    for pattern in CRISIS_PATTERNS:
        if pattern in normalized_text:
            return {
                "risk_detected": True,
                "risk_level": "high",
            }

    return {
        "risk_detected": False,
        "risk_level": "low",
    }