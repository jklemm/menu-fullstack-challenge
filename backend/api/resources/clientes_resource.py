import json

import falcon

from api.resources import BaseResource
from core.clientes.exceptions import ClienteNotFoundException, DuplicatedEntityException
from core.clientes.gateway import ClienteGateway


class ClientesResource(BaseResource):
    def on_get(self, req, resp, cliente_id=None):
        cliente_gateway = ClienteGateway(self.db.session)

        if cliente_id:
            try:
                clientes = cliente_gateway.get_one(int(cliente_id))
                content = clientes.as_dict
            except ClienteNotFoundException as exc:
                resp.status = falcon.HTTP_404
                resp.body = json.dumps({"erro": str(exc)})
                return resp
        else:
            clientes = cliente_gateway.get_all()
            content = [cliente.as_dict for cliente in clientes]

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(content)

    def on_post(self, req, resp):
        cliente_gateway = ClienteGateway(self.db.session)

        resp.status = falcon.HTTP_201
        raw_json = json.loads(req.bounded_stream.read().decode())
        primeiro_nome = raw_json['primeiro_nome']
        ultimo_nome = raw_json['ultimo_nome']
        email = raw_json['email']

        try:
            cliente_gateway.create(primeiro_nome, ultimo_nome, email)
        except DuplicatedEntityException as exc:
            resp.status = falcon.HTTP_412
            resp.body = json.dumps({"erro": str(exc)})
            return resp

    def on_put(self, req, resp, cliente_id=None):
        cliente_gateway = ClienteGateway(self.db.session)

        if not cliente_id:
            resp.status = falcon.HTTP_412
            return resp

        resp.status = falcon.HTTP_200
        raw_json = json.loads(req.bounded_stream.read().decode())
        primeiro_nome = raw_json.get('primeiro_nome', None)
        ultimo_nome = raw_json.get('ultimo_nome', None)
        email = raw_json.get('email', None)
        cliente_gateway.update(cliente_id, primeiro_nome, ultimo_nome, email)
