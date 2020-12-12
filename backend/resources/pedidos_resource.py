import json

import falcon

from core.pedidos.exceptions import PedidoNotFoundException
from core.pedidos.gateway import PedidoGateway


class PedidosResource(object):

    def on_get(self, req, resp, pedido_id=None):
        pedido_gateway = PedidoGateway(self.session)

        if pedido_id:
            try:
                pedidos = pedido_gateway.get_one(int(pedido_id))
                content = pedidos.to_json()
            except PedidoNotFoundException as exc:
                resp.status = falcon.HTTP_404
                resp.body = json.dumps({"erro": str(exc)})
                return resp
        else:
            pedidos = pedido_gateway.get_all()
            content = [pedido.to_json() for pedido in pedidos]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(content)

    def on_post(self, req, resp):
        pedido_gateway = PedidoGateway(self.session)

        resp.status = falcon.HTTP_201
        raw_json = json.loads(req.bounded_stream.read().decode())
        data = raw_json['data']
        cliente_id = raw_json['cliente_id']
        valor = raw_json['valor']
        pedido_gateway.create(data, cliente_id, valor)

    def on_put(self, req, resp, pedido_id=None):
        pedido_gateway = PedidoGateway(self.session)

        if not pedido_id:
            resp.status = falcon.HTTP_412
            return resp

        resp.status = falcon.HTTP_200
        raw_json = json.loads(req.bounded_stream.read().decode())
        data = raw_json.get('data', None)
        cliente_id = raw_json.get('cliente_id', None)
        valor = raw_json.get('valor', None)
        pedido_gateway.update(pedido_id, data, cliente_id, valor)
