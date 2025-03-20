from enum import Enum

items = []

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


class Condition(Enum):
    NEW = "new"
    AS_NEW = "as_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    BAD = "bad"
    BROKEN = "broken"


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