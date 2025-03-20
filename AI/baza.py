import os
import json
from enum import Enum


class Deceitful(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Personality(Enum):
    AGGRESSIVE = "aggressive"
    PASSIVE = "passive"
    FRIENDLY = "friendly"
    UNHELPFUL = "unhelpful"
    HOSTILE = "hostile"
    ANXIOUS = "anxious"


class TalkingStyle(Enum):
    NORMAL = "normal"
    CURSING = "cursing"
    FORMAL = "formal"
    INFORMAL = "informal"


class Naivety(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Attributes:
    def __init__(self, deceitful: Deceitful, personality: Personality, naivety: Naivety, talking_style: TalkingStyle):
        self.deceitful = deceitful
        self.personality = personality
        self.naivety = naivety
        self.talking_style = talking_style

    def __str__(self):
        return (f"{{\n"
                f"  Deceitful: { self.deceitful.value },\n"
                f"  Personality: { self.personality.value },\n"
                f"  Naivety: { self.naivety.value },\n"
                f"  TalkingStyle: { self.talking_style.value }\n"
                f"}}")



dir_path = "baza/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)


def create_person(
        image_id: str,
        name: str,
        info: str,
        description: str,
        temperature: float,
        attributes: Attributes):
    save_person(name, {
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
