from pydantic import BaseModel

class FacebookPost(BaseModel):
    content: str
    toxicity: float
    severe_toxicity: float
    obscene: float
    threat: float
    insult: float
    identity_attack: float