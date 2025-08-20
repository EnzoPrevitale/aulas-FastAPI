from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import PersonagensToyStory
from typing import Optional, Any

app = FastAPI(title="API dos personagens de Toy Story - DS18", version="0.0.1", description="Uma API feita com a DS18 para aprender FastAPI")

def fake_db():
    try:
        print("Conectando com o banco")
    finally:
        print("Fechando o banco")

personagens = {
    1: {
        "nome": "Woody",
        "dono": "Andy",
        "tamanho": "Pequeno",
        "foto": "https://static.wikia.nocookie.net/disney/images/0/05/Profile_-_Woody.jpg/revision/latest?cb=20240806015709&path-prefix=pt-br"
    },
    2: {
        "nome": "Buzz Lightyear",
        "dono": "Andy",
        "tamanho": "Médio",
        "foto": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/02/toy_story_pixar.jpg?w=1200&h=1200&crop=1"
    }
}

@app.get("/")
async def get():
    return {"Hello": "world"}

@app.get("/personagens")
async def get_personagens(db: Any = Depends(fake_db)):
    return personagens

@app.get("/personagens/{personagem_id}")
async def get_personagem(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[PersonagensToyStory] = None):
    next_id = len(personagens) + 1
    personagens[next_id] = personagem
    del personagem.id
    return personagem

@app.put("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id:int, personagem: PersonagensToyStory):
    if personagem_id in personagem:
        personagens[personagem_id] = personagem
        personagem.id = personagem_id
        del personagem.id
        return personagem
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.delete("/personagens/{personagem_id}")
async def delete_personagem(personagem_id: int):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.get("/calcular")
async def calcular(a: float, b: float):
    return {"Resultado": a + b}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)