from src.mindmate import analyze_message


def test_anxiety_message():
    result = analyze_message(
        "I feel really worried and anxious about my future."
    )

    assert result["emotion"] == "anxiety_related"
    assert result["confidence"] >= 0.60


def test_positive_message():
    result = analyze_message(
        "I am so happy and excited today!"
    )

    assert result["emotion"] == "positive"


def test_low_mood_message():
    result = analyze_message(
        "I have been feeling very sad and low lately."
    )

    assert result["emotion"] == "low_mood"


def test_uncertain_message():
    result = analyze_message(
        "The meeting is scheduled for tomorrow."
    )

    assert result["emotion"] == "uncertain"


def test_empty_message():
    try:
        analyze_message("")
        assert False
    except ValueError:
        assert True