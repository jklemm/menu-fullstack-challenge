import falcon

from api.database.database import Session
from api.middleware.sqlalchemy_mysql import SQLAlchemySessionManager
from api.resources.pedidos_resource import PedidosResource
from api.resources.clientes_resource import ClientesResource

app = falcon.API(
    middleware=[
        SQLAlchemySessionManager(Session),
    ]
)

pedidos = PedidosResource()

app.add_route('/pedidos', pedidos)
app.add_route('/pedidos/{pedido_id}', pedidos)

clientes = ClientesResource()

app.add_route('/clientes', clientes)
app.add_route('/clientes/{cliente_id}', clientes)
