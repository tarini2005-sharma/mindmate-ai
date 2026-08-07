from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.mindmate import analyze_message
from src.safety_layer import check_safety
from fastapi.middleware.cors import CORSMiddleware

from src.recommendation_engine import (
    get_personalized_recommendations
)

from backend.database import (
    save_user_profile,
    get_user_profile,
    save_mood_history,
    get_mood_history,
    create_database
)


# =========================================
# FASTAPI APPLICATION
# =========================================

app = FastAPI(
    title="MindMate API",
    description="API for emotion detection and personalised emotional support",
    version="1.0.0"
)
create_database()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# REQUEST MODELS
# =========================================


class AnalyzeRequest(BaseModel):

    text: str


class PersonalizedAnalyzeRequest(BaseModel):

    user_id: str
    text: str


class UserProfileRequest(BaseModel):

    user_id: str

    occupation: str | None = None

    common_emotions: list[str] = []

    common_triggers: list[str] = []

    helpful_activities: list[str] = []

    unhelpful_activities: list[str] = []

    preferred_support_style: str | None = None


# =========================================
# HOME ENDPOINT
# =========================================


@app.get("/")
def home():

    return {
        "message": "MindMate API is running"
    }


# =========================================
# BASIC ANALYSIS ENDPOINT
# =========================================


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    # -----------------------------
    # Validate input
    # -----------------------------

    if not request.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty."
        )


    # -----------------------------
    # HARD SAFETY GATE
    # -----------------------------

    safety_result = check_safety(request.text)


    # -----------------------------
    # If risk detected:
    # STOP EVERYTHING
    # -----------------------------

    if safety_result["risk_detected"]:

        return {

            "text": request.text,

            "safety": safety_result,

            "message": (
                "I'm really sorry that you're going through this. "
                "You deserve immediate support. Please contact a trusted "
                "person near you or a local emergency or crisis support "
                "service right now."
            ),

            "next_step": (
                "If you are in immediate danger, contact your local "
                "emergency services immediately."
            )

        }


    # -----------------------------
    # Emotion analysis
    # -----------------------------

    emotion_result = analyze_message(
        request.text
    )


    # -----------------------------
    # Save mood history
    # -----------------------------

    save_mood_history(

        user_id="anonymous",

        emotion=emotion_result["emotion"],

        confidence=emotion_result["confidence"],

        risk_level=safety_result["risk_level"]

    )


    # -----------------------------
    # Return result
    # -----------------------------

    return {

        "text": request.text,

        "safety": safety_result,

        "analysis": emotion_result

    }
from backend.database import (
    save_user_profile,
    get_user_profile,
    save_mood_history,
    get_mood_history,
    get_weekly_mood_trend
)
from backend.database import (
    save_user_profile,
    get_user_profile,
    save_mood_history,
    get_mood_history,
    get_weekly_mood_trend,
    get_mood_summary
)

# =========================================
# PERSONALIZED ANALYSIS ENDPOINT
# =========================================


@app.post("/personalized-analyze")
def personalized_analyze(
    request: PersonalizedAnalyzeRequest
):

    # -----------------------------
    # Validate input
    # -----------------------------

    if not request.text.strip():

        raise HTTPException(

            status_code=400,

            detail="Text cannot be empty."

        )


    # -----------------------------
    # HARD SAFETY GATE
    # -----------------------------

    safety_result = check_safety(

        request.text

    )


    # -----------------------------
    # HIGH-RISK SHORT CIRCUIT
    # -----------------------------

    if safety_result["risk_detected"]:

        return {

            "user_id": request.user_id,

            "safety": safety_result,

            "message": (

                "I'm really sorry that you're going through this. "
                "You deserve immediate support. Please contact a trusted "
                "person near you or a local emergency or crisis support "
                "service right now."
            ),

            "next_step": (

                "If you are in immediate danger, contact your local "
                "emergency services immediately."

            )

        }


    # -----------------------------
    # Load user profile
    # -----------------------------

    profile = get_user_profile(

        request.user_id

    )


    # -----------------------------
    # COLD-START STRATEGY
    # -----------------------------

    is_new_user = profile is None


    if profile is None:

        profile = {

            "user_id": request.user_id,

            "occupation": None,

            "common_emotions": [],

            "common_triggers": [],

            "helpful_activities": [],

            "unhelpful_activities": [],

            "preferred_support_style": None,

            "profile_completed": False

        }


    # -----------------------------
    # Emotion analysis
    # -----------------------------

    emotion_result = analyze_message(

        request.text

    )


    # -----------------------------
    # Save mood history
    # -----------------------------

    save_mood_history(

        user_id=request.user_id,

        emotion=emotion_result["emotion"],

        confidence=emotion_result["confidence"],

        risk_level=safety_result["risk_level"]

    )


    # -----------------------------
    # Personalised recommendations
    # -----------------------------

    personalized_activities = (

        get_personalized_recommendations(

            emotion=emotion_result["emotion"],

            profile=profile

        )

    )


    # Add recommendations
    # to emotion analysis result

    emotion_result["activities"] = (

        personalized_activities

    )


    # -----------------------------
    # Return complete response
    # -----------------------------

    return {

        "user_id": request.user_id,

        "is_new_user": is_new_user,

        "profile": profile,

        "safety": safety_result,

        "analysis": emotion_result

    }


# =========================================
# CREATE OR UPDATE USER PROFILE
# =========================================


@app.post("/profile")
def create_profile(

    profile: UserProfileRequest

):

    save_user_profile(

        profile

    )


    return {

        "message": "Profile saved successfully",

        "profile": profile.model_dump()

    }


# =========================================
# GET USER PROFILE
# =========================================


@app.get("/profile/{user_id}")
def read_profile(

    user_id: str

):

    profile = get_user_profile(

        user_id

    )


    if profile is None:

        raise HTTPException(

            status_code=404,

            detail="Profile not found."

        )


    return {

        "message": "Profile found successfully",

        "profile": profile

    }


# =========================================
# GET MOOD HISTORY
# =========================================


@app.get("/mood-history/{user_id}")
def read_mood_history(

    user_id: str

):

    history = get_mood_history(

        user_id

    )


    return {

        "user_id": user_id,

        "history": history

    }
@app.get("/mood-trend/{user_id}")
def mood_trend(user_id: str):

    trend = get_weekly_mood_trend(user_id)

    return {
        "user_id": user_id,
        "period": "last_7_days",
        "trend": trend
    }
@app.get("/mood-summary/{user_id}")
def mood_summary(user_id: str):

    summary = get_mood_summary(user_id)

    return {
        "user_id": user_id,
        "period": "last_7_days",
        "summary": summary
    }