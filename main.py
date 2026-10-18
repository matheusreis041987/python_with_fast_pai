from fastapi import FastAPI
from shared.logger import logger
import uvicorn
from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import router
from contas_a_pagar_e_receber.routers.fornecedor_cliente_router import router_fornecedor
from contas_a_pagar_e_receber.routers.fornecedor_cliente_vs_contas_router import router_vs
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler
from shared.audit import AuditMiddleware
from shared.security import criar_token

#from shared.database import engine, Base, SessionLocal
#from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import contaPagarReceber

logger.info("API iniciada")

#cria e recria o db sempre que começa
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine) #objet engine é quem sabe falar com o db

#instanciando o fast api
app = FastAPI(
    title="Exemplo de uso do FastAPI",
    version="1.0",
    description="trabalhando com o fastAPI"
)


app.add_middleware(AuditMiddleware)

app.add_exception_handler(NotFound, not_found_exception_handler)




@app.get("/ola")
async def ola() -> str:
    return "Oi, seja bem vindo ao FastAPI"



app.include_router(router)
app.include_router(router_fornecedor)
app.include_router(router_vs)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8087)   
    














    
# documentação : http://localhost:8087/docs    

# http://localhost:8087/ola


#RODAR O FASTAPI COM O UVICORN NO TERMINAL

# python -m uvicorn main:app --reload --port 8087


# Rodar alembic para gerar o arqeuivo com a versão nova
# python -m alembic revision --autogenerate -m "Cria a tabela de fornecedor e cliente"

#rodar para criar as tabelas novamente
# python -m alembic upgrade head