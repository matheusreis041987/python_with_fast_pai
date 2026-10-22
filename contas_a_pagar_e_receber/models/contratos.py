from shared.database import Base
from sqlalchemy import Column, Integer,String


class contratos(Base):
    __tablename__ = 'contratos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caminho_pdf = Column (String(255))