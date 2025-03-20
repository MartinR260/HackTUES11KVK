import os
import json
from enum import Enum


class Deceitful(Enum):
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high"


class Personality(Enum):
    AGGRESSIVE = "aggressive",
    PASSIVE = "passive",
    FRIENDLY = "friendly",
    UNHELPFUL = "unhelpful",
    HOSTILE = "hostile",
    ANXIOUS = "anxious"


class TalkingStyle(Enum):
    PSUVACH = "psuvach"


class Naivety(Enum):
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high"


dir_path = "baza/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)


def create_person(
        image_id: str,
        name: str,
        info: str,
        description: str,
        temperature: float,
        deceitful: Deceitful,
        personality: Personality,
        naivety: Naivety,
        talking_style: TalkingStyle):
    save_person(name, {
        "image_id": image_id,
        "name": name,
        "info": info,
        "description": description,
        "temperature": temperature,
        "attributes": {
            "deceitful": deceitful,
            "personality": personality,
            "naivety": naivety,
            "talking_style": talking_style
        },
        "memories": []
    })


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
