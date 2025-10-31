from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CRUD com FastAPI")

class Item(BaseModel):
    nome: str
    preco: float
    em_estoque: bool = True

itens = []

# ====// Rota inicial //====
@app.get("/")
def home():
    return {"mensagem": "API FastAPI funcionando "}

# ====// CREATE //====
@app.post("/itens")
def criar_item(item: Item):
    # evita duplicatas
    for i in itens:
        if i.nome.lower() == item.nome.lower():
            raise HTTPException(status_code=400, detail="Item já existe")
    itens.append(item)
    return {"mensagem": "Item adicionado com sucesso!", "item": item}

# ====// READ //====
@app.get("/itens")
def listar_itens():
    return itens

@app.get("/itens/{nome}")
def buscar_item(nome: str):
    for item in itens:
        if item.nome.lower() == nome.lower():
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

# ====// UPDATE //====
@app.put("/itens/{nome}")
def atualizar_item(nome: str, item_atualizado: Item):
    for i, item in enumerate(itens):
        if item.nome.lower() == nome.lower():
            itens[i] = item_atualizado
            return {"mensagem": f"Item '{nome}' atualizado!", "item": item_atualizado}
    raise HTTPException(status_code=404, detail="Item não encontrado para atualização")

# ====// DELETE //====
@app.delete("/itens/{nome}")
def deletar_item(nome: str):
    global itens
    antes = len(itens)
    itens = [item for item in itens if item.nome.lower() != nome.lower()]
    if len(itens) == antes:
        raise HTTPException(status_code=404, detail="Item não encontrado para exclusão")
    return {"mensagem": f"Item '{nome}' removido!"}
