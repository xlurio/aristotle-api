import uuid


def generate_registry():
    registry = uuid.uuid4()

    return str(registry)
