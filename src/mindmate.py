from src.emotion_predictor import predict_emotion
from src.recommendation_engine import get_recommendation
from src.safety_layer import check_safety
CONFIDENCE_THRESHOLD = 0.50


def analyze_message(text):
    """
    Analyze a user's message and return
    an emotion and supportive recommendation.
    """
    safety_result = check_safety(text)

    if safety_result["risk_detected"]:
        return {
        "text": text,
        "emotion": "high_risk",
        "confidence": 1.0,
        "safety": safety_result,
        "message": (
            "I'm really sorry you're going through this. "
            "You deserve immediate support. Please reach out to "
            "someone you trust or a local emergency or crisis "
            "support service right now."
        ),
        "activities": []
    }

    emotion, confidence = predict_emotion(text)

    confidence_threshold = CONFIDENCE_THRESHOLD

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