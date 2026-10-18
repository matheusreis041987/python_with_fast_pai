from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.database import Base
from shared.dependencies import get_db

# comando para rodar os testes: python -m pytest ou python -m pytest -p no:warnings

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db #O yield funciona de forma parecida com um return, mas permite que o código continue executando depois.
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

#TEM DE IMPLEMENTAR A PARTE DE CONTROLE DE3 ACESSO POR TOKEN
"""
#primeiro teste
def test_deve_listar_clientes_forcedores():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/fornecedor-cliente", json={'nome': 'Aguas do Rio'})
    response = client.post("/fornecedor-cliente", json={'nome': 'Light'})

    
    response = client.get("/fornecedor-cliente")
        
    assert response.status_code == 200

    assert response.json() == [
        {'id': 1, 'nome': 'Aguas do Rio'}, 
        {'id': 2, 'nome': 'Light'}
        ]

"""

def test_deve_criar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    novo_fornecedor_cliente = {
        "nome": "Aguas do Rio"
    }
    novo_fornecedor_cliente_copy =  novo_fornecedor_cliente.copy()
    novo_fornecedor_cliente_copy["id"] = 1
    response = client.post("/fornecedor-cliente", json=novo_fornecedor_cliente)
    
    assert response.status_code == 201
    assert response.json() == novo_fornecedor_cliente_copy


def test_deve_retornar_erro_quando_for_pequeno_texto_nome():
    response = client.post("/fornecedor-cliente", json={
        'nome': ''})
    
    assert response.status_code == 422

    
def test_deve_atualizar_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/fornecedor-cliente", json={
        'nome': 'Aguas do Rio'})
    
    id_da_conta = response.json()['id']
    
    response_put = client.put(f"/fornecedor-cliente/{id_da_conta}", json={   
    'nome': 'Aguas do Rio2'})
    
    assert response_put.status_code == 200
    assert response_put.json()['nome'] == 'Aguas do Rio2'
    

def test_deve_remover_cliente_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/fornecedor-cliente", json={
    'nome': 'Aguas do Rio2'})
    
    id_da_conta = response.json()['id']
    
    response_put = client.delete(f"/fornecedor-cliente/{id_da_conta}")
    
    assert response_put.status_code == 204

