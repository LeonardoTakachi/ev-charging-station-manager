import io
import unittest
from contextlib import redirect_stdout

from main import GerenciadorRecarga


class TestGerenciadorRecarga(unittest.TestCase):
    def setUp(self):
        self.gerenciador = GerenciadorRecarga()

    def cadastrar(self, veiculo, bateria, id_sessao=""):
        with redirect_stdout(io.StringIO()):
            return self.gerenciador.cadastrar_sessao(
                veiculo,
                bateria,
                id_sessao,
            )

    def test_cadastro_valido(self):
        resultado = self.cadastrar("ABC1D23", 60, "SES-010")

        self.assertTrue(resultado)
        self.assertEqual(len(self.gerenciador.sessoes), 1)
        self.assertEqual(self.gerenciador.sessoes[0].id_sessao, "SES-010")

    def test_rejeita_capacidade_invalida(self):
        resultado = self.cadastrar("ABC1D23", 0, "SES-001")

        self.assertFalse(resultado)
        self.assertEqual(len(self.gerenciador.sessoes), 0)

    def test_rejeita_id_duplicado(self):
        self.cadastrar("ABC1D23", 60, "SES-001")
        resultado = self.cadastrar("XYZ9Z99", 70, "SES-001")

        self.assertFalse(resultado)
        self.assertEqual(len(self.gerenciador.sessoes), 1)

    def test_busca_sequencial(self):
        self.cadastrar("ABC1D23", 60, "SES-001")
        self.cadastrar("XYZ9Z99", 70, "SES-002")

        sessao = self.gerenciador.busca_sequencial("SES-002")

        self.assertIsNotNone(sessao)
        self.assertEqual(sessao.id_veiculo, "XYZ9Z99")

    def test_bubble_sort_por_id(self):
        self.cadastrar("CARRO3", 60, "SES-003")
        self.cadastrar("CARRO1", 60, "SES-001")
        self.cadastrar("CARRO2", 60, "SES-002")

        self.gerenciador.bubble_sort("1")

        ids = [sessao.id_sessao for sessao in self.gerenciador.sessoes]
        self.assertEqual(ids, ["SES-001", "SES-002", "SES-003"])

    def test_smart_charging_respeita_limite_da_estacao(self):
        self.cadastrar("CARRO1", 60, "SES-001")
        self.cadastrar("CARRO2", 60, "SES-002")
        self.cadastrar("CARRO3", 60, "SES-003")

        potencia_total = sum(
            sessao.potencia_alocada
            for sessao in self.gerenciador.sessoes
            if sessao.status == "Carregando"
        )

        self.assertAlmostEqual(potencia_total, 50.0, places=2)

    def test_encerrar_sessao(self):
        self.cadastrar("ABC1D23", 60, "SES-001")

        with redirect_stdout(io.StringIO()):
            resultado = self.gerenciador.encerrar_sessao("SES-001")

        sessao = self.gerenciador.busca_sequencial("SES-001")
        self.assertTrue(resultado)
        self.assertEqual(sessao.status, "Encerrada pelo Usuário")
        self.assertEqual(sessao.potencia_alocada, 0.0)


if __name__ == "__main__":
    unittest.main()
