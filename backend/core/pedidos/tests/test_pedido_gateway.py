from datetime import datetime

import aumbry
import pytest

from api.config import AppConfig
from api.database.manager import DBManager
from core.pedidos.exceptions import PedidoNotFoundException, RequiredDataException
from core.pedidos.gateway import PedidoGateway


class TestPedidoGatewayTestCase(object):
    def setup(self):
        configurations = aumbry.load(aumbry.FILE, AppConfig, {"CONFIG_FILE_PATH": "./config.json"})
        db_manager = DBManager(configurations.db_test.connection)
        db_manager.setup()
        self.pedido_gateway = PedidoGateway(db_manager.session)

    def teardown(self):
        self.pedido_gateway.delete_all()

    def _cria_um_pedido(self):
        return self.pedido_gateway.create(data=datetime.now(), cliente_id=1, valor=1.0)


class TestPedidoGatewayGetAll(TestPedidoGatewayTestCase):
    def test_retorna_vazio_quando_nao_ha_pedidos_cadastrados(self):
        pedidos = self.pedido_gateway.get_all()

        assert pedidos == []

    def test_retorna_o_pedido_gerado(self):
        data = datetime.now().replace(microsecond=0)
        cliente_id = 1
        valor = 1.0
        self.pedido_gateway.create(data=data, cliente_id=cliente_id, valor=valor)

        pedidos = self.pedido_gateway.get_all()

        assert isinstance(pedidos, list)
        assert len(pedidos) == 1
        assert pedidos[0].data == data
        assert pedidos[0].cliente_id == cliente_id
        assert pedidos[0].valor == valor

    def test_retorna_tres_pedidos(self):
        self._cria_um_pedido()
        self._cria_um_pedido()
        self._cria_um_pedido()

        pedidos = self.pedido_gateway.get_all()

        assert len(pedidos) == 3


class TestPedidoGatewayGetOne(TestPedidoGatewayTestCase):
    def test_retorna_erro_quando_nao_existe_pedido_informado(self):
        pedido_id_inexistente = 1337

        with pytest.raises(PedidoNotFoundException):
            self.pedido_gateway.get_one(pedido_id_inexistente)

    def test_retorna_pedido_quando_busca_pelo_id(self):
        pedido = self._cria_um_pedido()

        pedido_db = self.pedido_gateway.get_one(pedido.id)

        assert pedido_db is pedido


class TestPedidoGatewayCreate(TestPedidoGatewayTestCase):
    def test_retorna_erro_quando_nao_informa_dados_do_pedido(self):
        data = None
        cliente_id = 0
        valor = 0

        with pytest.raises(RequiredDataException):
            self.pedido_gateway.create(data, cliente_id, valor)

    def test_gera_pedido_quando_informa_dados_corretos(self):
        data = datetime.now().replace(microsecond=0)
        cliente_id = 1
        valor = 123

        pedido = self.pedido_gateway.create(data, cliente_id, valor)

        pedido_db = self.pedido_gateway.get_one(pedido.id)
        assert pedido_db.data == data
        assert pedido_db.cliente_id == cliente_id
        assert pedido_db.valor == valor


class TestPedidoGatewayUpdate(TestPedidoGatewayTestCase):
    def test_retorna_erro_quando_pedido_nao_existe(self):
        pedido_id_inexistente = 1337
        data = None
        cliente_id = 0
        valor = 0

        with pytest.raises(PedidoNotFoundException):
            self.pedido_gateway.update(pedido_id_inexistente, data, cliente_id, valor)

    def test_altera_pedido_quando_informa_dados_corretos(self):
        data_alterada = datetime.strptime("2020-02-02 02:02:02", "%Y-%m-%d %H:%M:%S")
        cliente_id_alterado = 2
        valor_alterado = 321
        pedido = self._cria_um_pedido()

        self.pedido_gateway.update(pedido.id, data_alterada, cliente_id_alterado, valor_alterado)

        pedido_alterado = self.pedido_gateway.get_one(pedido.id)
        assert pedido_alterado.data == data_alterada
        assert pedido_alterado.cliente_id == cliente_id_alterado
        assert pedido_alterado.valor == valor_alterado


class TestPedidoGatewayDelete(TestPedidoGatewayTestCase):
    def test_retorna_erro_quando_pedido_nao_existe(self):
        pedido_id_inexistente = 1337

        with pytest.raises(PedidoNotFoundException):
            self.pedido_gateway.delete(pedido_id_inexistente)

    def test_remove_pedido_com_sucesso(self):
        pedido = self._cria_um_pedido()

        self.pedido_gateway.delete(pedido.id)

        with pytest.raises(PedidoNotFoundException):
            self.pedido_gateway.get_one(pedido.id)


class TestPedidoGatewayDeleteAll(TestPedidoGatewayTestCase):
    def test_remove_pedidos_com_sucesso(self):
        self._cria_um_pedido()
        self._cria_um_pedido()
        self._cria_um_pedido()

        self.pedido_gateway.delete_all()

        pedidos = self.pedido_gateway.get_all()
        assert len(pedidos) == 0
