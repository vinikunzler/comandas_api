# AUTOR: VINICIUS KUNZLER

from fastapi import APIRouter, Depends
from domain.entities.Produto import Produto
from security import get_current_active_user, User

# import da persistência
import db
from infra.orm.ProdutoModel import ProdutoDB

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produtos")
async def get_produtos():
    # Lógica para obter todos os produtos
    try:
        session = db.Session()
        # busca todos
        dados = session.query(ProdutoDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produtos/{produto_id}")
async def get_produto(produto_id: int):
    # Lógica para obter um produto específico pelo ID
    try:
        session = db.Session()
        # busca um com filtro
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == produto_id).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produtos")
async def create_produto(produto: Produto):
    # Lógica para criar um novo produto
    try:
        session = db.Session()

        # cria um novo objeto com os dados da requisição
        dados = ProdutoDB(None, produto.nome, produto.descricao, produto.foto.encode('utf-8') if produto.foto else None, produto.valor_unitario)
        session.add(dados)
        session.commit()
        
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produtos/{produto_id}")
async def update_produto(produto_id: int, produto: Produto):
    # Lógica para atualizar um produto específico pelo ID
    try:
        session = db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == produto_id).one()
       
        # atualiza os dados com base no corpo da requisição
        dados.nome = produto.nome
        dados.descricao = produto.descricao
        dados.foto = produto.foto.encode('utf-8') if produto.foto else None
        dados.valor_unitario = produto.valor_unitario


        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produtos/{produto_id}")
async def delete_produto(produto_id: int):
    # Lógica para deletar um produto específico pelo ID
    try:
        session = db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == produto_id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()