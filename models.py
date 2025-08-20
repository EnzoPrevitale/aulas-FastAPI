from typing import Optional
from pydantic import BaseModel

class PersonagensToyStory(BaseModel):
    id: Optional[int] = None
    nome: str
    dono: str
    tamanho: str
    foto: str