import streamlit as st

from src.mindmate import analyze_message


st.set_page_config(
    page_title="MindMate",
    page_icon="🧠"
)


st.title("🧠 MindMate")
st.write(
    "A supportive emotion-aware companion."
)


# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# Chat input
user_text = st.chat_input(
    "How are you feeling today?"
)


if user_text:

    # Display user's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    with st.chat_message("user"):
        st.write(user_text)


    # Analyze emotion
    result = analyze_message(user_text)


    # Build MindMate response
    response = result["message"]

    response += (
        f"\n\n**Detected emotion:** "
        f"{result['emotion']}"
    )

    response += (
        f"\n\n**Confidence:** "
        f"{result['confidence']:.2%}"
    )


    if result["activities"]:

        response += "\n\n**Suggested activities:**"

        for activity in result["activities"]:

            response += f"\n- {activity}"


    # Save MindMate response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })


    # Display MindMate response
    with st.chat_message("assistant"):

        st.write(response)