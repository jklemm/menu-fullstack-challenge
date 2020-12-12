from datetime import datetime

from core.pedidos.exceptions import PedidoNotFoundException, RequiredDataException
from database import Pedido


class PedidoGateway(object):
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Pedido).all()

    def get_one(self, pedido_id: int):
        pedido = self.session.query(Pedido).filter_by(id=pedido_id).first()
        if pedido:
            return pedido
        raise PedidoNotFoundException("Pedido ID = {} não encontrado!".format(pedido_id))

    def create(self, data: datetime, cliente_id: int, valor: float):
        if not data or not cliente_id or not valor:
            raise RequiredDataException

        pedido = Pedido(data=data, cliente_id=cliente_id, valor=valor)
        self.session.add(pedido)
        self.session.commit()
        return pedido

    def update(self, pedido_id: int, data: datetime = None, cliente_id: int = None, valor: float = None):
        pedido = self.get_one(pedido_id)

        if data and data != pedido.data:
            pedido.data = data

        if cliente_id and cliente_id != pedido.cliente_id:
            pedido.cliente_id = cliente_id

        if valor and valor != pedido.valor:
            pedido.valor = valor

        self.session.commit()
        return pedido

    def delete(self, pedido_id):
        pedido = self.get_one(pedido_id)
        self.session.delete(pedido)
        self.session.commit()

    def delete_all(self):
        self.session.query(Pedido).delete()
        self.session.commit()
