from src.emotion_predictor import predict_emotion
from src.recommendation_engine import get_recommendation


def analyze_message(text):
    """
    Analyze a user's message and return
    an emotion and supportive recommendation.
    """

    emotion, confidence = predict_emotion(text)

    confidence_threshold = 0.40

    if confidence < confidence_threshold:
        return {
            "text": text,
            "emotion": "uncertain",
            "confidence": confidence,
            "message": (
                "I'm not completely sure how you're feeling "
                "from that message. Could you tell me a little more?"
            ),
            "activities": []
        }

    recommendation = get_recommendation(emotion)

    return {
        "text": text,
        "emotion": emotion,
        "confidence": confidence,
        "message": recommendation["message"],
        "activities": recommendation["activities"]
    }


if __name__ == "__main__":

    user_text = input("How are you feeling today? ")

    result = analyze_message(user_text)

    print("\nDetected emotion:", result["emotion"])
    print(f"Confidence: {result['confidence']:.2%}")

    print("\nMindMate:")
    print(result["message"])

    if result["activities"]:
        print("\nSuggested activities:")

        for activity in result["activities"]:
            print("-", activity)