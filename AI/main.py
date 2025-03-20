import baza
from baza import Deceitful, Personality, Naivety, TalkingStyle
import random

from enum import Enum

def generate_random_npc(image_id):
    # TODO: anton
    name = ""
    description = ""
    descriptive_personality = ""

    baza.create_person(image_id, name, description, descriptive_personality,
                       random.uniform(0, 1),
                       random.choice(list(Deceitful)),
                       random.choice(list(Personality)),
                       random.choice(list(Naivety)),
                       random.choice(list(TalkingStyle)))



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
    def __init__(self, name, image_id, base_price):
        self.name = name
        self.image_id = image_id
        self.base_price = base_price

        items.append(self)

    @staticmethod
    def get_item(name):
        for item in items:
            if item.name == name:
                return item


def generate_offer(npc):
    item = {
        "id": items[random.randint(0, len(items) - 1)],
        "condition": random.choice(list(Condition)),
    }

    # TODO: anton
    offer = {
        "price": 0,
        "item": item,
        "description": "",
        "quantity": 1
    }

    return offer
