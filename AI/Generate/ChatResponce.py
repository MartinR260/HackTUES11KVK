#!rule {"name":,"info":,"description":,}
import json
import random
import model
# import sys

import requests

import api.offers as offers

# def parse():
#     if len(sys.argv) != 4:
#         print("Usage: python ChatResponce.py <json1> <json2> <json3>")
#         sys.exit(1)
#
#     try:
#         json1 = json.loads(sys.argv[1])
#         json2 = json.loads(sys.argv[2])
#         json3 = json.loads(sys.argv[3])
#     except json.JSONDecodeError as e:
#         print("Error decoding JSON:", e)
#         sys.exit(1)
#
#     return json1, json2, json3

def get_Responce_gemma(offer):
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
        "model": model.model,
        # "model": "gemma3:12b",
        # "seed": random.randint(1, 10 ** 18),
        "messages": offer["messages"],
        "keep_alive": "30m",
        "stream": False,
        "format": json_schema,
        "options": {
            "temperature":offer["npc"]["temperature"],
            "seed": random.randint(1, 100),
        },
    }

    # url = "http://192.168.100.99:11434/api/chat"
    url = "http://localhost:11434/api/chat"
    response = requests.post(url, json=data)
    answer = response.json().get("message", "").get("content", "")
    result = json.loads(answer)

    # conversation = Messages["messages"]
    # conversation.append({"role": "assistant", "content": result["answer_to_player"]})


    # return result, conversation, Offer_Data
    # return result, conversation
    return result



# if __name__ == "__main__":
#
#     NPC_data, Offer_Data, Messages = parse()
#
#     result = get_Responce_gemma(NPC_data, Offer_Data, Messages)
#
#     # print(result)
#
#
#
# """
# python ChatResponce.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Co'on man cant we do 900?\" }]}"
#
# python ChatResponce.py "{\"image_id\": null, \"name\": \"Bradley Jenkins\", \"info\": \"Lives in Boston. Works as a teacher in middle school\", \"description\": \"You like to think logically and in the long term\", \"temperature\": 0.987018549049676, \"attributes\": {\"deceitful\": \"high\", \"personality\": \"hostile\", \"naivety\": \"high\", \"talking_style\": \"informal\"}, \"memories\": []}" "{\"item\": {\"name\": \"Lada\", \"price\": \"$1000\"}, \"description\": \"Old but gold\", \"price\": \"$1500\"}" "{\"messages\": [ { \"role\": \"user\", \"content\": \"Can you sell me this for half the price if i give you a old watch\" }, { \"role\": \"assistant\", \"content\": \"I dont need old watches\" }, { \"role\": \"user\", \"content\": \"Ok how about getting 10% off for me this time but i contact you again if need more\" }]}"
# """
