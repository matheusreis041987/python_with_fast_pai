from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from shared.dependencies import get_db
from shared.exceptions import NotFound
from contas_a_pagar_e_receber.models.contratos import contratos
import base64
from pathlib import Path

router_contrato = APIRouter(prefix='/contratos')


class contrato_response(BaseModel):
    id: int
    nome_arquivo: str
    base64: str
    
@router_contrato.get("/documentos", response_model=list[contrato_response])
def listar_documentos(db: Session = Depends(get_db)):
    documentos = db.query(contratos).all()
    
    resultado = []
    
    for documento in documentos:
        caminho = Path(documento.caminho_pdf)       
        if not caminho.exists():
            continue       
        with open(caminho, "rb") as arquivo:
            conteudo = arquivo.read()            
        
        pdf_base64 = base64.b64encode(conteudo).decode("utf-8")
        
        resultado.append({
            "id": documento.id,
            "nome_arquivo" : caminho.name,
            "base64": pdf_base64
            
        })
    return resultado