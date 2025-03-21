import random

import api.offers as offers
from api.api import app
from flask import jsonify, request
from Generate.ChatResponce import get_Responce_gemma
from utils import Item


@app.route("/api/sellChat", methods=["POST"])
def chat():
    if len(offers.active_offer["messages"]) == 0:
        # npc_first = True if random.random() > 0.5 else False
        npc_first = False
        message = {
            "role": "system",
            "content": (
                "You are an NPC in a videogame about trading and you are negotiating with the player. "
                "You want to buy his "
                + offers.active_offer["offer"]["item"]["id"]
                + "."
                +
                # " to " + offers.active_offer["npc"]["name"] +
                " for "
                + str(offers.active_offer["offer"]["price"])
                + " - the actual price of the "
                + offers.active_offer["offer"]["item"]["id"]
                + " is "
                + str(Item.get_item(offers.active_offer["offer"]["item"]["id"]).price)
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
                "You want to buy his "
                + offers.active_offer["offer"]["item"]["id"]
                + " for some profit."
                +
                # " to " + offers.active_offer["npc"]["name"] +
                " for "
                + str(offers.active_offer["offer"]["price"])
                + " - the actual price of the "
                + offers.active_offer["offer"]["item"]["id"]
                + " is "
                + str(Item.get_item(offers.active_offer["offer"]["item"]["id"]).price)
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

        message[ "content" ] += "\n**Output the string of your message to the player and if you accept the offer, output the final price.**"

        offers.active_offer["messages"].append(message)

    message = request.get_json().get("message")
    offers.active_offer["messages"].append({"role": "user", "content": message})

    result = get_Responce_gemma()

    offers.active_offer["messages"].append(
        {"role": "npc", "content": result["answer_to_player"]}
    )

    return jsonify({"response": result})
