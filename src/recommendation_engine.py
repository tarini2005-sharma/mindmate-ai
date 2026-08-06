# src/recommendation_engine.py


def get_recommendation(emotion):
    """
    Default recommendations for users without personalization.
    """

    recommendations = {
        "anxiety_related": [
            {
                "activity": "Try slow breathing for 2 minutes",
                "score": 0.75,
                "reason": "Breathing exercises are commonly used to reduce immediate anxiety symptoms."
            },
            {
                "activity": "Name 5 things you can see around you",
                "score": 0.70,
                "reason": "Grounding can help redirect attention away from anxious thoughts."
            },
            {
                "activity": "Write down what is worrying you",
                "score": 0.60,
                "reason": "Writing can help organise and externalise worrying thoughts."
            }
        ],

        "stress": [
            {
                "activity": "Take a short walk",
                "score": 0.75,
                "reason": "Light physical activity can be a useful stress-management strategy."
            },
            {
                "activity": "Listen to calming music",
                "score": 0.70,
                "reason": "Music can help some users relax during stressful moments."
            },
            {
                "activity": "Take slow deep breaths",
                "score": 0.65,
                "reason": "Slow breathing may help reduce immediate physical stress symptoms."
            }
        ],

        "sadness": [
            {
                "activity": "Talk to someone you trust",
                "score": 0.80,
                "reason": "Social support can help reduce feelings of isolation."
            },
            {
                "activity": "Listen to music",
                "score": 0.65,
                "reason": "Music may help users process or regulate difficult emotions."
            }
        ],

        "anger": [
            {
                "activity": "Take a short break before reacting",
                "score": 0.80,
                "reason": "A brief pause can create space for emotional regulation."
            },
            {
                "activity": "Take a walk",
                "score": 0.70,
                "reason": "Physical movement may help release tension."
            }
        ]
    }

    return recommendations.get(
        emotion,
        [
            {
                "activity": "Take a few slow breaths",
                "score": 0.50,
                "reason": "Slow breathing is a general low-risk coping strategy."
            }
        ]
    )


def get_personalized_recommendations(emotion, profile):
    """
    Personalizes recommendations using the user's profile.

    Strategy:
    1. Start with emotion-based default recommendations.
    2. Remove activities marked as unhelpful.
    3. Boost activities marked as helpful.
    4. Add helpful user activities if they are relevant to the emotion.
    5. Return scores and explainability reasons.
    """

    default_recommendations = get_recommendation(emotion)

    helpful_activities = [
        activity.lower()
        for activity in profile.get("helpful_activities", [])
    ]

    unhelpful_activities = [
        activity.lower()
        for activity in profile.get("unhelpful_activities", [])
    ]

    personalized = []

    # -----------------------------------
    # Step 1: Process default recommendations
    # -----------------------------------

    for recommendation in default_recommendations:

        activity_name = recommendation["activity"]
        activity_lower = activity_name.lower()

        # Remove activities marked as unhelpful
        if any(
            unhelpful in activity_lower
            or activity_lower in unhelpful
            for unhelpful in unhelpful_activities
        ):
            continue

        score = recommendation["score"]

        reason = recommendation["reason"]

        # Boost activities previously marked helpful
        if any(
            helpful in activity_lower
            or activity_lower in helpful
            for helpful in helpful_activities
        ):
            score = min(score + 0.15, 1.0)

            reason = (
                f"{activity_name} was prioritised because it was previously "
                f"identified as helpful for this user."
            )

        personalized.append({
            "activity": activity_name,
            "score": round(score, 2),
            "reason": reason
        })

    # -----------------------------------
    # Step 2: Add user-specific activities
    # -----------------------------------

    emotion_activity_map = {

        "anxiety_related": [
            "music",
            "walking",
            "breathing",
            "grounding",
            "journaling"
        ],

        "stress": [
            "music",
            "walking",
            "exercise",
            "breathing"
        ],

        "sadness": [
            "music",
            "walking",
            "talking",
            "socialising"
        ],

        "anger": [
            "walking",
            "exercise",
            "breathing"
        ]
    }

    relevant_activities = emotion_activity_map.get(
        emotion,
        []
    )

    for helpful_activity in helpful_activities:

        if helpful_activity not in relevant_activities:
            continue

        already_added = any(
            helpful_activity in recommendation["activity"].lower()
            for recommendation in personalized
        )

        if already_added:
            continue

        personalized.append({
            "activity": helpful_activity.title(),
            "score": 0.86,
            "reason": (
                f"{helpful_activity.title()} was recommended because it is "
                f"both relevant to {emotion.replace('_', ' ')} and previously "
                f"identified as helpful for this user."
            )
        })

    # -----------------------------------
    # Step 3: Sort recommendations
    # -----------------------------------

    personalized.sort(
        key=lambda recommendation: recommendation["score"],
        reverse=True
    )

    return personalized