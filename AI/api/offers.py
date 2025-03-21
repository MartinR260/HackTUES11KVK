from os import system
from flask import request, jsonify
from Generate import NPC as npc_gen
from Generate import Memory as memo_gen 
from api.api import app
from baza import baza as baza
from utils import Item

active_offer = None
money = 1000


def initialize_offer(npc_image):
    global active_offer
    npc = npc_gen.generate_random_npc(npc_image)
    offer = npc_gen.generate_offer(npc["name"])
    active_offer = {"npc": npc, "offer": offer, "messages": []}
    print("initialized")

@app.route('/api/purse', methods=['GET'])
def get_purse():
    global money
    return jsonify({"money": money})

@app.route('/api/offer', methods=['GET'])
def get_offer():
    npc_image = request.args.get('npc_image')
    global active_offer
    if active_offer is None:
        initialize_offer(npc_image)

    return jsonify(active_offer)


@app.route('/api/offer/accept', methods=['POST'])
def accept_offer():
    global active_offer
    global money

    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400

    money -= active_offer["offer"]["price"]
    response = {"success": True, "money": money}

    # add to memo
    # acc . [message] .a pped "player accepted it"
    # active_offer["messages"].append({"role": "user", "content": "Accepted the offer for " + active_offer["offer"]["price"]})
    message = {"role": "user", "content": "Accepted the offer for " + str(active_offer["offer"]["price"])}

    # if active_offer["offer"]["price"] > 0.5 * active_offer["offer"]["original_price"]:
    system_message = {"role": "system", "content": ""}
    if active_offer["offer"]["price"] > Item.get_item(active_offer["offer"]["item"]["id"]).price:
        system_message["content"] += "This was a profit"
    else:
        system_message["content"] += "This was a loss"

    active_offer["messages"].append(message)
    active_offer["messages"].append(system_message)

    summary = memo_gen.get_summary(active_offer)

    active_offer["npc"]["memories"].append(summary)

    baza.save_person(active_offer["npc"]["name"], active_offer["npc"])

    active_offer = None
    return jsonify(response)


@app.route('/api/offer/decline', methods=['POST'])
def decline_offer():
    global active_offer

    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400

    response = {"success": True}

    message = {"role": "user", "content": "I will pass, bye! "}

    active_offer["messages"].append(message)
    # active_offer["messages"].append(system_message)

    summary = memo_gen.get_summary(active_offer)

    active_offer["npc"]["memories"].append(summary)

    baza.save_person(active_offer["npc"]["name"], active_offer["npc"])

    active_offer = None
    return jsonify(response)
