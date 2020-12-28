from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyModel = declarative_base()


class Pedido(SqlAlchemyModel):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    cliente_id = Column(Integer)
    valor = Column(Float)

    def __init__(self, data, cliente_id, valor):
        self.data = data
        self.cliente_id = cliente_id
        self.valor = valor

    def __repr__(self):
        return "<Pedido(id={}, data='{}', cliente_id={}, valor={})>".format(self.id, self.data, self.cliente_id, self.valor)

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "data": str(self.data.isoformat()),
            "cliente_id": self.cliente_id,
            "valor": self.valor,
        }


class Cliente(SqlAlchemyModel):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    primeiro_nome = Column(String(100))
    ultimo_nome = Column(String(100))
    email = Column(String(255), unique=True)

    def __repr__(self):
        return "<Cliente(id={}, first_name='{}', last_name='{}', email='{}')>".format(
            self.id, self.primeiro_nome, self.ultimo_nome, self.email
        )

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "primeiro_nome": self.primeiro_nome,
            "ultimo_nome": self.ultimo_nome,
            "email": self.email,
        }
