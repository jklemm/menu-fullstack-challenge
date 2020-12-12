import falcon

from database import Session
from middlewares.sqlalchemy_mysql import SQLAlchemySessionManager
from resources import PedidosResource

# /pedidos (GET, POST)
# /pedidos/:id (GET, PUT, DELETE)
# /clientes (GET, POST)
# /clientes/:id (GET, PUT, DELETE)

app = falcon.API(
    middleware=[
        SQLAlchemySessionManager(Session),
    ]
)

pedidos = PedidosResource()

app.add_route('/pedidos', pedidos)
app.add_route('/pedidos/{pedido_id}', pedidos)
