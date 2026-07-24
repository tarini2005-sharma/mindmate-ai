from mindmate import analyze_message


def start_chat():

    print("=" * 60)
    print("Welcome to MindMate")
    print("Type 'quit' to end the conversation.")
    print("=" * 60)

    while True:

        user_text = input("\nYou: ")

        if user_text.lower() == "quit":
            print("\nMindMate: Take care of yourself. Goodbye!")
            break

        try:
            result = analyze_message(user_text)

            print("\nMindMate:")
            print(result["message"])

            print(
                f"\nDetected emotion: {result['emotion']}"
            )

            print(
                f"Confidence: {result['confidence']:.2%}"
            )

            if result["activities"]:

                print("\nSuggested activities:")

                for activity in result["activities"]:
                    print("-", activity)

        except ValueError as error:

            print(f"\nError: {error}")


if __name__ == "__main__":
    start_chat()