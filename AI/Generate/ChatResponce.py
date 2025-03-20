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

def get_Responce(NPC_data, Offer_Data, Messages):

    Messages["messages"].insert(0, {"role": "system", "content": ""})

    Messages["messages"][0]["content"] = (
        "You are an NPC in a videogame about trading and you are negotiating with the player. "
        "You are selling a " + Offer_Data["item"]["name"] +
        # " to " + NPC_data["name"] +
        " to the player " +
        " for " + str(Offer_Data["price"]) +
        " - the actual price of the " + Offer_Data["item"]["name"] +
        " is " + str(Offer_Data["item"]["price"]) + ", which is unknown to the player. "
        "This is the info for you:\n" + NPC_data["info"] + "\n"
        "This is your personal description: " + NPC_data["description"] + "\n\n"
        "These are your attributes as NPC that should be followed:\n"
    )

    for attribute, value in NPC_data["attributes"].items():
        Messages["messages"][0]["content"] += f"{attribute}: {value}\n"

    Messages["messages"][0]["content"] += (
        # "\n**Be short with your answer as the NPC. After your answer, append a endl for final line that contains just the final price for clarity.**"
        # "\n**Be short with your answer to the user. If this is your final answer of the negotiation, tell your \"Final Price\", and if not ask a question.**"
        # "\n**If this is your final answer of the negotiation, say your \"Final Price\" as a number, and if not ask a question.**"
        "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"
    )

    # For debugging, you might print the prompt to check it
    print(Messages["messages"][0]["content"])    # Messages["messages"][0]["content"] = (
    #     f"You are an NPC in a videogame about trading and you are negotiating with the player. "
    #     f"You are selling a {Offer_Data['item']['name']} to {NPC_data['name']} for {Offer_Data['price']} "
    #     f"- the actual price of the {Offer_Data['item']['name']} {Offer_Data['item']['price']}, "
    #     "which is unknown to the player."
    # )

    json_schema = {
        "type": "object",
        "properties": {
            # "sentance": {"type": "string"},
            "answer_to_player": {"type": "string"},
            "is_final": {"type": "boolean"},
            "price": {"type": "integer"},
        },
        # "required": ["sentance", "is_final", "price"],
        "required": ["answer_to_player", "is_final", "price"],
    }



    data = {
        # "model": "llama3.2:1b",
        "model": "deepseek-r1:14b",
        # "model": "deepseek-r1:7b",
        # "prompt": question,
        "seed": random.randint(0, 10000),
        "messages": [
            # {"role": "user", "content": question}
        ],
        "keep_alive": "30m",
        "stream": False,
        # "format": json_schema,
    }

    for message in Messages["messages"]:
        data["messages"].append(message)

    # url  = "http://localhost:11434/api/generate"
    # url = "http://localhost:11434/api/chat"  # important
    url = "http://192.168.100.99:11434/api/chat"  # important

    response = requests.post(url, json=data)

    # answer = ""
    # for line in response.text.strip().split("\n"):
    #     if line:
    #         part = json.loads(line)
    #         # content = part.get("response", {})
    #         content = part.get("message", {}).get("content", "")
    #         answer += content
    #
    #         # removfe the last line

    answer = response.json().get("message", "").get("content", "")
    # answer = response.json().get("response", "")

    print("---------------")
    print(answer)
    print(response)
    print("---------------")
    # print(response.json())

    lines = answer.splitlines()

    try:
        end_think_index = lines.index("</think>")
    except ValueError:
        raise ValueError("The closing </think> tag was not found in the response.")

    # extracted_lines = lines[end_think_index + 1 : -1]
    extracted_lines = lines[end_think_index + 1]

    result = "\n".join(line.strip() for line in extracted_lines if line.strip())

    print(result)
    print("--------------")

    final_price = answer.split()[-1]
    # skipp everything from start to finding "$"
    final_price = final_price[final_price.find("$"):]
    print(final_price)

    return result, final_price



if __name__ == "__main__":

    NPC_data, Offer_Data, Messages = parse()

    result, final_price = get_Responce(NPC_data, Offer_Data, Messages)

    if final_price!="":
        # TOVA ZNAI4AVA CHE E KRAIA NA NEGOCIACIQTA
        pass



    
"""
python ChatResponce.py "{\"name\": \"Gosho\"}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"


python ChatResponce.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"
"""
