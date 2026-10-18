from shared.database import Base
from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
#O relationship() é utilizado para criar relacionamentos entre tabelas no ORM do SQLAlchemy.

class contaPagarReceber(Base):
    __tablename__ = 'contas_a_pagar_e_receber'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column (String(255))
    valor = Column(Numeric(10,2))
    tipo = Column(String(30))
    date_previsao = Column(DateTime(), nullable=False)
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric())
    esta_baixada = Column(Boolean(), default=False)
    
    fornecedor_cliente_id = Column(ForeignKey("fornecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")


















class Departamento(Base):
    __tablename__ = "departamento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sigla = Column(String(255))
    centro_custo = Column(Integer)
    

class Empregados(Base):
    __tablename__ = "empregados"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
    cpf = Column(String(255))
    dt_nascimento = Column(Date)
    salario = Column(Numeric)
    id_departamento = Column(Integer, ForeignKey("departamento.id"))
    departamento = relationship("Departamento")
    
