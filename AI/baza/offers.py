import os
import json
import glob

offers_path = "baza/offers/"

if not os.path.exists(offers_path):
    os.makedirs(offers_path)


def create_offer(
        npc_name: str,
        price: float,
        starting_price: float,
        item_id: str,
        # condition: Condition,
        description: str,
        quantity: int):
    value = {
        "npc_name": npc_name,
        "price": price,
        "starting_price": starting_price,
        "item_id": item_id,
        "description": description,
        "quantity": quantity
    }

    save_offer(npc_name, value)
    return value


def save_offer(npc_name, offer):
    curr_path = offers_path + npc_name + "/"
    if not os.path.exists(curr_path):
        os.makedirs(curr_path)

    id = len(get_all_offers_npc(npc_name))
    offer["id"] = id

    with open(curr_path + str(id) + ".json", "w") as json_file:
        json.dump(offer, json_file)


def get_offer(npc_name, id):
    with open(offers_path + npc_name + "/" + str(id) + ".json", "r") as json_file:
        return json.load(json_file)

def get_all_offers_npc(npc_name):
    return [
        json.load(open(offers_path + npc_name + "/" + f, "r"))
        for f in os.listdir(offers_path + npc_name)
        if f.endswith(".json")
    ]

def get_all_offers():
    return [
        json.load(open(f, "r"))
        for f in glob.glob(offers_path + "**/*.json", recursive=True)
    ]

def remove_offer(npc_name, id):
    os.remove(offers_path + npc_name + "/" + str(id) + ".json")
