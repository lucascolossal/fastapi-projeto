from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    idade: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def raiz():
    return {"mensagem": "API de usuários funcionando"}

@app.post("/usuarios")
def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.nome == usuario.nome).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="usuário já existe")
    novo = models.Usuario(nome=usuario.nome, email=usuario.email, idade=usuario.idade)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.get("/usuarios/{nome}")
def buscar_usuario(nome: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrado")
    return usuario

@app.delete("/usuarios/{nome}")
def deletar_usuario(nome: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensagem": f"Usuário {nome} deletado"}

@app.put("/usuarios/{nome}")
def atualizar_usuario(nome: str, usuario: UsuarioSchema, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrado")
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    db_usuario.idade = usuario.idade
    db.commit()
    db.refresh(db_usuario)
    return db_usuario