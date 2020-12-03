import json

import falcon


class PedidosStorage(object):
    def __init__(self, pedidos_dict=None):
        self.pedidos = pedidos_dict if pedidos_dict else []

    def create(self, pedido_dict):
        self.pedidos.append(pedido_dict)

    def get_one(self, pedido_id):
        try:
            return [p for p in self.pedidos
                    if p['id'] == int(pedido_id)]
        except KeyError:
            raise Exception('Pedido not found!')

    def get_all(self):
        return self.pedidos


class PedidosResource(object):
    def __init__(self):
        self.storage = PedidosStorage([
            {'id': 1, 'cliente_id': 1, 'valor': 120.51},
            {'id': 2, 'cliente_id': 2, 'valor': 253.48}
        ])

    def on_get(self, req, resp, pedido_id=None):
        resp.status = falcon.HTTP_200
        if pedido_id:
            content = self.storage.get_one(int(pedido_id))
        else:
            content = self.storage.get_all()
        resp.body = json.dumps(content)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        raw_json = json.loads(req.bounded_stream.read().decode())
        self.storage.create(raw_json)
