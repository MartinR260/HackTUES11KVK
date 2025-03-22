import os
import json
import random
from enum import Enum

# Define a temporary directory for testing
people_path = "temp_people/"
if not os.path.exists(people_path):
    os.makedirs(people_path)

# Dummy enum to simulate attributes
class DummyEnum(Enum):
    A = "A"
    B = "B"

# Dummy Attributes class similar to your implementation
class Attributes:
    def __init__(self, deceitful, personality, naivety, talking_style):
        self.deceitful = deceitful
        self.personality = personality
        self.naivety = naivety
        self.talking_style = talking_style

# Dummy function to simulate generate_npc_data
def generate_npc_data(image_id, attributes):
    # Generates a random name to reduce chances of duplicate files.
    return f"Name_{random.randint(1,10000)}", f"Info_{image_id}", f"Description_{attributes.deceitful.value}"

def create_person(image_id: str, name: str, info: str, description: str, temperature: float, attributes: Attributes):
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

def save_person(name, person):
    file_path = os.path.join(people_path, name + ".json")
    with open(file_path, "w") as json_file:
        json.dump(person, json_file)

def get_all_people_names():
    return [f[:-5] for f in os.listdir(people_path) if f.endswith(".json")]

def generate_random_npc(image_id):
    attributes = Attributes(
        random.choice(list(DummyEnum)),
        random.choice(list(DummyEnum)),
        random.choice(list(DummyEnum)),
        random.choice(list(DummyEnum))
    )
    name, info, description = generate_npc_data(image_id, attributes)
    return create_person(str(image_id), name, info, description, random.uniform(0, 1), attributes)

# Generate a new NPC
npc = generate_random_npc(0)
print("Generated NPC:", npc)

# Read back all names from the directory
names = get_all_people_names()
print("All NPC names from files:", names)

