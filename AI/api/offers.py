from flask import request, jsonify
from Generate import NPC as npc_gen
from api.api import app

active_offer = None
money = 1000


def initialize_offer(npc_image):
    global active_offer
    npc = npc_gen.generate_random_npc(npc_image)
    offer = npc_gen.generate_offer(npc["name"])
    active_offer = {"npc": npc, "offer": offer, "messages": []}
    print("initialized")


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

    active_offer = None
    return jsonify(response)


@app.route('/api/offer/decline', methods=['POST'])
def decline_offer():
    global active_offer

    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400

    response = {"success": True}
    active_offer = None
    return jsonify(response)
