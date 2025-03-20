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

    Messages["messages"].insert(0, {"role": "system", "content": ""})

    Messages["messages"][0]["content"] = (
        "You are an NPC in a videogame about trading and you are negotiating with the player."
        + " You are selling a "
        + Offer_Data["item"]["name"]
        + " to "
        + NPC_data["name"]
        + " for"
        + Offer_Data["price"]
        + " - the actual price of the"
        + Offer_Data["item"]["name"]
        + " "
        + Offer_Data["item"]["price"]
        + ", which is unknown to the player. Be short with your answer as the npc. After your answer append last line that should be the final price - nothing else just the price."
    )

    # Messages["messages"][0]["content"] = (
    #     f"You are an NPC in a videogame about trading and you are negotiating with the player. "
    #     f"You are selling a {Offer_Data['item']['name']} to {NPC_data['name']} for {Offer_Data['price']} "
    #     f"- the actual price of the {Offer_Data['item']['name']} {Offer_Data['item']['price']}, "
    #     "which is unknown to the player."
    # )

    data = {
        # "model": "llama3.2:1b",
        "model": "deepseek-r1:14b",
        # "prompt": question,
        "seed": random.randint(0, 10000),
        "messages": [
            # {"role": "user", "content": question}
        ],
        "keep_alive": "30m",
        "steal": False,
    }

    for message in Messages["messages"]:
        data["messages"].append(message)

    # url  = "http://localhost:11434/api/generate"
    # url = "http://localhost:11434/api/chat"  # important
    url = "http://192.168.100.99:11434/api/chat"  # important

    response = requests.post(url, json=data)

    answer = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            # content = part.get("response", {})
            content = part.get("message", {}).get("content", "")
            answer += content

            # removfe the last line

    print(answer)
    print("---------------")

    lines = answer.splitlines()

    try:
        end_think_index = lines.index('</think>')
    except ValueError:
        raise ValueError("The closing </think> tag was not found in the response.")

    extracted_lines = lines[end_think_index + 1:-1]

    result = "\n".join(line.strip() for line in extracted_lines if line.strip())

    print(result)
    print("--------------")


    final_price = answer.split()[-1]
    print(final_price)


"""
python ChatResponce.py "{\"name\": \"Gosho\"}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1000\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"
"""
