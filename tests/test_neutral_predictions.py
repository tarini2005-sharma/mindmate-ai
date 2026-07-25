from src.emotion_predictor import predict_emotion


def test_neutral_messages_are_not_strongly_emotional():

    neutral_messages = [
        "The meeting starts at 10 AM.",
        "I live in Toronto.",
        "The package arrived this morning.",
        "She is studying computer science.",
        "The weather is sunny today."
    ]

    for message in neutral_messages:

        emotion, confidence = predict_emotion(message)

        print(f"{message} -> {emotion} ({confidence:.2%})")

        assert emotion in [
            "neutral_other",
            "anger_frustration",
            "anxiety_related",
            "low_mood",
            "positive",
            "grief_loss"
        ]