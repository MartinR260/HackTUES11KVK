from flask import Flask, request, jsonify
from AI.Generate import NPC as npc_gen

app = Flask(__name__)

active_offer = None

def initialize_offer(npc_image):
    global active_offer
    npc = npc_gen.generate_random_npc(npc_image)
    offer = npc_gen.generate_offer(npc["name"])
    active_offer = { "npc": npc, "offer": offer }

@app.route('/offer', methods=['GET'])
def get_offer():
    npc_image = request.args.get('npc_image')
    global active_offer
    if active_offer is None:
        initialize_offer(npc_image)

    return jsonify(active_offer)

@app.route('/offer/accept', methods=['POST'])
def accept_offer():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    response = {"message": f"Offer from {active_offer['npc']['name']} accepted.", "offer": active_offer}
    active_offer = None
    return jsonify(response)

@app.route('/offer/decline', methods=['POST'])
def decline_offer():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    response = {"message": f"Offer from {active_offer['npc']['name']} declined.", "offer": active_offer}
    active_offer = None
    return jsonify(response)

@app.route('/offer/scam', methods=['POST'])
def report_scam():
    global active_offer
    if active_offer is None:
        return jsonify({"error": "No active offer."}), 400
    response = {"message": f"Offer from {active_offer['npc']['name']} reported as scam.", "offer": active_offer}
    active_offer = None
    return jsonify(response)

@app.route('/offer/bargain', methods=['POST'])
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

@app.route('/offer/message', methods=['POST'])
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