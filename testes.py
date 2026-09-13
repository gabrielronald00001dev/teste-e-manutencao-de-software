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

        self.assertIsNotNone(id_tipo)

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

        self.assertIsNotNone(material)
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


class TesteLocacaoDao(unittest.TestCase):

        def setUp(self):
            self.db = BancoDeDados()

            self.cliente_dao = ClienteDAO(self.db)
            self.locacao_dao = LocacaoDAO(self.db)

            self.cliente_id = self.cliente_dao.criar(
                "Fulano",
                "Casa do caixa prego",
                "99999-9999",
            )

        def tearDown(self):
            self.db.fechar()

        def test_create_locacao(self):
            locacao_id = self.locacao_dao.criar(
                cliente_id=self.cliente_id,
                data="2026-09-13",
                previsao_devolucao="2026-09-20",
            )

            self.assertIsNotNone(locacao_id)

            locacao = self.locacao_dao.buscar_por_id(locacao_id)

            self.assertIsNotNone(locacao)
            self.assertEqual(locacao[0], locacao_id)
            self.assertEqual(locacao[1], self.cliente_id)
            self.assertEqual(locacao[2], "2026-09-13")
            self.assertEqual(locacao[3], "2026-09-20")

        def test_criar_locacao_vazia(self):
            with self.assertRaises(ValueError):
                self.locacao_dao.criar(
                    cliente_id=self.cliente_id,
                    data="",
                    previsao_devolucao="2026-09-20",
                )

        def test_delete_locacao(self):
            locacao_id = self.locacao_dao.criar(
                cliente_id=self.cliente_id,
                data="2026-09-13",
                previsao_devolucao="2026-09-20",
            )

            self.locacao_dao.deletar(locacao_id)

            locacao = self.locacao_dao.buscar_por_id(locacao_id)

            self.assertIsNone(locacao)


class TesteItensDaAlocacao(unittest.TestCase):

    def setUp(self):

        self.db = BancoDeDados()
        self.cliente_dao = ClienteDAO(self.db)
        self.tipo_dao = TipoMaterialDAO(self.db)
        self.material_dao = MaterialDAO(self.db)
        self.locacao_dao = LocacaoDAO(self.db)
        self.item_dao = ItensDaAlocacaoDAO(self.db)

        self.cliente_id = self.cliente_dao.criar(
            "Fulano",
            "Casa do caixa prego",
            "99999-9999",
        )

        self.tipo_id = self.tipo_dao.criar(
            "Ferramentas"
        )

        self.material_id = self.material_dao.criar(
            tipo_id=self.tipo_id,
            nome="Chave Philips",
            valor_compra=35.00,
            valor_alocacao_diaria=2.00,
        )

        self.locacao_id = self.locacao_dao.criar(
            cliente_id=self.cliente_id,
            data="2026-09-13",
            previsao_devolucao="2026-09-20",
        )

    def tearDown(self):
        self.db.fechar()


    def test_adicionar_item(self):
        self.item_dao.adicionar_item(
            id_locacao=self.locacao_id,
            id_material=self.material_id,
            valor=2.00
        )

        itens = self.item_dao.buscar_por_locacao(
            self.locacao_id
        )

        self.assertIsNotNone(itens)
        self.assertEqual(len(itens), 1)

        item = itens[0]

        self.assertEqual(item[0], self.locacao_id)
        self.assertEqual(item[1], self.material_id)
        self.assertEqual(item[2], 2.00)
        self.assertIsNone(item[3])
        self.assertIsNone(item[4])


    def test_adicionar_item_vazio(self):
        with self.assertRaises(ValueError):
            self.item_dao.adicionar_item(
                id_locacao=self.locacao_id,
                id_material=self.material_id,
                valor=None
            )



    def test_registrar_devolucao(self):
        self.item_dao.adicionar_item(
            id_locacao=self.locacao_id,
            id_material=self.material_id,
            valor=2.00
        )

        self.item_dao.registrar_devolucao(
            id_locacao=self.locacao_id,
            id_material=self.material_id,
            data_devolucao="2026-09-18",
            valor_pago=10.00
        )

        itens = self.item_dao.buscar_por_locacao(
            self.locacao_id
        )

        self.assertEqual(len(itens), 1)

        item = itens[0]

        self.assertEqual(item[3], "2026-09-18")
        self.assertEqual(item[4], 10.00)



if __name__ == '__main__':
    unittest.main()