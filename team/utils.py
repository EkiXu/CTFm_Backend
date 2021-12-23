import uuid

def genTeamToken(teamName:str)->str:
    return uuid.uuid5(uuid.NAMESPACE_OID,teamName)