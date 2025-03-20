#!rule {"name":,"info":,"description":,}
import json
import random
import sys

import requests


def parse():
    if len(sys.argv) != 4:
        print("Usage: python ChatResponce.py <json1> <json2> <json3>")
        sys.exit(1)

    try:
        json1 = json.loads(sys.argv[1])
        json2 = json.loads(sys.argv[2])
        json3 = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        sys.exit(1)

    return json1, json2, json3


if __name__ == "__main__":

    NPC_data, Offer_Data, Messages = parse()

    Messages["messages"].insert(0, {"role": "OBJECTIVE", "content": ""})
    Messages["messages"][0]["content"] = "You are an NPC in a videogame about trading."

    print(Messages)

    data = {
        "model": "llama3.2:1b",
        # "prompt": question,
        # "seed": random.randint(0, 10000),
        "messages": [
            # {"role": "user", "content": question}
        ],
        # "keep_alive": "30m",
    }

    print("-------------------1")
    for message in Messages["messages"]:
        data["messages"].append(message)
    print("-------------------2")

    # url  = "http://localhost:11434/api/generate"
    url = "http://localhost:11434/api/chat"  # important

    response = requests.post(url, json=data)

    print("-------------------3")
    print(response.text)
    print("-------------------4")

    answer = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            # content = part.get("response", {})
            content = part.get("message", {}).get("content", "")
            answer += content

    print(answer)
    print("-------------------")


# python ChatResponce.py "{\"name\": \"Gosho\"}" "{\"product\": \"banana\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"why is the sky blue?\" }, { \"role\": \"assistant\", \"content\": \"due to rayleigh scattering.\" }, { \"role\": \"user\", \"content\": \"how is that different than mie scattering?\" }]}"
