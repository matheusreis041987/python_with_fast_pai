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

#primeiro teste
def test_deve_listar_contas_de_um_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/fornecedor-cliente", json={'nome': 'Casa do Código'})
    client.post("/fornecedor-cliente", json={'nome': 'AD Treinamentos'})

    client.post("/contas-a-pagar-e-receber", 
                json={'descricao': 'Curso Python', 
                      'valor': 2500.45, 
                      'tipo': 'PAGAR',
                      'date_previsao': '2026-10-18',
                      'fornecedor_cliente_id' : 1
                      }
                )
    client.post("/contas-a-pagar-e-receber",
                json={'descricao': 'Curso de Guitarra', 
                      'valor': 15000, 
                      'tipo': 'PAGAR',
                      'date_previsao': '2026-10-18',
                      'fornecedor_cliente_id' : 2
                      }
                )    
    response_get_fornecedor1 = client.get(f"/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response_get_fornecedor1.status_code == 200
    assert len(response_get_fornecedor1.json()) == 1
    
    response_get_fornecedor2 = client.get(f"/fornecedor-cliente/2/contas-a-pagar-e-receber")
    assert response_get_fornecedor2.status_code == 200
    assert len(response_get_fornecedor2.json()) == 1



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
"""
