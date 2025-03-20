# {"name":,"info":,"description":,}
import json
import requests

if __name__ == "__main__":
    question = "Genereta a name for an NPC in a real life simulation game. Return only the name."
    data = {
        "model": "llama3.2:1b",
        "prompt": question,
        "steal": False,
    }
    # url  = "http://localhost:11434/api/chat"
    url  = "http://localhost:11434/api/generate"

    response = requests.post(url, json=data)

    name = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            content = part.get("response", {})
            name += content

    print(name)

    question = "Generate info for a NPC named" + name + " - where its born, what his/her job is, what it does and some random data. Be really short and return only the info."

    data = {
        "model": "llama3.2:1b",
        "prompt": question,
        "steal": False,
    }

    response = requests.post(url, json=data)

    info = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            content = part.get("response", {})
            info += content

    print(info)

    question = "Generate talking style and character description for a NPC named" + name + ". Be super short"

    data = {
        "model": "llama3.2:1b",
        "prompt": question,
        "steal": False,
    }

    response = requests.post(url, json=data)

    description = ""
    for line in response.text.strip().split("\n"):
        if line:
            part = json.loads(line)
            content = part.get("response", {})
            description += content

    print(description)

