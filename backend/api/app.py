import os

import falcon

from api.database.manager import DBManager
from api.middleware.context import ContextMiddleware
from api.resources.clientes_resource import ClientesResource
from api.resources.pedidos_resource import PedidosResource


class APIService(falcon.API):
    def __init__(self, cfg):
        super(APIService, self).__init__(middleware=[ContextMiddleware()])

        self.cfg = cfg

        self.db_manager = DBManager(self.cfg.db.connection)
        if os.environ["ENV"] == "TEST":
            self.db_manager = DBManager(self.cfg.db_test.connection)
        elif os.environ["ENV"] == "CI":
            self.db_manager = DBManager(self.cfg.db_ci_test.connection)
        self.db_manager.setup()

        pedidos_resource = PedidosResource(self.db_manager)
        clientes_resource = ClientesResource(self.db_manager)

        self.add_route("/pedidos", pedidos_resource)
        self.add_route("/pedidos/{pedido_id}", pedidos_resource)
        self.add_route("/clientes", clientes_resource)
        self.add_route("/clientes/{cliente_id}", clientes_resource)

    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass
