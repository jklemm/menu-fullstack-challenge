import falcon

from database import Session
from middlewares.sqlalchemy_mysql import SQLAlchemySessionManager
from resources.pedidos_resource import PedidosResource
from resources.clientes_resource import ClientesResource

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
