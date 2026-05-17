from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
class Usuario(BaseModel):
    nome: str
    email: str
    idade: int

app = FastAPI()

usuarios = {}

@app.get("/")
def raiz():
    return {"mensagem": "API de usuários funcionando"}

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    if usuario.nome in usuarios:
        raise HTTPException(status_code=400, detail="usuário já existe")
    usuarios[usuario.nome] = usuario.dict()
    return {"mensagem": f"usuário {usuario.nome} criado"}

@app.get("/usuarios")
def listar_usuarios():
    return usuarios

@app.get("/usuarios/{nome}")
def buscar_usuario(nome: str):
    if nome not in usuarios:
        raise HTTPException(status_code=404, detail="usuário não existe")
    return usuarios[nome]

@app.delete("/usuarios/{nome}")
def deletar_usuario(nome: str):
    if nome not in usuarios:
        raise HTTPException(status_code=404, detail="usuário nao existe")
    del usuarios[nome]
    return     {"mensagem": f"Usuário {nome} deletado"}

@app.put("/usuarios/{nome}")
def atualizar_usuario(usuario: Usuario, nome: str):
    if  nome not in usuarios:
        raise HTTPException(status_code=404, detail="usuário nao existe")
    usuarios[usuario.nome] = usuario.dict()
    return     {"mensagem": f"Usuário {usuario.nome} atualizado"}

    