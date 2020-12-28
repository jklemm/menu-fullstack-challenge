import aumbry
import pytest

from api.config import AppConfig
from api.database.manager import DBManager
from core.clientes.exceptions import ClienteNotFoundException, RequiredDataException
from core.clientes.gateway import ClienteGateway


class TestClienteGatewayTestCase(object):
    def setup(self):
        configurations = aumbry.load(aumbry.FILE, AppConfig, {"CONFIG_FILE_PATH": "./config.json"})
        db_manager = DBManager(configurations.db_test.connection)
        db_manager.setup()
        self.cliente_gateway = ClienteGateway(db_manager.session)

    def teardown(self):
        self.cliente_gateway.delete_all()

    def _cria_um_cliente(self, primeiro_nome: str = "", ultimo_nome: str = "", email: str = ""):
        return self.cliente_gateway.create(
            primeiro_nome=primeiro_nome or "João",
            ultimo_nome=ultimo_nome or "Ninguém",
            email=email or "joao.ninguem@gmail.com",
        )


class TestClienteGatewayGetAll(TestClienteGatewayTestCase):
    def test_retorna_vazio_quando_nao_ha_clientes_cadastrados(self):
        clientes = self.cliente_gateway.get_all()

        assert clientes == []

    def test_retorna_o_cliente_gerado(self):
        primeiro_nome = "Joaquim"
        ultimo_nome = "Delgado"
        email = "joaquim.delgado@gmail.com"
        self.cliente_gateway.create(primeiro_nome=primeiro_nome, ultimo_nome=ultimo_nome, email=email)

        clientes = self.cliente_gateway.get_all()

        assert isinstance(clientes, list)
        assert len(clientes) == 1
        assert clientes[0].primeiro_nome == primeiro_nome
        assert clientes[0].ultimo_nome == ultimo_nome
        assert clientes[0].email == email

    def test_retorna_tres_clientes(self):
        self._cria_um_cliente("João", "Ninguém", "joao.ninguem@gmail.com")
        self._cria_um_cliente("Joaquim", "Amaranto", "joaquim.amaranto@gmail.com")
        self._cria_um_cliente("Juca", "Pots", "juca.pots@gmail.com")

        clientes = self.cliente_gateway.get_all()

        assert len(clientes) == 3


class TestClienteGatewayGetOne(TestClienteGatewayTestCase):
    def test_retorna_erro_quando_nao_existe_cliente_informado(self):
        cliente_id_inexistente = 1337

        with pytest.raises(ClienteNotFoundException):
            self.cliente_gateway.get_one(cliente_id_inexistente)

    def test_retorna_cliente_quando_busca_pelo_id(self):
        cliente = self._cria_um_cliente()

        cliente_db = self.cliente_gateway.get_one(cliente.id)

        assert cliente_db is cliente


class TestClienteGatewayCreate(TestClienteGatewayTestCase):
    def test_retorna_erro_quando_nao_informa_dados_do_cliente(self):
        primeiro_nome = ""
        ultimo_nome = ""
        email = ""

        with pytest.raises(RequiredDataException):
            self.cliente_gateway.create(primeiro_nome, ultimo_nome, email)

    def test_gera_cliente_quando_informa_dados_corretos(self):
        primeiro_nome = "Jorge"
        ultimo_nome = "Klemm"
        email = "jorgeklemm@gmail.com"

        cliente = self.cliente_gateway.create(primeiro_nome, ultimo_nome, email)

        cliente_db = self.cliente_gateway.get_one(cliente.id)
        assert cliente_db.primeiro_nome == primeiro_nome
        assert cliente_db.ultimo_nome == ultimo_nome
        assert cliente_db.email == email


class TestClienteGatewayUpdate(TestClienteGatewayTestCase):
    def test_retorna_erro_quando_cliente_nao_existe(self):
        cliente_id_inexistente = 1337
        primeiro_nome = "Jorge"
        ultimo_nome = "Klemm"
        email = "jorgeklemm@gmail.com"

        with pytest.raises(ClienteNotFoundException):
            self.cliente_gateway.update(cliente_id_inexistente, primeiro_nome, ultimo_nome, email)

    def test_altera_cliente_quando_informa_dados_corretos(self):
        primeiro_nome_alterado = "Jailson"
        ultimo_nome_alterado = "Maia"
        email_alterado = "jailson.maia@gmail.com"
        cliente = self._cria_um_cliente()

        self.cliente_gateway.update(cliente.id, primeiro_nome_alterado, ultimo_nome_alterado, email_alterado)

        cliente_alterado = self.cliente_gateway.get_one(cliente.id)
        assert cliente_alterado.primeiro_nome == primeiro_nome_alterado
        assert cliente_alterado.ultimo_nome == ultimo_nome_alterado
        assert cliente_alterado.email == email_alterado


class TestClienteGatewayDelete(TestClienteGatewayTestCase):
    def test_retorna_erro_quando_cliente_nao_existe(self):
        cliente_id_inexistente = 1337

        with pytest.raises(ClienteNotFoundException):
            self.cliente_gateway.delete(cliente_id_inexistente)

    def test_remove_cliente_com_sucesso(self):
        cliente = self._cria_um_cliente()

        self.cliente_gateway.delete(cliente.id)

        with pytest.raises(ClienteNotFoundException):
            self.cliente_gateway.get_one(cliente.id)


class TestClienteGatewayDeleteAll(TestClienteGatewayTestCase):
    def test_remove_clientes_com_sucesso(self):
        self._cria_um_cliente("João", "Ninguém", "joao.ninguem@gmail.com")
        self._cria_um_cliente("Joaquim", "Amaranto", "joaquim.amaranto@gmail.com")
        self._cria_um_cliente("Juca", "Pots", "juca.pots@gmail.com")

        self.cliente_gateway.delete_all()

        clientes = self.cliente_gateway.get_all()
        assert len(clientes) == 0
