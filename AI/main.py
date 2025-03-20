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
    return baza.create_person(image_id, name, info, description, random.uniform(0, 1), attributes)



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


Item("leather jacket", "jacket_img", 250)
Item("antique watch", "watch_img", 500)
Item("silver necklace", "necklace_img", 180)
Item("vintage record", "record_img", 75)
Item("smartphone", "phone_img", 350)
Item("handcrafted vase", "vase_img", 120)
Item("gaming console", "console_img", 400)
Item("rare book", "book_img", 150)
Item("mountain bike", "bike_img", 320)
Item("wooden sculpture", "sculpture_img", 200)

def generate_offer(npc_name):
    item = {
        "id": items[random.randint(0, len(items) - 1)].name,
        "condition": random.choice(list(Condition)),
    }

    price, description = npc_gen.generate_offer_data(
        baza.get_person_str(npc_name),
        f"Name: {item["id"]}\n"
        f"Condition: {item['condition'].value}\n"
    )

    offer = {
        "price": price,
        "item": item,
        "description": description,
        "quantity": 1 # zar nqkoj den != 1
    }


    return offer


if __name__ == "__main__":
    npc = generate_random_npc(0)
    print(generate_offer(npc["name"]))