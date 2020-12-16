import json
from datetime import datetime

import aumbry
import falcon
from falcon import testing
import pytest

from api.app import APIService
from api.config import AppConfig
from core.clientes.gateway import ClienteGateway
from core.pedidos.gateway import PedidoGateway

configurations = aumbry.load(aumbry.FILE, AppConfig, {'CONFIG_FILE_PATH': './config.json'})
menu_service = APIService(configurations)


class TestPedidoResourceTestCase(object):
    def setup(self):
        self.session = menu_service.db_manager.session
        self.headers = {"Content-Type": "application/json"}

    def teardown(self):
        ClienteGateway(self.session).delete_all()
        PedidoGateway(self.session).delete_all()

    @pytest.fixture(scope="class")
    def client(self):
        return testing.TestClient(menu_service)

    def _gera_um_cliente(self, primeiro_nome, ultimo_nome, email):
        return ClienteGateway(self.session).create(
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            email=email
        )

    def _gera_um_pedido(self, data, cliente_id, valor):
        return PedidoGateway(self.session).create(
            data=data,
            cliente_id=cliente_id,
            valor=valor
        )

    def _busca_um_pedido(self, pedido_id):
        return PedidoGateway(self.session).get_one(pedido_id)


class TestPedidoResourceGetAll(TestPedidoResourceTestCase):

    def test_retorna_vazio_quando_nao_ha_pedidos_cadastrados(self, client):
        resposta_esperada = []

        response = client.simulate_get('/pedidos', headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_OK
        assert json_retornado == resposta_esperada

    def test_retorna_um_pedido_gerado(self, client):
        cliente = self._gera_um_cliente(primeiro_nome="Maria", ultimo_nome="Galvão", email="maria.galvao@gmail.com")
        data = datetime.now().replace(microsecond=0)
        valor = 30.53
        pedido = self._gera_um_pedido(data, cliente.id, valor)
        resposta_esperada = [
            {
                "id": pedido.id,
                "cliente_id": cliente.id,
                "valor": valor,
                "data": data.isoformat()
            }
        ]

        response = client.simulate_get('/pedidos', headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_OK
        assert json_retornado == resposta_esperada

    def test_retorna_tres_pedidos(self, client):
        cliente_1 = self._gera_um_cliente(primeiro_nome="Jorge", ultimo_nome="Klemm", email="jorgeklemm@gmail.com")
        data_1 = datetime.now().replace(microsecond=0)
        valor_1 = 10.12
        pedido_1 = self._gera_um_pedido(data_1, cliente_1.id, valor_1)
        cliente_2 = self._gera_um_cliente(primeiro_nome="João", ultimo_nome="Rosalvo", email="joao.rosalvo@gmail.com")
        data_2 = datetime.now().replace(microsecond=0)
        valor_2 = 20.23
        pedido_2 = self._gera_um_pedido(data_2, cliente_2.id, valor_2)
        cliente_3 = self._gera_um_cliente(primeiro_nome="Darci", ultimo_nome="de Matos", email="darci.matos@gmail.com")
        data_3 = datetime.now().replace(microsecond=0)
        valor_3 = 30.34
        pedido_3 = self._gera_um_pedido(data_3, cliente_3.id, valor_3)
        resposta_esperada = [
            {
                "id": pedido_1.id,
                "cliente_id": cliente_1.id,
                "valor": valor_1,
                "data": data_1.isoformat()
            },
            {
                "id": pedido_2.id,
                "cliente_id": cliente_2.id,
                "valor": valor_2,
                "data": data_2.isoformat()
            },
            {
                "id": pedido_3.id,
                "cliente_id": cliente_3.id,
                "valor": valor_3,
                "data": data_3.isoformat()
            },
        ]

        response = client.simulate_get('/pedidos', headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_OK
        assert json_retornado == resposta_esperada


class TestPedidoResourceGetOne(TestPedidoResourceTestCase):
    def test_retorna_erro_quando_nao_existe_pedido_informado(self, client):
        resposta_esperada = {'erro': 'Pedido ID = 1618613 não encontrado!'}

        response = client.simulate_get('/pedidos/1618613', headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_NOT_FOUND
        assert json_retornado == resposta_esperada

    def test_retorna_pedido_quando_busca_pelo_id(self, client):
        cliente = self._gera_um_cliente(primeiro_nome="Maria", ultimo_nome="Galvão", email="maria.galvao@gmail.com")
        data = datetime.now().replace(microsecond=0)
        valor = 30.53
        pedido = self._gera_um_pedido(data, cliente.id, valor)
        resposta_esperada = {
            "id": pedido.id,
            "cliente_id": cliente.id,
            "valor": valor,
            "data": data.isoformat()
        }

        response = client.simulate_get('/pedidos/{}'.format(pedido.id), headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_OK
        assert json_retornado == resposta_esperada


class TestPedidoResourceCreate(TestPedidoResourceTestCase):
    def test_retorna_erro_quando_nao_informa_dados_do_pedido(self, client):
        response = client.simulate_post('/pedidos', body="", headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_PRECONDITION_FAILED
        assert json_retornado == {"erro": "POST precisa conter um body."}

    def test_gera_pedido_quando_informa_dados_corretos(self, client):
        pedido = {
            "data": "2020-12-15 07:30:00",
            "cliente_id": "1",
            "valor": 101.23
        }

        response = client.simulate_post('/pedidos', body=json.dumps(pedido), headers=self.headers)

        assert response.status == falcon.HTTP_CREATED


class TestPedidoResourceUpdate(TestPedidoResourceTestCase):
    def test_retorna_erro_quando_nao_envia_id_na_url(self, client):
        response = client.simulate_put('/pedidos/', body="", headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_PRECONDITION_FAILED
        assert json_retornado == {"erro": "Metodo PUT requer o campo 'pedido_id' na URL"}

    def test_retorna_erro_quando_pedido_nao_existe(self, client):
        pedido_id_inexistente = 13254864
        pedido = {
            "data": "2020-12-15 07:30:00",
            "cliente_id": "1",
            "valor": 101.23
        }

        response = client.simulate_put('/pedidos/{}'.format(pedido_id_inexistente), body=json.dumps(pedido), headers=self.headers)

        json_retornado = json.loads(response.content.decode())
        assert response.status == falcon.HTTP_NOT_FOUND
        assert json_retornado == {"erro": "Pedido ID = {} não encontrado!".format(pedido_id_inexistente)}

    def test_altera_pedido_quando_informa_dados_corretos(self, client):
        cliente = self._gera_um_cliente(primeiro_nome="Jorge", ultimo_nome="Klemm", email="jorgeklemm@gmail.com")
        data = datetime.now().replace(microsecond=0)
        valor = 10.12
        pedido = self._gera_um_pedido(data, cliente.id, valor)

        cliente_alterado = self._gera_um_cliente(primeiro_nome="Outro", ultimo_nome="Cliente", email="outrocliente@gmail.com")
        data_alterada = "2020-12-15 07:30:00"
        valor_alterado = 20.23
        pedido_alterado = {
            "data": data_alterada,
            "cliente_id": cliente_alterado.id,
            "valor": valor_alterado
        }

        response = client.simulate_put('/pedidos/{}'.format(pedido.id), body=json.dumps(pedido_alterado),
                                       headers=self.headers)
        assert response.status == falcon.HTTP_OK

        pedido_retornado = self._busca_um_pedido(pedido.id)
        assert pedido_retornado.cliente_id == cliente_alterado.id
        assert pedido_retornado.data.strftime("%Y-%m-%d %H:%M:%S") == data_alterada
        assert pedido_retornado.valor == valor_alterado
