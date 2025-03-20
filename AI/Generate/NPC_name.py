import json
import requests

if __name__ == "__main__":
    number_of_questions = 3
    conversation_history = []  # This will store all the messages

    for _ in range(number_of_questions):
        # Get the user's input and add it to the conversation history
        question = input("Llama: ")
        conversation_history.append({"role": "user", "content": question})
        
        data = {
            "model": "llama3.2:1b",
            "messages": conversation_history,
            "steal": False,  # Retained from your original code
        }
        # url = "http://localhost:11434/api/chat"
        url = "http://127.0.0.1:11434/api/chat"

        response = requests.post(url, json=data)

        full_reply = ""
        for line in response.text.strip().split("\n"):
            if line:
                part = json.loads(line)
                # Extract the reply content from the assistant's message
                content = part.get("message", {}).get("content", "")
                full_reply += content

        # Print and add the assistant's reply to the conversation history
        print("AI Reply:", full_reply)
        conversation_history.append({"role": "assistant", "content": full_reply})

