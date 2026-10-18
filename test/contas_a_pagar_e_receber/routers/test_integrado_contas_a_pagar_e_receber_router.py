from datetime import datetime

from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.database import Base, SessionLocal
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
def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/contas-a-pagar-e-receber", json={'descricao': 'Aluguel', 'valor': 2500.45, 'tipo': 'PAGAR'})
    response = client.post("/contas-a-pagar-e-receber", json={'descricao': 'Dividendos', 'valor': 15000, 'tipo': 'RECEBER'})
    response = client.post("/contas-a-pagar-e-receber", json={'descricao': 'Folha de pagamento', 'valor': 45865.45, 'tipo': 'PAGAR'})
    
    response = client.get("/contas-a-pagar-e-receber")
        
    assert response.status_code == 200

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 2500.45, 'tipo': 'PAGAR', "data_baixa": None, "valor_baixa": None,  "esta_baixada":False, 'fornecedor': None}, 
        {'id': 2, 'descricao': 'Dividendos', 'valor': 15000, 'tipo': 'RECEBER', "data_baixa": None, "valor_baixa": None,  "esta_baixada":False, 'fornecedor': None}, 
        {'id': 3, 'descricao': 'Folha de pagamento', 'valor': 45865.45, 'tipo': 'PAGAR', "data_baixa": None, "valor_baixa": None,  "esta_baixada":False, 'fornecedor': None}
        ]
    
def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        "descricao" : "Curso de python com fastAPI",
        "valor" : 2500.98,
        "tipo" : "PAGAR",
        "data_baixa": None,
        "valor_baixa": None, 
        "esta_baixada": False,
        'fornecedor': None 
    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    
    assert response.status_code == 201
    assert response.json() == nova_conta_copy
    
def test_deve_retornar_erro_quando_exceder_a_descricao():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
        'valor': 2500.45, 
        'tipo': 'PAGAR'
        })
    
    assert response.status_code == 422
    
def test_deve_retornar_erro_quando_exceder_do_tipo():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'titulo bancário', 
        'valor': 2500.45, 
        'tipo': 'PAGARRIA'})
    
    assert response.status_code == 422
    
def test_deve_retornar_erro_quando_exceder_do_valor():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'titulo bancário', 
        'valor': 'aaaa', 
        'tipo': 'PAGARRIA'})
    
    assert response.status_code == 422
    
def test_deve_retornar_erro_quando_exceder_do_valor_negativo():
    response = client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'titulo bancário', 
        'valor': -122, 
        'tipo': 'PAGARRIA'})
    
    assert response.status_code == 422
    
    
def test_deve_atualizar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/contas-a-pagar-e-receber", json={
    'descricao': 'titulo bancário', 
    'valor': 100, 
    'tipo': 'PAGAR'})
    
    id_da_conta = response.json()['id']
    
    response_put = client.put(f"/contas-a-pagar-e-receber/{id_da_conta}", json={   
    'descricao': 'titulo bancário', 
    'valor': 150, 
    'tipo': 'PAGAR'})
    
    assert response_put.status_code == 200
    assert response_put.json()['valor'] == 150
    


def test_deve_remover_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.post("/contas-a-pagar-e-receber", json={
    'descricao': 'titulo bancário2', 
    'valor': 150, 
    'tipo': 'PAGAR'})
    
    id_da_conta = response.json()['id']
    
    response_put = client.delete(f"/contas-a-pagar-e-receber/{id_da_conta}")
    
    assert response_put.status_code == 204
    
def test_deve_pegar_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response = client.post("/contas-a-pagar-e-receber", json={
    'descricao': 'titulo bancário2', 
    'valor': 150, 
    'tipo': 'PAGAR'})
    
    id = response.json()['id']
    
    response_get = client.get(f'/contas-a-pagar-e-receber/{id}')
    assert response_get.status_code == 200
    assert response_get.json()['valor'] == 150
    assert response_get.json()['descricao'] == 'titulo bancário2' 
    assert response_get.json()['tipo'] == 'PAGAR'    
    
def test_deve_pegar_por_id_invalido():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response = client.post("/contas-a-pagar-e-receber", json={
    'descricao': 'titulo bancário2', 
    'valor': 150, 
    'tipo': 'PAGAR'})
    
    id = 100
    
    response_get = client.get(f'/contas-a-pagar-e-receber/{id}')
    assert response_get.status_code == 404
    assert response_get.json()['Mensagem'] == 'Item não encontrato: Conta a pagar e Receber'

def test_deve_criar_conta_a_pagar_e_receber_com_fornecedor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta_response = {
        "id": 1,
        "descricao" : "Curso de python com fastAPI",
        "valor" : 2500.98,
        "tipo" : "PAGAR",
        "data_baixa": None,
        "valor_baixa": None,
        "esta_baixada": False,
        'fornecedor': {
            'id': 1,
            'nome': 'IBM Brasil'
        }
    }
    novo_fornecedor = {
        "nome": "IBM Brasil"
    }
    nova_conta = {
            "descricao" : "Curso de python com fastAPI",
            "valor" : 2500.98,
            "tipo" : "PAGAR",
            'fornecedor_cliente_id': 1 
        }
    client.post("/fornecedor-cliente", json=novo_fornecedor)
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    
    assert response.status_code == 201
    assert response.json() == nova_conta_response



def test_deve_baixar_conta():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'titulo bancário', 
        'valor': 2500.45, 
        'tipo': 'PAGAR'
        })
    
    response_acao = client.post(f'/contas-a-pagar-e-receber/1/baixar')
    
    assert response_acao.status_code == 200
    
    response_acao.json()['esta_baixada'] is True
    response_acao.json()['valor_baixa'] == 2500.45
    response_acao.json()['data_baixa'] is datetime