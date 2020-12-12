import os

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import settings

if os.environ["ENV"] == "TEST":
    engine = create_engine(
        '{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(
            **settings.MYSQL_TEST
        )
    )
else:
    engine = create_engine(
        '{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(
            **settings.MYSQL_PROD
        )
    )

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()


class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    cliente_id = Column(Integer)
    valor = Column(Float)

    def __repr__(self):
        return "<Pedido(id={}, data='{}', cliente_id={}, valor={})>".format(
            self.id, self.data, self.cliente_id, self.valor
        )

    def to_json(self):
        return {
            'id': self.id,
            'data': str(self.data.isoformat()),
            'cliente_id': self.cliente_id,
            'valor': self.valor,
        }


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    primeiro_nome = Column(String(100))
    ultimo_nome = Column(String(100))
    email = Column(String(255))

    def __repr__(self):
        return "<Cliente(id={}, first_name='{}', last_name='{}', email='{}')>".format(
            self.id, self.primeiro_nome, self.ultimo_nome, self.email
        )

    def to_json(self):
        return {
            'id': self.id,
            'primeiro_nome': self.primeiro_nome,
            'ultimo_nome': self.ultimo_nome,
            'email': self.email,
        }


Base.metadata.create_all(engine)
