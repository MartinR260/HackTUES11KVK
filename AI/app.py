from api.api import app

import random

import api.offers
import api.chat
from baza.item import get_num_items
from baza.npc import get_all_people_names
import Generate.NPC as npc_gen
import Generate.Item as item_gen
from baza.offers import get_all_offers

num_people = 5
num_items = 5
num_offers = 10

num_images = 6

if __name__ == "__main__":
    item_types = [
        "jewelry",
        "weapon",
        "clothing",
        "tech",
        "tool",
        "vehicle"
    ]

    names = get_all_people_names()

    if len(names) < num_people:
        for i in range(num_people - len(names)):
            npc_gen.generate_random_npc(random.randint(0, num_images))


    curr_num_items = get_num_items()
    if curr_num_items < num_items:
        for i in range(num_items - curr_num_items):
            item_gen.create_item(random.choice(item_types), random.randint(0, curr_num_items))



    curr_num_offers = len(get_all_offers())
    if curr_num_offers < num_offers:
        for i in range(num_offers - curr_num_offers):
            npc_gen.generate_offer(random.choice(get_all_people_names()))

    app.run(debug=True, host='0.0.0.0', port=5000)
