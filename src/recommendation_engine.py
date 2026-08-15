RECOMMENDATIONS = {
    "anxiety_related": {
        "message": (
            "It sounds like you may be feeling worried or anxious. "
            "A short breathing or grounding exercise may help."
        ),
        "activities": [
            "Try slow breathing for 2 minutes",
            "Name 5 things you can see around you",
            "Write down what is worrying you"
        ]
    },

    "low_mood": {
        "message": (
            "It sounds like you may be experiencing a low mood. "
            "Be gentle with yourself today."
        ),
        "activities": [
            "Take a short walk",
            "Listen to music you enjoy",
            "Write down how you are feeling"
        ]
    },
    "grief_loss": {
        "message": (
            "It sounds like you may be going through a difficult experience "
            "of loss or grief. Be gentle with yourself and take things one "
            "moment at a time."
    ),
        "activities": [
            "Talk to someone you trust about how you are feeling",
            "Write down what you are missing or thinking about",
            "Take a quiet walk or spend some time in a comforting place"
        ]   
    },

    "anger_frustration": {
        "message": (
            "It sounds like something may be frustrating or upsetting you. "
            "Taking a short pause may help before responding."
        ),
        "activities": [
            "Take 10 slow breaths",
            "Step away for a few minutes",
            "Write down what triggered the frustration"
        ]
    },

    "positive": {
        "message": (
            "It sounds like you are experiencing a positive emotion. "
            "That is great — taking a moment to appreciate it can be valuable."
        ),
        "activities": [
            "Write down what made you feel good",
            "Share your positive moment with someone",
            "Take a moment to appreciate how you feel"
        ]
    },

    "neutral_other": {
        "message": (
            "Thanks for sharing. I don't detect a strong emotional signal "
            "in this message."
        ),
        "activities": [
            "Tell me more about how you are feeling",
            "Describe what is on your mind",
            "Take a moment to check in with yourself"
        ]
    }
}


def get_recommendation(emotion):
    """
    Return a supportive recommendation based on the detected emotion.
    """

    return RECOMMENDATIONS.get(
        emotion,
        RECOMMENDATIONS["neutral_other"]
    )


if __name__ == "__main__":

    result = get_recommendation("anxiety_related")

    print(result["message"])
    print("\nSuggested activities:")

    for activity in result["activities"]:
        print("-", activity)