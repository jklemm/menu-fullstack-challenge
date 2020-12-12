import json

import falcon

from core.clientes.gateway import ClienteGateway


class ClientesResource(object):

    def on_get(self, req, resp, cliente_id=None):
        cliente_gateway = ClienteGateway(self.session)

        resp.status = falcon.HTTP_200
        if cliente_id:
            clientes = cliente_gateway.get_one(int(cliente_id))
            content = clientes.to_json()
        else:
            clientes = cliente_gateway.get_all()
            content = [cliente.to_json() for cliente in clientes]
        resp.body = json.dumps(content)

    def on_post(self, req, resp):
        cliente_gateway = ClienteGateway(self.session)

        resp.status = falcon.HTTP_201
        raw_json = json.loads(req.bounded_stream.read().decode())
        primeiro_nome = raw_json['primeiro_nome']
        ultimo_nome = raw_json['ultimo_nome']
        email = raw_json['email']
        cliente_gateway.create(primeiro_nome, ultimo_nome, email)

    def on_put(self, req, resp, cliente_id=None):
        cliente_gateway = ClienteGateway(self.session)

        if not cliente_id:
            resp.status = falcon.HTTP_412
            return resp

        resp.status = falcon.HTTP_200
        raw_json = json.loads(req.bounded_stream.read().decode())
        primeiro_nome = raw_json.get('primeiro_nome', None)
        ultimo_nome = raw_json.get('ultimo_nome', None)
        email = raw_json.get('email', None)
        cliente_gateway.update(cliente_id, primeiro_nome, ultimo_nome, email)
