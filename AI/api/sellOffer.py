# from os import system
# from flask import request, jsonify
# from Generate import NPC as npc_gen
# from Generate import Memory as memo_gen
# from api.api import app
# from baza.item import get_item
#
# active_offer = None
# money = 1000
#
#
# def initialize_sellOffer(npc_image):
#     global active_offer
#     npc = npc_gen.generate_random_npc(npc_image)
#     sellOffer = npc_gen.generate_sellOffer(npc["name"])
#     active_offer = {"npc": npc, "offer": sellOffer, "messages": []}
#     print("initialized")
#
# @app.route('/api/sell', methods=['GET'])
# def get_sell():
#     npc_image = request.args.get('npc_image')
#     global active_offer
#     if active_offer is None:
#         initialize_sellOffer(npc_image)
#
#     return jsonify(active_offer)
#
#
# @app.route('/api/sell/accept', methods=['POST']) # finish
# def accept_offer():
#     global active_offer
#     global money
#
#     if active_offer is None:
#         return jsonify({"error": "No active offer."}), 400
#
#     money += active_offer["offer"]["price"]
#     response = {"success": True, "money": money}
#
#     # add to memo
#     # acc . [message] .a pped "player accepted it"
#     # active_offer["messages"].append({"role": "user", "content": "Accepted the offer for " + active_offer["offer"]["price"]})
#     message = {"role": "user", "content": "Accepted the offer for " + str(active_offer["offer"]["price"])}
#
#     # if active_offer["offer"]["price"] > 0.5 * active_offer["offer"]["original_price"]:
#     system_message = {"role": "system", "content": ""}
#     if active_offer["offer"]["price"] < get_item(active_offer["offer"]["item_id"])["price"]:
#         system_message["content"] += "This was a profit"
#     else:
#         system_message["content"] += "This was a loss"
#
#     active_offer["messages"].append(message)
#     active_offer["messages"].append(system_message)
#
#     summary = memo_gen.get_summary(active_offer)
#
#     active_offer["npc"]["memories"].append(summary)
#
#     baza.save_person(active_offer["npc"]["name"], active_offer["npc"])
#
#     active_offer = None
#     return jsonify(response)
#
#
# @app.route('/api/offer/decline', methods=['POST']) # finish
# def decline_offer():
#     global active_offer
#
#     if active_offer is None:
#         return jsonify({"error": "No active offer."}), 400
#
#     response = {"success": True}
#
#     message = {"role": "user", "content": "I guess i will find another buyer, bye! "}
#
#     active_offer["messages"].append(message)
#
#     summary = memo_gen.get_summary(active_offer)
#
#     active_offer["npc"]["memories"].append(summary)
#
#     baza.save_person(active_offer["npc"]["name"], active_offer["npc"])
#
#     active_offer = None
#     return jsonify(response)
