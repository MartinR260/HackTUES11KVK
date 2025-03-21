import json

from Generate.NPC import ask_question
from baza.item import save_item


def create_item(type, image_id):
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"},
        },
        "required": ["name", "price"]
    }

    res = json.loads(ask_question("Create a random item with this specification " + type, json_schema))
    save_item(type, res["name"], image_id, res["price"])

    return res