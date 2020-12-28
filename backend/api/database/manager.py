import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

from api.database import models


class DBManager(object):
    def __init__(self, connection=None):
        self.connection = connection

        self.engine = sqlalchemy.create_engine(self.connection)
        self.DBSession = scoping.scoped_session(orm.sessionmaker(bind=self.engine, autocommit=False))

    @property
    def session(self):
        return self.DBSession()

    def setup(self):
        try:
            models.SqlAlchemyModel.metadata.create_all(self.engine)
        except Exception as e:
            print("Não foi possivel gerar o Banco de Dados: {}".format(e))
