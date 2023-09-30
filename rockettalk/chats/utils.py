import uuid as _uuid
import random


def channel_fmt(name):
    return f"chat_{name}"

def uuid(rndbits=128):
    return str(_uuid.UUID(int=random.Random().getrandbits(rndbits)))