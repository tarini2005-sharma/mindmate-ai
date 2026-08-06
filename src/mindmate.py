from src.emotion_predictor import predict_emotion
from src.recommendation_engine import get_recommendation


def analyze_message(text):

    emotion_result = predict_emotion(text)

    # predict_emotion returns:
    # emotion, confidence
    emotion, confidence = emotion_result

    activities = get_recommendation(emotion)

    return {
        "text": text,
        "emotion": emotion,
        "confidence": confidence,
        "message": (
            "It sounds like you may be feeling worried or anxious. "
            "A short breathing or grounding exercise may help."
        ),
        "activities": activities
    }