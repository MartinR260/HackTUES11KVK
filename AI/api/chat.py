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
        "answer_to_player": "Look, I'm not running a charity here. $1500 is the price. I gotta think about my future, ya know? "
                            "Middle school teachers don't exactly rake in the dough. A little wiggle room, maybe, but 10%? Nah. "
                            "That's a lot off a perfectly good Lada. It's reliable, it's a classic... it's an investment! "
                            "Seriously, think about it. You're getting a steal at $1500.",
        "is_final": False,
        "price": 1500
    }

    offers.active_offer["messages"].append({"role": "npc", "content": result})

    return jsonify({"response": result})

