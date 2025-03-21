import json
import random

import requests

from utils import Item

import model


def get_summary(Offer_Data):
    Messages = Offer_Data["messages"]

    prompt = "Get a conclusion out of this trade bargaining conversation. You are the NPC assistant. Get with 1 sentance the conclusion of the conversation:\n"

    prompt += "Offer: you are selling " + Offer_Data["offer"]["item"]["id"] + " for " + str(Offer_Data["offer"]["price"]) + ". (actual price: " + str(Item.get_item(Offer_Data["offer"]["item"]["id"]).price) + ")\n"

    for idx, message in enumerate(Messages):
        if idx == 0:  
            continue
        prefix = "NPC: " if idx % 2 == 0 else "Player: "
        prompt += prefix + message["content"] + "\n"
        print(prefix + message["content"])


    data = {
        # "model": "gemma3:12b",
        # "model": "llama3.2:1b",
        "model": model.model,
        "seed": random.randint(1, 10 ** 18),
        # "messages": [ ],
        "prompt": prompt,
        "keep_alive": "30m",
        "stream": False,
        # "format": json_schema,
    }

    # url = "http://192.168.100.99:11434/api/chat"  
    url = "http://127.0.0.1:11434/api/generate"
    # url = "http://192.168.100.99:11434/api/generate"

    response = requests.post(url, json=data)

    # answer = response.json().get("message", "").get("content", "")
    answer = response.json().get("response", "")

    # return json.loads(answer)
    return answer

# if __name__ == "__main__":
#
#     NPC_data, Offer_Data, Messages = parse()
#
#     accepted = False
#
#     # result, conversation, acceptet_ili_ne, oferta = get_Responce_gemma(NPC_data, Offer_Data, Messages)
#     result, conversation, offer = get_Responce_gemma(NPC_data, Offer_Data, Messages)
#
#     conversation.append({"role": "user", "content": "Accepted the offer"})
#
#     memory = get_summary(conversation, offer, accepted)
#
#     print("-------------Memory-------------")
#     print(memory)

# -- da napravim kato ofertata svurshi prosto da se dobavq suobstenie za Player: deslcine ili accept

    
"""
python Memory.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"
"""
