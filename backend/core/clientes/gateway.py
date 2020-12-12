from core.clientes.exceptions import ClienteNotFoundException, RequiredDataException
from database import Cliente


class ClienteGateway(object):
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Cliente).all()

    def get_one(self, cliente_id: int):
        cliente = self.session.query(Cliente).filter_by(id=cliente_id).first()
        if cliente:
            return cliente
        raise ClienteNotFoundException("Cliente ID = {} não encontrado!".format(cliente_id))

    def create(self, primeiro_nome: str, ultimo_nome: str, email: str):
        if not primeiro_nome or not ultimo_nome or not email:
            raise RequiredDataException

        cliente = Cliente(primeiro_nome=primeiro_nome, ultimo_nome=ultimo_nome, email=email)
        self.session.add(cliente)
        self.session.commit()
        return cliente

    def update(self, cliente_id: int, primeiro_nome: str = None, ultimo_nome: str = None, email: str = None):
        cliente = self.get_one(cliente_id)

        if primeiro_nome and primeiro_nome != cliente.primeiro_nome:
            cliente.primeiro_nome = primeiro_nome

        if ultimo_nome and ultimo_nome != cliente.ultimo_nome:
            cliente.ultimo_nome = ultimo_nome

        if email and email != cliente.email:
            cliente.email = email

        self.session.commit()
        return cliente

    def delete(self, cliente_id):
        cliente = self.get_one(cliente_id)
        self.session.delete(cliente)
        self.session.commit()

    def delete_all(self):
        self.session.query(Cliente).delete()
        self.session.commit()
