import json
import os
import glob

item_path = "baza/items/"

if not os.path.exists(item_path):
    os.makedirs(item_path)

def save_item(type, name, image_id, price):
    value = {
        "type": type,
        "name": name,
        "image_id": image_id,
        "price": price
    }

    with open(item_path + name + ".json", "w") as json_file:
        json.dump(value, json_file)

    return value

def get_item(name):
    with open(item_path + name + ".json", "r") as json_file:
        return json.load(json_file)

def get_num_items():
    return len([f for f in os.listdir(item_path) if f.endswith(".json")])

def get_all_item_idx():
    return [
        f[:-5]
        for f in os.listdir(item_path)
        if f.endswith(".json")
    ]

def get_all_items():
    return [
        get_item(f[:-5])
        for f in os.listdir(item_path)
        if f.endswith(".json")
    ]