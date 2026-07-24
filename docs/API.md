# MindMate API

## Analyze Emotion

### Endpoint

POST `/analyze`

### Request

```json
{
  "text": "I feel really anxious about tomorrow.",
  "emotion": "anxiety_related",
  "confidence": 0.47179123048376337,
  "message": "It sounds like you may be feeling worried or anxious. A short breathing or grounding exercise may help.",
  "activities": [
    "Try slow breathing for 2 minutes",
    "Name 5 things you can see around you",
    "Write down what is worrying you"
  ]
}