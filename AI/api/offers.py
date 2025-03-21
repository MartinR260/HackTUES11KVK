import random

from flask import request, jsonify
from Generate import Memory as memo_gen
from api.api import app
from baza.item import get_item
from baza.npc import save_person, get_person
from baza.offers import get_all_offers, get_offer

money = 1000
active_offer = None

@app.route('/api/purse', methods=['GET'])
def get_purse():
    global money
    return jsonify({"money": money})

@app.route('/api/purse', methods=['POST'])
def set_purse():
    global money
    message = request.get_json().get('message')
    money = int(message)
    return jsonify({"money": money})

@app.route('/api/offers', methods=['GET'])
def get_offers():
    final_offers = []
    offers = random.choices(get_all_offers(), k=10)
    for offer in offers:
        final_offers.append({
            "offer": offer[0],
            "npc": get_person(offer[1])
        })
    return jsonify({"content": final_offers})


@app.route('/api/offer/select', methods=['POST'])
def select_offer():
    global active_offer

    offer_id = request.get_json().get('offer_id')
    npc_name = request.get_json().get('npc_name')

    offer = get_offer(npc_name, offer_id)
    npc = get_person(npc_name)

    active_offer = {
        "npc": npc,
        "offer": offer,
        "messages": []
    }

    return jsonify({"success": True, "active_offer": active_offer})

@app.route('/api/offer/accept', methods=['POST'])
def accept_offer():
    global money
    global active_offer

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
    if active_offer["offer"]["price"] > get_item(active_offer["offer"]["item_id"])["price"]:
        system_message["content"] += "This was a profit"
    else:
        system_message["content"] += "This was a loss"

    active_offer["messages"].append(message)
    active_offer["messages"].append(system_message)

    summary = memo_gen.get_summary(active_offer)

    active_offer["npc"]["memories"].append(summary)

    save_person(active_offer["npc"]["name"], active_offer["npc"])

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

    save_person(active_offer["npc"]["name"], active_offer["npc"])

    active_offer = None
    return jsonify(response)
