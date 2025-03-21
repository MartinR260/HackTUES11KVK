#!rule {"name":,"info":,"description":,}
import json
import random
import sys
import re

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

def get_Responce_gemma(NPC_data, Offer_Data, Messages):

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
        "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"
    )

    print(Messages["messages"][0]["content"])    

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
        "model": "gemma3:12b",
        "seed": random.randint(1, 10 ** 18),
        "messages": [ ],
        "keep_alive": "30m",
        "stream": False,
        "format": json_schema,
    }

    for message in Messages["messages"]:
        data["messages"].append(message)

    url = "http://192.168.100.99:11434/api/chat"  

    response = requests.post(url, json=data)

    answer = response.json().get("message", "").get("content", "")

    result = answer

    # print(result)
    # print("--------------")
    #
    # final_price = answer.split()[-1]
    # final_price = "".join(re.findall(r'\d', final_price))
    #
    # print(final_price)

    return result 



if __name__ == "__main__":

    NPC_data, Offer_Data, Messages = parse()

    result = get_Responce_gemma(NPC_data, Offer_Data, Messages)

    print(result)


    
"""
python ChatResponce.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Co'on man cant we do 900?\" }]}"

python ChatResponce.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"
"""
