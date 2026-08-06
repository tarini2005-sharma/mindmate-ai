import sqlite3


DATABASE_NAME = "mindmate.db"


# =========================================
# CREATE DATABASE
# =========================================

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    # -----------------------------------------
    # USER PROFILES TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (

            user_id TEXT PRIMARY KEY,

            occupation TEXT,

            common_emotions TEXT,

            common_triggers TEXT,

            helpful_activities TEXT,

            unhelpful_activities TEXT,

            preferred_support_style TEXT,

            profile_completed INTEGER DEFAULT 0

        )
    """)


    # -----------------------------------------
    # MOOD HISTORY TABLE
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT NOT NULL,

            emotion TEXT NOT NULL,

            confidence REAL,

            risk_level TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    connection.commit()

    connection.close()


# =========================================
# SAVE USER PROFILE
# =========================================

def save_user_profile(profile):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    cursor.execute("""
        INSERT OR REPLACE INTO user_profiles (

            user_id,

            occupation,

            common_emotions,

            common_triggers,

            helpful_activities,

            unhelpful_activities,

            preferred_support_style,

            profile_completed

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        profile.user_id,

        profile.occupation,

        ",".join(profile.common_emotions),

        ",".join(profile.common_triggers),

        ",".join(profile.helpful_activities),

        ",".join(profile.unhelpful_activities),

        profile.preferred_support_style,

        1

    ))


    connection.commit()

    connection.close()


# =========================================
# GET USER PROFILE
# =========================================

def get_user_profile(user_id):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT

            user_id,

            occupation,

            common_emotions,

            common_triggers,

            helpful_activities,

            unhelpful_activities,

            preferred_support_style,

            profile_completed

        FROM user_profiles

        WHERE user_id = ?

    """, (user_id,))


    row = cursor.fetchone()

    connection.close()


    if row is None:

        return None


    return {

        "user_id": row[0],

        "occupation": row[1],

        "common_emotions": (
            row[2].split(",")
            if row[2]
            else []
        ),

        "common_triggers": (
            row[3].split(",")
            if row[3]
            else []
        ),

        "helpful_activities": (
            row[4].split(",")
            if row[4]
            else []
        ),

        "unhelpful_activities": (
            row[5].split(",")
            if row[5]
            else []
        ),

        "preferred_support_style": row[6],

        "profile_completed": bool(row[7])

    }


# =========================================
# SAVE MOOD HISTORY
# =========================================

def save_mood_history(

    user_id,

    emotion,

    confidence,

    risk_level

):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO mood_history (

            user_id,

            emotion,

            confidence,

            risk_level

        )

        VALUES (?, ?, ?, ?)

    """, (

        user_id,

        emotion,

        confidence,

        risk_level

    ))


    connection.commit()

    connection.close()


# =========================================
# GET MOOD HISTORY
# =========================================

def get_mood_history(user_id):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT

            emotion,

            confidence,

            risk_level,

            created_at

        FROM mood_history

        WHERE user_id = ?

        ORDER BY created_at DESC

    """, (user_id,))


    rows = cursor.fetchall()

    connection.close()


    return [

        {

            "emotion": row[0],

            "confidence": row[1],

            "risk_level": row[2],

            "created_at": row[3]

        }

        for row in rows

    ]


# =========================================
# RUN DATABASE CREATION
# =========================================

if __name__ == "__main__":

    create_database()

    print("Database created successfully.")
def get_weekly_mood_trend(user_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE(created_at) AS mood_date,
            emotion,
            COUNT(*) AS count
        FROM mood_history
        WHERE user_id = ?
        AND created_at >= DATE('now', '-7 days')
        GROUP BY mood_date, emotion
        ORDER BY mood_date ASC
    """, (user_id,))

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "date": row[0],
            "emotion": row[1],
            "count": row[2]
        }
        for row in rows
    ]
def get_mood_summary(user_id):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT emotion, COUNT(*)
        FROM mood_history
        WHERE user_id = ?
        AND created_at >= DATE('now', '-7 days')
        GROUP BY emotion
        ORDER BY COUNT(*) DESC
    """, (user_id,))

    emotion_rows = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*)
        FROM mood_history
        WHERE user_id = ?
        AND created_at >= DATE('now', '-7 days')
    """, (user_id,))

    total_checkins = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM mood_history
        WHERE user_id = ?
        AND risk_level = 'high'
        AND created_at >= DATE('now', '-7 days')
    """, (user_id,))

    high_risk_events = cursor.fetchone()[0]

    connection.close()

    most_common_emotion = (
        emotion_rows[0][0]
        if emotion_rows
        else None
    )

    return {
        "most_common_emotion": most_common_emotion,
        "total_checkins": total_checkins,
        "high_risk_events": high_risk_events,
        "emotion_breakdown": [
            {
                "emotion": row[0],
                "count": row[1]
            }
            for row in emotion_rows
        ]
    }