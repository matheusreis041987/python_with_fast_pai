from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal
from sqlalchemy import extract, text
from sqlalchemy.orm import Session
from typing import Optional

from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente
from contas_a_pagar_e_receber.routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.dependencies import get_db
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import contaPagarReceber, Departamento, Empregados
from datetime import date, datetime

from shared.exceptions import NotFound

router = APIRouter(prefix="/contas-a-pagar-e-receber")


#DTO de saída
#é uma das classes mais importantes do Pydantic e é amplamente utilizada no FastAPI para definir e validar dados.

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str 
    valor:float
    tipo: str    #PAGAR, RECEBER
    data_baixa: datetime  | None = None
    valor_baixa: float  | None = None
    esta_baixada: bool  | None = None
    fornecedor: FornecedorClienteResponse | None = None
    
    class Config:
        orm_mode: True




#definir um Enun para o campo de tipo
class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'
    
    
class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min=3, max_length=30)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum   #PAGAR, RECEBER
    fornecedor_cliente_id: int | None = None
    
    

@router.get("", response_model=list[ContaPagarReceberResponse])
async def listar_contas(db: Session = Depends(get_db)) -> list[ContaPagarReceberResponse]:
    return db.query(contaPagarReceber).all()



@router.get("/{id_conta}", response_model=ContaPagarReceberResponse)
async def lista_conta(id_conta: int, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    return busca_conta_por_id(id_conta, db)
    

    

# MESMA COISA, RETORNANDO TUDO, MAS USANDO INJEÇÃO DE SQL


@router.get("/listar-contas", response_model=list[ContaPagarReceberResponse], status_code=200)
async def listar_contas(db: Session = Depends(get_db)) -> list[ContaPagarReceberResponse]:
    sql = text(
    """
    select
    *
    from contas_a_pagar_e_receber
    
    """
    )
    
    result = db.execute(sql)
    
    return result.mappings().all()
    
    


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)    
def criar_conta(conta_request: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    
    print(f'quantidade: {recupera_numero_registros(2026,10,db)}')
    
    
    contas_a_pagar_e_receber = contaPagarReceber(**conta_request.dict()) #passa já todos os parâmetros do model
    # contas_a_pagar_e_receber = contaPagarReceber(descricao = conta_request.descricao, valor = conta_request.valor, tipo = conta_request.tipo)
    
    if contas_a_pagar_e_receber is None:
        raise NotFound("Conta a pagar e Receber")
    
    if contas_a_pagar_e_receber.fornecedor_cliente_id is not None:
        fornecedor_cliente = db.query(FornecedorCliente).get(contas_a_pagar_e_receber.fornecedor_cliente_id)
        print(fornecedor_cliente)
        if fornecedor_cliente is None:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    
    return contas_a_pagar_e_receber       
    

@router.put("/{id_conta}", response_model=ContaPagarReceberResponse, status_code=200)    
def atualizar_conta(id_conta: int,
                conta_request: ContaPagarReceberRequest, 
                db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    
    conta_a_pagar_e_receber: contaPagarReceber = busca_conta_por_id(id_conta, db)
    
    if conta_a_pagar_e_receber.fornecedor_cliente_id is not None:
        fornecedor_cliente = db.query(FornecedorCliente).get(conta_a_pagar_e_receber.fornecedor_cliente_id)
        print(fornecedor_cliente)
        if fornecedor_cliente is None:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    conta_a_pagar_e_receber.tipo = conta_request.tipo
    conta_a_pagar_e_receber.descricao = conta_request.descricao
    conta_a_pagar_e_receber.valor = conta_request.valor
    db.add(conta_a_pagar_e_receber)
    db.commit()    
    db.refresh(conta_a_pagar_e_receber)
    
    return conta_a_pagar_e_receber






@router.post("/{id_conta}/baixar", response_model=ContaPagarReceberResponse, status_code=200)    
def baixar_conta(id_conta: int,
                db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    
    conta_a_pagar_e_receber: contaPagarReceber = busca_conta_por_id(id_conta, db)
    conta_a_pagar_e_receber.data_baixa = datetime.now()
    conta_a_pagar_e_receber.esta_baixada = True
    conta_a_pagar_e_receber.valor_baixa = conta_a_pagar_e_receber.valor

    db.add(conta_a_pagar_e_receber)
    db.commit()    
    db.refresh(conta_a_pagar_e_receber)
    
    return conta_a_pagar_e_receber







@router.delete("/{id_conta}", status_code=204)    
def deletar_conta(id_conta: int, db: Session = Depends(get_db)) -> None:
    
    conta_a_pagar_e_receber = busca_conta_por_id(id_conta,db)
    db.delete(conta_a_pagar_e_receber)
    db.commit()    

    
    return "Conta deletada"



def busca_conta_por_id(id_conta: int, db: Session = Depends(get_db)) -> contaPagarReceber:
    conta_a_pagar_e_receber = db.query(contaPagarReceber).get(id_conta)
    if conta_a_pagar_e_receber is None:
        raise NotFound("Conta a pagar e Receber")
    return conta_a_pagar_e_receber




def recupera_numero_registros(ano: int, mes: int, db: Session = Depends(get_db)) -> int:
    quantidade_registro = (db.query(contaPagarReceber).filter(
            extract('year',  contaPagarReceber.data_baixa) == ano,
            extract('month',contaPagarReceber.data_baixa) == mes).count())
    return quantidade_registro
    
    
def valida_se_pode_registrar_novas_contas(ano: int, mes: int, db: Session = Depends(get_db)) -> bool:
    if recupera_numero_registros(ano,mes, db) > 100:
        return False
    return True   
    
def lanca_excecao_quando_ultrapassar_numero_registros(contas_a_pagar_e_receber_resquest: ContaPagarReceberRequest,
                                                    db: Session = Depends(get_db)) -> None:
    if valida_se_pode_registrar_novas_contas(contas_a_pagar_e_receber_resquest.ano, contas_a_pagar_e_receber_resquest.mes, db):
        raise HTTPException(status_code=404, detail="Não é possível cadastrar. Ultrapassou o número de registros permitidos para o mês")
    






















# TESTE COM CLASSES DE EMPREGADOS  DEPARTAMENTO   


class departamentoResponse (BaseModel):
    id: int
    sigla: str
    centro_custo: int
    class Config:
        orm_mode: True
    
    
class departamentoRequest(BaseModel):
    sigla: str = Field(min_length=1, max_length=100)
    centro_custo: int = Field(gt=0)    

@router.post("/criar-departamento", response_model=departamentoResponse, status_code=201)
def criar_departamento(depart_resquest: departamentoRequest, db: Session = Depends(get_db)) -> departamentoResponse:
    
    departamento = Departamento(**depart_resquest.dict())
    db.add(departamento)
    db.commit()
    db.refresh(departamento)
    
    
    return departamento


@router.put("/atualizar-departamento/{id_departamento}", response_model=departamentoRequest, status_code=200)
def atualizar_conta(id_departamento: int, depart_request: departamentoRequest, db: Session = Depends(get_db)) -> departamentoResponse:
    departamento: Departamento = db.query(Departamento).get(id_departamento)
    departamento.sigla = depart_request.sigla
    departamento.centro_custo = depart_request.centro_custo
    db.add(departamento)
    db.commit()
    db.refresh(departamento)
    return departamento
    
@router.put("/atualizar-sigla-departamento/{id_depart}/{sigla_depart}", status_code=200 ) 
def autalizar_sigla_departamento(id_depart: int, sigla_depart: str,  db: Session = Depends(get_db)):
    sql = """
    update departamento
    set sigla = :sigla
    where id = :id
    
    """
    db.execute(
        text(sql),
        {"id": id_depart, "sigla": sigla_depart}
    )
    db.commit()
    return {"mensagem": "Departamento atualizado com sucesso"}


class empregadoResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    dt_nascimento: date
    salario: float
    id_departamento: int
    class Config:
        orm_mode: True
    
class empregadoRequest(BaseModel):
    nome: str
    cpf: str
    dt_nascimento: date
    salario: float
    id_departamento: int
    
@router.post("/criar-empregado", response_model=empregadoResponse, status_code=201)
def criar_empregado(emp_resquest: empregadoRequest, db: Session = Depends(get_db)) -> empregadoResponse:
    empregado = Empregados(**emp_resquest.dict())
    db.add(empregado)
    db.commit()
    db.refresh(empregado)
    
    return empregado


class empregadoResponseCompleto(BaseModel):
    id: int
    nome: str
    cpf: str
    dt_nascimento: date
    salario: float
    sigla_departamento: str
    centro_de_custo: int


@router.get("/buscar-empregado-completo/{id_empregado}", response_model=empregadoResponseCompleto, status_code=200)
def buscar_empregado_completo(id_empregado: int, db: Session = Depends(get_db)):
    
    sql = text("""
        select
        e.id,
        e.nome,
        e.cpf,
        e.dt_nascimento,
        e.salario,
        d.sigla as sigla_departamento,
        d.centro_custo as centro_de_custo
        from empregados as e
        left join departamento as d on (e.id_departamento = d.id)
        where
        e.id = :id_empregado 
    """)    
    
    resultado = db.execute(sql, {"id_empregado": id_empregado})
    return resultado.mappings().first()


@router.get("/buscar-empregado-por-sigla/{sigla_departamento}",  response_model=list[empregadoResponseCompleto], status_code=200)
def buscar_empregado_por_sigla(sigla_departamento :str, db: Session = Depends(get_db)):
    sql = text("""
                select
                e.id,
                e.nome,
                e.cpf,
                e.dt_nascimento,
                e.salario,
                d.sigla as sigla_departamento,
                d.centro_custo as centro_de_custo
                from empregados as e
                left join departamento as d on (e.id_departamento = d.id)
                where
                sigla ilike :sigla_departamento
    """)
    resultado = db.execute(sql, {"sigla_departamento": f"%{sigla_departamento}%"})
    return resultado.mappings().all()


#ENDPOINT PARA QUEM CHAMAR USAR O QUERY PARAMTER
@router.get("/buscar-empregado-por-sigla_query_parameter",  response_model=list[empregadoResponseCompleto], status_code=200)
def buscar_empregado_por_sigla(sigla_departamento :str, db: Session = Depends(get_db)):
    sql = text("""
                select
                e.id,
                e.nome,
                e.cpf,
                e.dt_nascimento,
                e.salario,
                d.sigla as sigla_departamento,
                d.centro_custo as centro_de_custo
                from empregados as e
                left join departamento as d on (e.id_departamento = d.id)
                where
                sigla ilike :sigla_departamento
    """)
    resultado = db.execute(sql, {"sigla_departamento": f"%{sigla_departamento}%"})
    return resultado.mappings().all()


from typing import Optional

@router.get("/buscar-empregado-id-sigla",response_model=list[empregadoResponseCompleto]
)
def buscar_empregado(
    id_empregado: Optional[int] = None,
    sigla_departamento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    sql = """
        select
            e.id,
            e.nome,
            e.cpf,
            e.dt_nascimento,
            e.salario,
            d.sigla as sigla_departamento,
            d.centro_custo as centro_de_custo
        from empregados e
        left join departamento d
            on e.id_departamento = d.id
        where 1 = 1
    """
    
    parametros = {}

    if id_empregado:
        sql += " and e.id = :id_empregado"
        parametros["id_empregado"] = id_empregado

    if sigla_departamento:
        sql += " and d.sigla ilike :sigla_departamento"
        parametros["sigla_departamento"] = f"%{sigla_departamento}%"

    resultado = db.execute(text(sql), parametros)

    return resultado.mappings().all()

