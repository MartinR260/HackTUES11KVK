import baza
from baza import Deceitful, Personality, Naivety, TalkingStyle, Attributes
import random

import Generate.NPC as npc_gen

from enum import Enum

def generate_random_npc(image_id):
    attributes = Attributes(
        random.choice(list(Deceitful)),
        random.choice(list(Personality)),
        random.choice(list(Naivety)),
        random.choice(list(TalkingStyle)))

    name, info, description = npc_gen.generate_npc_data(attributes)
    baza.create_person(image_id, name, info, description, random.uniform(0, 1), attributes)



class Condition(Enum):
    NEW = "new"
    AS_NEW = "as_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    BAD = "bad"
    BROKEN = "broken"

items = []
class Item:
    def __init__(self, name, image_id, price):
        self.name = name
        self.image_id = image_id
        self.price = price

        items.append(self)

    @staticmethod
    def get_item(name):
        for item in items:
            if item.name == name:
                return item


Item("ciagane", "snimka2", 100)

def generate_offer(npc):
    item = {
        "id": items[random.randint(0, len(items) - 1)],
        "condition": random.choice(list(Condition)),
    }

    offer = {
        "price": 0, # TODO: anton
        "item": item,
        "description": "", # TODO: anton
        "quantity": 1 # zar nqkoj den != 1
    }

    return offer


if __name__ == "__main__":
    generate_random_npc(0)