from flask import request, jsonify

from Generate.ChatResponce import get_Responce_gemma
from api.api import app
import api.offers as offers
from utils import Item


@app.route('/api/chat', methods=['POST'])
def chat():
    if len(offers.active_offer["messages"]) == 0:
        message = {"role": "system", "content": (
                "You are an NPC in a videogame about trading and you are negotiating with the player. "
                "You are selling a " + offers.active_offer["offer"]["item"]["id"] +
                # " to " + offers.active_offer["npc"]["name"] +
                " to the player " +
                " for " + str(offers.active_offer["offer"]["price"]) +
                " - the actual price of the " + offers.active_offer["offer"]["item"]["id"] +
                " is " + str(Item.get_item(offers.active_offer["offer"]["item"]["id"]).price) + ", which is unknown to the player. "
                                                                              "This is the info for you:\n" +
                offers.active_offer["npc"]["info"] + "\nThis is your personal description: " +
                offers.active_offer["npc"]["description"] + "\n\nThese are your attributes as NPC that should be followed:\n"
        )}

        for attribute, value in offers.active_offer["npc"]["attributes"].items():
            message["content"] += f"{attribute}: {value}\n"

        message["content"] += (
            "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"
        )

        offers.active_offer["messages"].append(message)

    message = request.get_json().get('message')
    offers.active_offer["messages"].append({"role": "user", "content": message})


    result = get_Responce_gemma()

    offers.active_offer["messages"].append({"role": "npc", "content": result["answer_to_player"]})

    return jsonify({"response": result})

