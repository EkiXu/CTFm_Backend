import uuid

def genRandomTeamToken()->str:
    return uuid.uuid4()