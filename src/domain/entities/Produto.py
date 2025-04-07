# AUTOR: VINICIUS KUNZLER

from pydantic import BaseModel

class Produto(BaseModel):
    id_produto: int = None
    nome: str
    descricao: str = None
    valor_unitario: float
    foto: str = None