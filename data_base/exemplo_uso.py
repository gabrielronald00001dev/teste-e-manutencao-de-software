"""Demonstração do fluxo completo. Execute com: python exemplo_uso.py

Serve como conferência rápida de que a modelagem funciona ponta a ponta.
Os testes unitários ficam por sua conta, na pasta testes/.
"""

from datetime import date

from sistema_alocacao import (
    Cliente,
    ClienteDAO,
    Database,
    ItemDaAlocacao,
    ItemDaAlocacaoDAO,
    Locacao,
    LocacaoDAO,
    Material,
    MaterialDAO,
    TipoMaterial,
    TipoMaterialDAO,
)


def main():
    db = Database(":memory:")

    tipo_dao = TipoMaterialDAO(db)
    material_dao = MaterialDAO(db)
    cliente_dao = ClienteDAO(db)
    locacao_dao = LocacaoDAO(db)
    item_dao = ItemDaAlocacaoDAO(db)

    # --- Cadastros básicos -------------------------------------------------
    tipo_id = tipo_dao.inserir(TipoMaterial(nome="Andaimes"))
    material_id = material_dao.inserir(
        Material(
            tipo_id=tipo_id,
            nome="Andaime tubular 1,5m",
            valor_compra=1200.00,
            valor_alocacao_diaria=45.00,
        )
    )
    cliente_id = cliente_dao.inserir(
        Cliente(
            nome="Construtora Vale do Aço",
            endereco="Av. Amaral Peixoto, 100 - Volta Redonda/RJ",
            telefone="(24) 99999-1234",
        )
    )

    material = material_dao.buscar_por_id(material_id)
    print("Material cadastrado:", material)
    print("Dias para retorno do investimento:", material.calcular_dias_para_retorno())

    # --- Abertura da locação ----------------------------------------------
    data_locacao = date(2026, 8, 31)
    previsao = date(2026, 9, 5)

    locacao_id = locacao_dao.inserir(
        Locacao(cliente_id=cliente_id, data=data_locacao, previsao_devolucao=previsao)
    )
    locacao = locacao_dao.buscar_por_id(locacao_id)
    print("Dias previstos:", locacao.calcular_dias_previstos())

    item = ItemDaAlocacao(
        locacao_id=locacao_id,
        material_id=material_id,
        valor=material.valor_alocacao_diaria,
    )
    item_dao.inserir(item)
    material_dao.atualizar_status(material_id, Material.STATUS_ALOCADO)

    print("Status após alocar:", material_dao.buscar_por_id(material_id).status)
    print("Valor previsto:", locacao.calcular_valor_previsto([item]))

    # --- Devolução com 2 dias de atraso ------------------------------------
    item = item_dao.buscar_por_id(item.id)
    devolvido_em = date(2026, 9, 7)
    item.registrar_devolucao(devolvido_em, locacao.data, locacao.previsao_devolucao)
    item_dao.registrar_devolucao(item)
    material_dao.atualizar_status(material_id, Material.STATUS_DISPONIVEL)
    material_dao.atualizar_condicao(material_id, Material.CONDICAO_BOM)

    itens = item_dao.listar_por_locacao(locacao_id)
    print("Dias de atraso:", itens[0].calcular_dias_atraso(locacao.previsao_devolucao))
    print("Valor pago no item:", itens[0].valor_pago)
    print("Total da locação:", locacao.finalizar_locacao(itens))

    db.fechar()


if __name__ == "__main__":
    main()
