from sqlalchemy.orm import relationship

from shared.database import Base
from sqlalchemy import Column, Integer, String




class FornecedorCliente(Base):
    __tablename__ = 'fornecedor_cliente'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))
