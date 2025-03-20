import json
import requests
import random

from lldb import INT32_MAX

# url  = "http://localhost:11434/api/chat"
url  = "http://localhost:11434/api/generate"

def ask_question(question):
    data = {
        "model": "llama3.2:1b",
        "prompt": question,
        "seed": random.randint(0, INT32_MAX),
        "keep_alive": "30m",
    }

    response = requests.post(url, json=data)

    value = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            content = part.get("response", {})
            value += content

    return value

def generate_npc_data(attributes) -> list: # TODO: pol
    name = ask_question("Create a random name that fits a normal person. Write it to be only a name, without any additional text.")

    info = ask_question("For an NPC called " + name + "\n"
                        "write a short description that describes where they live (country, town), who they are, where they work, etc. "
                        "Don't write about personality and write only that description and no excess text. "
                        "The description should be 1-2 sentences long at max written in first person. Make it match their talking style."
                        "These are their attributes: " + str(attributes))

    description = ask_question("For a NPC called " + name + " with this description:\n" + info + "\n"
                               "Expand on their personality, how they act, talk, etc. "
                               "Don't write about their appearance and write only that description and no excess text. "
                               "Don't copy everything verbatim, expand on the data I give you for a more rich and detailed personality description. "                                                                  
                               "Make it short and concise, Don't write extra stuff. "
                               "These are their attributes: " + str(attributes))

    return [name, info, description]