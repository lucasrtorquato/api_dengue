from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class FocoDengue(Base):
    __tablename__ = "focos"

    id = Column(Integer, primary_key=True, index=True)

    tipo = Column(String)

    rua = Column(String)
    numero = Column(String)
    bairro = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)

    status = Column(String, default="Pendente")

    data_criacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    latitude = Column(Float)
    longitude = Column(Float)
