from flask import request, jsonify

from Generate.ChatResponce import get_Responce_gemma
from api.api import app
import api.offers as offers
from baza.item import get_item


@app.route('/api/chat', methods=['POST'])
def chat():
    if len(offers.active_offer["messages"]) == 0:
        npc_first = False
        message = {
            "role": "system",
            "content": (
                    "You are an NPC in a videogame about trading and you are negotiating with the player. "
                    "You are selling a " + offers.active_offer["offer"]["item_id"] +
                    # " to " + offers.active_offer["npc"]["name"] +
                    " to the player "
                    + " for "
                    + str(offers.active_offer["offer"]["price"])
                    + " - the actual price of the "
                    + offers.active_offer["offer"]["item_id"]
                    + " is "
                    + str(get_item(offers.active_offer["offer"]["item_id"])["price"])
                    + ", which is unknown to the player. "
                    + offers.active_offer["npc"]["info"]
                    + "\nThis is your personal description: "
                    + offers.active_offer["npc"]["description"]
                    + "\n\nThese are your attributes as NPC that should be followed:\n"
            ),
        }

        if npc_first:
            message["content"] = (
                    "You are an NPC in a videogame about trading and you are negotiating with the player. "
                    "You are selling a " + offers.active_offer["offer"]["item_id"] +
                    # " to " + offers.active_offer["npc"]["name"] +
                    " to the player "
                    + " for "
                    + str(offers.active_offer["offer"]["price"])
                    + " - the actual price of the "
                    + offers.active_offer["offer"]["item_id"]
                    + " is "
                    + str(get_item(offers.active_offer["offer"]["item_id"])["price"])
                    + ", which is unknown to the player. "
                    + offers.active_offer["npc"]["info"]
                    + "\nThis is your personal description: "
                    + offers.active_offer["npc"]["description"]
                    + "\n\nThese are your attributes as NPC that should be followed:\n"
            )

        for attribute, value in offers.active_offer["npc"]["attributes"].items():
            message["content"] += f"{attribute}: {value}\n"

            # if not npc_first:
            #     message["content"] += (
            #         "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"
            #     )
            # else:
            #     message["content"] += (
            #         "\n**Start convincing the player with 1 sentance**"
            #     )

        message[
            "content"
        ] += "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"

        offers.active_offer["messages"].append(message)

    message = request.get_json().get('message')
    offers.active_offer["messages"].append({"role": "user", "content": message})


    result = get_Responce_gemma(offers.active_offer)

    offers.active_offer["messages"].append({"role": "npc", "content": result["answer_to_player"]})

    offers.active_offer["offer"]["price"] = result["price"]

    return jsonify({"response": result})

