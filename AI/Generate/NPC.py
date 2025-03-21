import json

import requests
import random

import model
from baza.item import get_all_item_idx
from baza.npc import *
from baza.offers import save_offer

from utils import Attributes, Deceitful, Personality, Naivety, TalkingStyle, Condition
import utils as utils

# url  = "http://localhost:11434/api/chat"
url  = "http://localhost:11434/api/generate"

def ask_question(question, fmt=None):
    data = {
        # "model": "llama3.2:1b",
        "model": model.model,
        "prompt": question,
        "seed": random.randint(1, 10 ** 18),
        "keep_alive": "30m",
        "stream": False
    }

    if fmt:
        data["format"] = fmt

    response = requests.post(url, json=data)
    return response.json().get("response", "")

def generate_npc_data(attributes): # TODO: pol (muz/zena/treto)
    name_prompt = (
        "Generate a random name for a typical person. "
        "Output only the name with no additional text."
    )
    name = ask_question(name_prompt).strip()

    info_prompt = (
        f"For an NPC named '{name}', provide a brief background description. "
        "Include where they live (e.g., country and town), their occupation, and a bit about who they are. "
        "Do NOT mention personality traits. "
        "Keep the description to 1-2 sentences in first person. Give me only the description, no additional text. "
        f"Attributes to consider: {attributes}"
    )
    info = ask_question(info_prompt).strip()

    personality_prompt = (
        f"Given the NPC named '{name}' with the following background:\n'{info}'\n\n"
        "Now, expand on their personality. Describe how they behave, speak, and interact, "
        "focusing on personality traits and talking style without mentioning appearance. "
        "Do not repeat the background details verbatim — create a richer, more detailed personality description. "
        "Keep it concise and to the point. Give me only the description, no additional text. "
        f"Attributes to consider: {attributes}"
    )
    description = ask_question(personality_prompt).strip()

    return name, info, description

def generate_offer_data(npc_parsed, item_parsed):
    prompt = (
            f"You have this NPC:\n{npc_parsed}.\n"
            f"That wants to sell this item:\n{item_parsed}\n"
            "Provide an offer for the item in JSON format with the following keys:\n"
            "- 'price': a number formatted as a float 0.00 (be sure not to set it too low, base it on the NPC's attributes and deceitfulness).\n"
            "- 'description': a short description of the item as if the NPC is trying to sell it. Use the language the NPC would use.\n"
            "Return only the JSON, with no extra text."
    )

    json_schema = {
        "type": "object",
        "properties": {
            "price": {"type": "integer"},
            "description": {"type": "string"}
        },
        "required": ["price", "description"]
    }

    response_text = ask_question(prompt, fmt=json_schema)
    result = json.loads(response_text)
    return float(result["price"]), result["description"]


def generate_random_npc(image_id):
    attributes = Attributes(
        random.choice(list(Deceitful)),
        random.choice(list(Personality)),
        random.choice(list(Naivety)),
        random.choice(list(TalkingStyle)))

    name, info, description = generate_npc_data(attributes)
    return create_person(image_id, name, info, description, random.uniform(0, 1), attributes)

def generate_offer(npc_name):
    item_id = random.choice(get_all_item_idx())

    price, description = generate_offer_data(
        get_person_str(npc_name),
        f"Name: {item_id}\n"
    )

    offer = {
        "price": price,
        "starting_price": price,
        "item_id": item_id,
        "description": description,
        "quantity": 1 # zar nqkoj den != 1
    }


    save_offer(npc_name, offer)

    return offer
