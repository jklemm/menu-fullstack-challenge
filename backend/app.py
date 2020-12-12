import falcon

from database import Session
from middlewares.sqlalchemy_mysql import SQLAlchemySessionManager

# /pedidos (GET, POST)
# /pedidos/:id (GET, PUT, DELETE)
# /clientes (GET, POST)
# /clientes/:id (GET, PUT, DELETE)
from resources.pedidos_resource import PedidosResource

app = falcon.API(
    middleware=[
        SQLAlchemySessionManager(Session),
    ]
)

pedidos = PedidosResource()

app.add_route('/pedidos', pedidos)
app.add_route('/pedidos/{pedido_id}', pedidos)
