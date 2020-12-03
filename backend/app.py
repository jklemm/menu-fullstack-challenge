import falcon

from resources.pedidos_resource import PedidosResource

# /pedidos (GET, POST)
# /pedidos/:id (GET, PUT, DELETE)
# /clientes (GET, POST)
# /clientes/:id (GET, PUT, DELETE)

app = falcon.API()

pedidos = PedidosResource()

app.add_route('/pedidos', pedidos)
app.add_route('/pedidos/{pedido_id}', pedidos)
