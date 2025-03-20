from flask import request, jsonify
from Generate import NPC as npc_gen
from api.api import app

active_offer = None
money = 1000


def initialize_offer(npc_image):
    global active_offer
    npc = npc_gen.generate_random_npc(npc_image)
    offer = npc_gen.generate_offer(npc["name"])
    active_offer = {"npc": npc, "offer": offer}


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


@app.route('/api/offer/scam', methods=['POST'])
def report_scam():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    response = {"success": True}
    active_offer = None
    return jsonify(response)


@app.route('/api/offer/bargain', methods=['POST'])
def bargain_offer():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    data = request.get_json()
    counter_offer = data.get("counter_offer")
    if counter_offer is None:
        return jsonify({"error": "counter_offer field is required."}), 400

    response = {"message": f"Bargaining initiated with a counter offer of {counter_offer}.", "offer": active_offer}
    return jsonify(response)


@app.route('/api/offer/message', methods=['POST'])
def message_offer():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    data = request.get_json()
    message = data.get("message")
    if message is None:
        return jsonify({"error": "message field is required."}), 400

    response = {"message": f"Message sent to {active_offer['npc']['name']}: {message}", "offer": active_offer}
    return jsonify(response)
