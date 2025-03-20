import os
import json
from utils import *

dir_path = "baza/bazi/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)


def create_person(
        image_id: str,
        name: str,
        info: str,
        description: str,
        temperature: float,
        attributes: Attributes):
    value = {
        "image_id": image_id,
        "name": name,
        "info": info,
        "description": description,
        "temperature": temperature,
        "attributes": {
            "deceitful": attributes.deceitful.value,
            "personality": attributes.personality.value,
            "naivety": attributes.naivety.value,
            "talking_style": attributes.talking_style.value,
        },
        "memories": []
    }
    save_person(name, value)
    return value


def get_person(name):
    with open(dir_path + name + ".json", "r") as json_file:
        return json.load(json_file)


def save_person(name, person):
    with open(dir_path + name + ".json", "w") as json_file:
        json.dump(person, json_file)


def set_property(name, property_name, value):
    person = get_person(name)
    person[property_name] = value
    save_person(name, person)


def save_memory(name, memory):
    person = get_person(name)
    person["memories"].append(memory)
    save_person(name, person)

def get_person_str(name):
    person = get_person(name)
    return (f"Name: {person['name']}\n"
            f"Info: {person['info']}\n"
            f"Description: {person['description']}\n"
            f"Attributes: {person['attributes']}\n")