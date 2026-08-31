"""CRUD de ItensDaAlocacao."""

from ..database import data_para_texto
from ..modelos.item_da_alocacao import ItemDaAlocacao
from .base_dao import BaseDAO

COLUNAS = "id, locacao_id, material_id, valor, data_devolucao, valor_pago"


class ItemDaAlocacaoDAO(BaseDAO):

    def inserir(self, item):
        """Data de devolução e valor pago entram como NULL (vazios)."""
        item.validar()
        cursor = self._executar(
            "INSERT INTO itens_da_alocacao "
            "(locacao_id, material_id, valor, data_devolucao, valor_pago) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                item.locacao_id,
                item.material_id,
                item.valor,
                data_para_texto(item.data_devolucao),
                item.valor_pago,
            ),
        )
        item.id = cursor.lastrowid
        return item.id

    def buscar_por_id(self, id):
        linha = self._consultar_um(
            "SELECT {} FROM itens_da_alocacao WHERE id = ?".format(COLUNAS), (id,)
        )
        return self._para_objeto(linha)

    def listar_por_locacao(self, locacao_id):
        linhas = self._consultar_todos(
            "SELECT {} FROM itens_da_alocacao WHERE locacao_id = ? "
            "ORDER BY id".format(COLUNAS),
            (locacao_id,),
        )
        return [self._para_objeto(linha) for linha in linhas]

    def listar_pendentes(self, locacao_id=None):
        """Itens ainda sem devolução registrada."""
        sql = "SELECT {} FROM itens_da_alocacao WHERE data_devolucao IS NULL".format(
            COLUNAS
        )
        parametros = ()
        if locacao_id is not None:
            sql += " AND locacao_id = ?"
            parametros = (locacao_id,)
        return [self._para_objeto(linha) for linha in self._consultar_todos(sql, parametros)]

    def listar_todos(self):
        linhas = self._consultar_todos(
            "SELECT {} FROM itens_da_alocacao ORDER BY id".format(COLUNAS)
        )
        return [self._para_objeto(linha) for linha in linhas]

    def atualizar(self, item):
        if item.id is None:
            raise ValueError("Não é possível atualizar um item sem id.")
        item.validar()
        cursor = self._executar(
            "UPDATE itens_da_alocacao SET locacao_id = ?, material_id = ?, valor = ?, "
            "data_devolucao = ?, valor_pago = ? WHERE id = ?",
            (
                item.locacao_id,
                item.material_id,
                item.valor,
                data_para_texto(item.data_devolucao),
                item.valor_pago,
                item.id,
            ),
        )
        return cursor.rowcount > 0

    def registrar_devolucao(self, item):
        """Persiste apenas os campos preenchidos no retorno."""
        if item.id is None:
            raise ValueError("Não é possível registrar devolução de um item sem id.")
        if not item.foi_devolvido():
            raise ValueError(
                "Chame item.registrar_devolucao(...) antes de persistir a devolução."
            )
        cursor = self._executar(
            "UPDATE itens_da_alocacao SET data_devolucao = ?, valor_pago = ? "
            "WHERE id = ?",
            (data_para_texto(item.data_devolucao), item.valor_pago, item.id),
        )
        return cursor.rowcount > 0

    def remover(self, id):
        cursor = self._executar("DELETE FROM itens_da_alocacao WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def calcular_total_pago(self, locacao_id):
        """Soma de tudo que já foi pago em uma locação."""
        linha = self._consultar_um(
            "SELECT COALESCE(SUM(valor_pago), 0) AS total FROM itens_da_alocacao "
            "WHERE locacao_id = ?",
            (locacao_id,),
        )
        return round(linha["total"], 2)

    def contar(self):
        return self._consultar_um(
            "SELECT COUNT(*) AS total FROM itens_da_alocacao"
        )["total"]

    @staticmethod
    def _para_objeto(linha):
        if linha is None:
            return None
        return ItemDaAlocacao(
            id=linha["id"],
            locacao_id=linha["locacao_id"],
            material_id=linha["material_id"],
            valor=linha["valor"],
            data_devolucao=linha["data_devolucao"],
            valor_pago=linha["valor_pago"],
        )
