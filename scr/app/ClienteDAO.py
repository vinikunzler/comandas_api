from fastapi import APIRouter, HTTPException
from domain.entities.Cliente import Cliente

# import da persistência
import db
from infra.orm.ClienteModel import ClienteDB

router = APIRouter()

# Helper function to check for duplicate CPF
def is_cpf_duplicate(cpf: str, session) -> bool:
    return session.query(ClienteDB).filter(ClienteDB.cpf == cpf).first() is not None

# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/cliente/", tags=["Cliente"])
async def get_cliente():
    session = db.Session()
    try:
        clientes = session.query(ClienteDB).all()
        return clientes, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente(id: int):
    session = db.Session()
    try:
        cliente = session.query(ClienteDB).filter(ClienteDB.id == id).first()
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        return cliente, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    session = db.Session()
    try:
        # verifica se o CPF já está cadastrado
        if is_cpf_duplicate(corpo.cpf, session):
            return {"erro": "CPF já cadastrado"}, 400
        
        # cria um novo objeto com os dados da requisição
        novo_cliente = ClienteDB(
            nome=corpo.nome,
            cpf=corpo.cpf,
            telefone=corpo.telefone,
            grupo=corpo.grupo,
            senha=corpo.senha
        )
        session.add(novo_cliente)
        session.commit()
        return {"id": novo_cliente.id}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    session = db.Session()
    try:
        cliente = session.query(ClienteDB).filter(ClienteDB.id == id).first()
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        
        if cliente.cpf != corpo.cpf and is_cpf_duplicate(corpo.cpf, session):
            raise HTTPException(status_code=400, detail="CPF already exists")
        
        cliente.nome = corpo.nome
        cliente.cpf = corpo.cpf
        cliente.telefone = corpo.telefone
        cliente.grupo = corpo.grupo
        cliente.senha = corpo.senha
        
        session.commit()
        return {"msg": "put executado", "cliente": corpo}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    session = db.Session()
    try:
        cliente = session.query(ClienteDB).filter(ClienteDB.id == id).first()
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        
        session.delete(cliente)
        session.commit()
        return {"msg": "delete executado", "id": id}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()
# verifica se o CPF informado já esta cadastrado, retornado os dados atuais caso já esteja
@router.get("/cliente/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = db.Session()
        # busca um com filtro, retornando os dados cadastrados
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()