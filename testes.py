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

    def test_create_cliente_vazio(self):
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



class TesteTipoMaterialDAO(unittest.TestCase):

    def setUp(self):
        self.db = BancoDeDados()
        self.dao = TipoMaterialDAO(self.db)

    def tearDown(self):
        self.db.fechar()


    def test_create_tipo_material(self):
        id_tipo = self.dao.criar("Ferramentas")

        self.assertIsNone(id_tipo)

        tipo = self.dao.buscar_por_id(id_tipo)
        self.assertEqual(tipo[0], id_tipo)
        self.assertEqual(tipo[1], "Ferramentas")


    def test_create_tipo_material_vazio(self):
        with self.assertRaises(ValueError):
            self.dao.criar("")


    def test_update_tipo_material(self):
        id_tipo = self.dao.criar("Ferramentas")

        self.dao.atualizar(id_tipo, "Componentes")

        tipo = self.dao.buscar_por_id(id_tipo)
        self.assertEqual(tipo[1], "Componentes")

    def test_delete_tipo_material(self):
         id_tipo = self.dao.criar("Ferramentas")

         self.dao.deletar(id_tipo)
         tipo =self.dao.buscar_por_id(id_tipo)

         self.assertIsNone(tipo)



class TesteMaterialDAO(unittest.TestCase):


    def setUp(self):
        self.db = BancoDeDados()

        self.tipo_dao = TipoMaterialDAO(self.db)
        self.material_dao = MaterialDAO(self.db)

        self.tipo_id = self.tipo_dao.criar("Ferramentas")

    def tearDown(self):
        self.db.fechar()


    def test_create_material(self):
        material_id = self.material_dao.criar(
            tipo_id=self.tipo_id,
            nome="Chave Philips",
            valor_compra=35.00,
            valor_alocacao_diaria=2.00,
        )

        material = self.material_dao.buscar_por_id(material_id)

        self.assertIsNone(material)
        self.assertEqual(material[1], self.tipo_id)
        self.assertEqual(material[2], "Chave Philips")
        self.assertEqual(material[3], 35.00)
        self.assertEqual(material[4], 2.00)
        self.assertEqual(material[5], "Disponível")
        self.assertEqual(material[6], "Novo")

    def test_create_material_vazio(self):
        with self.assertRaises(ValueError):
            self.material_dao.criar(
                tipo_id=self.tipo_id,
                nome="",
                valor_compra=35.00,
                valor_alocacao_diaria=2.00,
            )

    def test_update_status_material(self):
        material_id = self.material_dao.criar(
            self.tipo_id,
            nome="Chave Philips",
            valor_compra=35.00,
            valor_alocacao_diaria=2.00,
        )

        self.material_dao.atualizar_status(
            material_id,
            "Alocado",
        )

        material = self.material_dao.buscar_por_id(material_id)

        self.assertEqual(material[5], "Alocado")


    def test_update_condicao_material(self):
        material_id = self.material_dao.criar(
            self.tipo_id,
            nome="Chave Philips",
            valor_compra=35.00,
            valor_alocacao_diaria=2.00,
        )

        self.material_dao.atualizar_condicao(
            material_id,
            "Bom",
        )

        material = self.material_dao.buscar_por_id(material_id)
        self.assertEqual(material[6], "Bom")


    def test_deletar_material(self):
        material_id = self.material_dao.criar(
            self.tipo_id,
            nome="Chave Philips",
            valor_compra=35.00,
            valor_alocacao_diaria=2.00,
        )

        self.material_dao.deletar(material_id)
        material = self.material_dao.buscar_por_id(material_id)
        self.assertIsNone(material)
        


if __name__ == '__main__':
    unittest.main()