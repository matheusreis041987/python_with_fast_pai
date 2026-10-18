from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import contaPagarReceber
from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import ContaPagarReceberResponse
from shared.dependencies import get_db

router_vs = APIRouter(prefix="/fornecedor-cliente")

@router_vs.get("/{id_conta}/contas-a-pagar-e-receber", response_model=List[ContaPagarReceberResponse])
async def obter_contas_fornecedor_por_id(id_conta: int, db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    resposta = db.query(contaPagarReceber).filter_by(fornecedor_cliente_id = id_conta).all()
    return resposta 
