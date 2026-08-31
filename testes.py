import unittest

from database import (
    BancoDeDados,
    TipoMaterialDAO,
    ClienteDAO,
    MaterialDAO,
    LocacaoDAO,
    ItensDaAlocacaoDAO,
)

class TesteClienteDAO(unittest.TestCase):

    def setUp(self):
        self.db = BancoDeDados()
        self.dao = ClienteDAO(self.db)

    def tearDown(self):
        self.db.fechar()

    def test_criar_cliente(self):
        id_cliente = self.dao.criar(
            "Fulano",
            "Casa do caixa prego",
            "99999-9999",
        )

        cliente = self.dao.buscar_por_id(id_cliente)

        self.assertIsNotNone(cliente)
        self.assertEqual(cliente[1], "Fulano")
        self.assertEqual(cliente[2], "Casa do caixa prego")
        self.assertEqual(cliente[3], "99999-9999")

    def test_criar_cliente_vazio(self):
        with self.assertRaises(ValueError):
            self.dao.criar(
                "",
                "Ponte que caiu",
                "99999-9999",
            )

    def test_update_cliente(self):
        id_cliente = self.dao.criar(
            "Fulano",
            "Casa do caixa prego",
            "99999-9999",
        )

        self.dao.atualizar(
            id_cliente,
            "Ciclano",
            "Ponte que caiu",
            "99999-9999",
        )

    def test_delete_cliente(self):
        id_cliente = self.dao.criar(
            "Fulano",
            "Casa do caixa prego",
            "99999-9999",
        )

        self.dao.deletar(id_cliente)
        cliente = self.dao.buscar_por_id(id_cliente)
        self.assertIsNone(cliente)

if __name__ == '__main__':
    unittest.main()