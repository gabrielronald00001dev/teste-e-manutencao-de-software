"""CRUD de Locacao."""

from ..database import data_para_texto
from ..modelos.locacao import Locacao
from .base_dao import BaseDAO

COLUNAS = "id, data, cliente_id, previsao_devolucao"


class LocacaoDAO(BaseDAO):

    def inserir(self, locacao):
        locacao.validar()
        cursor = self._executar(
            "INSERT INTO locacao (data, cliente_id, previsao_devolucao) "
            "VALUES (?, ?, ?)",
            (
                data_para_texto(locacao.data),
                locacao.cliente_id,
                data_para_texto(locacao.previsao_devolucao),
            ),
        )
        locacao.id = cursor.lastrowid
        return locacao.id

    def buscar_por_id(self, id):
        linha = self._consultar_um(
            "SELECT {} FROM locacao WHERE id = ?".format(COLUNAS), (id,)
        )
        return self._para_objeto(linha)

    def listar_todos(self):
        linhas = self._consultar_todos(
            "SELECT {} FROM locacao ORDER BY id".format(COLUNAS)
        )
        return [self._para_objeto(linha) for linha in linhas]

    def listar_por_cliente(self, cliente_id):
        linhas = self._consultar_todos(
            "SELECT {} FROM locacao WHERE cliente_id = ? ORDER BY id".format(COLUNAS),
            (cliente_id,),
        )
        return [self._para_objeto(linha) for linha in linhas]

    def atualizar(self, locacao):
        if locacao.id is None:
            raise ValueError("Não é possível atualizar uma locação sem id.")
        locacao.validar()
        cursor = self._executar(
            "UPDATE locacao SET data = ?, cliente_id = ?, previsao_devolucao = ? "
            "WHERE id = ?",
            (
                data_para_texto(locacao.data),
                locacao.cliente_id,
                data_para_texto(locacao.previsao_devolucao),
                locacao.id,
            ),
        )
        return cursor.rowcount > 0

    def remover(self, id):
        """Remove a locação; os itens caem junto por ON DELETE CASCADE."""
        cursor = self._executar("DELETE FROM locacao WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def contar(self):
        return self._consultar_um("SELECT COUNT(*) AS total FROM locacao")["total"]

    @staticmethod
    def _para_objeto(linha):
        if linha is None:
            return None
        return Locacao(
            id=linha["id"],
            data=linha["data"],
            cliente_id=linha["cliente_id"],
            previsao_devolucao=linha["previsao_devolucao"],
        )
