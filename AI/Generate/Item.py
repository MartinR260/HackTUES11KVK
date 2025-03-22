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

    res = json.loads(ask_question("Create a super basic item for a trading game." + type, json_schema))
    save_item(type, res["name"], image_id, res["price"])

    print("Generated an Item")

    return res
