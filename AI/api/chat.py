from flask import request, jsonify

from api.api import app
import api.offers as offers

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.get_json().get('message')

    print(offers.active_offer)
    offers.active_offer["messages"].append({"role": "user", "content": message})

    # aktual response from AI
    result = {
        "answer_to_player": "Otgovor",
        "is_final": False,
        "price": 1500
    }

    offers.active_offer["messages"].append({"role": "npc", "content": result})

    return jsonify({"response": result})

