import os
import joblib


# Find the project root directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Path to the trained emotion classification model
MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "emotion_classifier.pkl"
)


# Load the trained model
model = joblib.load(MODEL_PATH)


def predict_emotion(text):
    """
    Predict the emotional category and confidence score.
    """

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    if not text.strip():
        raise ValueError("Input text cannot be empty.")

    probabilities = model.predict_proba([text])[0]

    best_index = probabilities.argmax()

    emotion = model.classes_[best_index]

    confidence = probabilities[best_index]

    return emotion, confidence


if __name__ == "__main__":

    test_text = (
        "I feel really worried about my future."
    )

    emotion, confidence = predict_emotion(test_text)

    print("Input:", test_text)
    print("Predicted emotion:", emotion)
    print(f"Confidence: {confidence:.2%}")