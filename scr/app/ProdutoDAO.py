# AUTOR: VINICIUS KUNZLER

from fastapi import APIRouter
from domain.entities.Produto import Produto

# import da persistência
import db
from infra.orm.ProdutoModel import ProdutoDB

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produtos")
async def get_produtos():
    # Lógica para obter todos os produtos
    return {"message": "GET all produtos"}

@router.get("/produtos/{produto_id}")
async def get_produto(produto_id: int):
    # Lógica para obter um produto específico pelo ID
    return {"message": "GET produto"}

@router.post("/produtos")
async def create_produto(produto: Produto):
    # Lógica para criar um novo produto
    return {"message": "POST create produto"}

@router.put("/produtos/{produto_id}")
async def update_produto(produto_id: int, produto: Produto):
    # Lógica para atualizar um produto específico pelo ID
    return {"message": "PUT update produto {produto_id}"}

@router.delete("/produtos/{produto_id}")
async def delete_produto(produto_id: int):
    # Lógica para deletar um produto específico pelo ID
    return {"message": "DELETE produto {produto_id}"}