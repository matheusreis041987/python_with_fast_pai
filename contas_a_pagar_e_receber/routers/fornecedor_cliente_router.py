from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import contaPagarReceber
from shared.dependencies import get_db
from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente
from shared.exceptions import NotFound
from shared.auth import usuario_logado
from shared.security import criar_token
from shared.logger import logger

#O Depends é um dos recursos mais importantes do FastAPI. 
# Ele implementa o conceito de injeção de dependências (Dependency Injection).


router_fornecedor = APIRouter(prefix="/fornecedor-cliente")


#DTO de saída
#é uma das classes mais importantes do Pydantic e é amplamente utilizada no FastAPI para definir e validar dados.

class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str
    
    class Config:
        orm_mode: True


    
class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    



@router_fornecedor.post("/login")
def login():

    token = criar_token(
        {
            "sub": "matheus",
            "nome": "Matheus Reis Costa",
            "perfil": "ADMIN"
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router_fornecedor.get("", response_model=list[FornecedorClienteResponse])
async def listar_fornecedor_cliente(usuario = Depends(usuario_logado) ,
                                    db: Session = Depends(get_db)) -> list[FornecedorClienteResponse]:
    logger.info(f"USUARIO={usuario['sub']} acessou listar_fornecedor_cliente")
    return db.query(FornecedorCliente).all()





# TESTAR AS POSSOBILIDADE DENTRO DO DB.QUERY

@router_fornecedor.get("/teste-query-1{id_fornecedor}", response_model=list[FornecedorClienteResponse])
async def listar_fornecedor_cliente_query_teste_1(id_fornecedor: int,
                                                db: Session = Depends(get_db)) -> list[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).order_by(
        FornecedorCliente.nome
        ).distinct(
            ).filter(
            FornecedorCliente.id > id_fornecedor)

@router_fornecedor.get("/quantidade", response_model=int)
async def listar_fornecedor_cliente_query_quantidade(db: Session = Depends(get_db)) -> int:
    return db.query(FornecedorCliente).count()



@router_fornecedor.get("/get-id{id_fornecedor}", response_model=FornecedorClienteResponse)
async def listar_fornecedor_cliente_query_get(id_fornecedor: int, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor = db.query(FornecedorCliente).get(id_fornecedor)
    if fornecedor  is None:
        raise NotFound("Fornecedor não encontrado")
    return fornecedor 



@router_fornecedor.get("/listar-tudo-tudo")
async def listar_fornecedor_cliente_tudo_tudo( db: Session = Depends(get_db)):
    return db.query(contaPagarReceber).join(FornecedorCliente).distinct().all()


# FIM DO TESTE DAS POSSOBILIDADE DENTRO DO DB.QUERY



# MESMA COISA, RETORNANDO TUDO, MAS USANDO INJEÇÃO DE SQL


@router_fornecedor.get("/listar-fornecedor-cliente", response_model=list[FornecedorClienteResponse], status_code=200)
async def listar_fornecedor_cliente_sql(db: Session = Depends(get_db)) -> list[FornecedorClienteResponse]:
    sql = text(
    """
    select
    *
    from fornecedor_cliente
    
    """
    )
    
    result = db.execute(sql)
    
    return result.mappings().all()
    


@router_fornecedor.get("/{id_conta}", response_model=FornecedorClienteResponse)
async def lista_fornecedor_cliente(id_conta: int, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    return busca_fornecedor_cliente_por_id(id_conta, db)   




@router_fornecedor.post("", response_model=FornecedorClienteResponse, status_code=201)    
def criar_conta(conta_request: FornecedorClienteRequest, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    
    forencedor_cliente = FornecedorCliente(**conta_request.dict()) #passa já todos os parâmetros do model

    if forencedor_cliente is None:
        raise NotFound("Sem fornecedor ou cliente")
    
    
    db.add(forencedor_cliente)
    db.commit()
    db.refresh(forencedor_cliente)
    
    return forencedor_cliente      
    

@router_fornecedor.put("/{id_conta}", response_model=FornecedorClienteResponse, status_code=200)    
def atualizar_conta(id_conta: int,
                conta_request: FornecedorClienteRequest, 
                db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    
    forencedor_cliente: FornecedorCliente = busca_fornecedor_cliente_por_id(id_conta, db)
    forencedor_cliente.nome = conta_request.nome

    db.add(forencedor_cliente)
    db.commit()    
    db.refresh(forencedor_cliente)
    
    return forencedor_cliente



@router_fornecedor.delete("/{id_conta}", status_code=204)    
def deletar_conta(id_conta: int, db: Session = Depends(get_db)) -> None:
    
    forencedor_cliente = busca_fornecedor_cliente_por_id(id_conta,db)
    db.delete(forencedor_cliente)
    db.commit()    

    
    return "Fornecedor/cliente deletada"



def busca_fornecedor_cliente_por_id(id_conta: int, db: Session = Depends(get_db)) -> FornecedorCliente:
    fornecedor_cliente = db.query(FornecedorCliente).get(id_conta)
    if fornecedor_cliente is None:
        raise NotFound("Cliente e Fornecedor não encontrado")
    return fornecedor_cliente



