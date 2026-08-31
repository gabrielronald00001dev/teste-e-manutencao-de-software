"""CRUD de Material."""

from ..modelos.material import Material
from .base_dao import BaseDAO

COLUNAS = (
    "id, tipo_id, nome, valor_compra, valor_alocacao_diaria, status, condicao"
)


class MaterialDAO(BaseDAO):

    def inserir(self, material):
        material.validar()
        cursor = self._executar(
            "INSERT INTO material "
            "(tipo_id, nome, valor_compra, valor_alocacao_diaria, status, condicao) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                material.tipo_id,
                material.nome,
                material.valor_compra,
                material.valor_alocacao_diaria,
                material.status,
                material.condicao,
            ),
        )
        material.id = cursor.lastrowid
        return material.id

    def buscar_por_id(self, id):
        linha = self._consultar_um(
            "SELECT {} FROM material WHERE id = ?".format(COLUNAS), (id,)
        )
        return self._para_objeto(linha)

    def listar_todos(self):
        linhas = self._consultar_todos(
            "SELECT {} FROM material ORDER BY id".format(COLUNAS)
        )
        return [self._para_objeto(linha) for linha in linhas]

    def listar_por_status(self, status):
        linhas = self._consultar_todos(
            "SELECT {} FROM material WHERE status = ? ORDER BY id".format(COLUNAS),
            (status,),
        )
        return [self._para_objeto(linha) for linha in linhas]

    def listar_por_tipo(self, tipo_id):
        linhas = self._consultar_todos(
            "SELECT {} FROM material WHERE tipo_id = ? ORDER BY id".format(COLUNAS),
            (tipo_id,),
        )
        return [self._para_objeto(linha) for linha in linhas]

    def atualizar(self, material):
        if material.id is None:
            raise ValueError("Não é possível atualizar um material sem id.")
        material.validar()
        cursor = self._executar(
            "UPDATE material SET tipo_id = ?, nome = ?, valor_compra = ?, "
            "valor_alocacao_diaria = ?, status = ?, condicao = ? WHERE id = ?",
            (
                material.tipo_id,
                material.nome,
                material.valor_compra,
                material.valor_alocacao_diaria,
                material.status,
                material.condicao,
                material.id,
            ),
        )
        return cursor.rowcount > 0

    def atualizar_status(self, id, novo_status):
        """Aplica a regra de domínio no objeto e persiste a mudança."""
        material = self.buscar_por_id(id)
        if material is None:
            raise ValueError("Material {} não encontrado.".format(id))
        material.atualizar_status(novo_status)
        cursor = self._executar(
            "UPDATE material SET status = ? WHERE id = ?", (material.status, id)
        )
        return cursor.rowcount > 0

    def atualizar_condicao(self, id, nova_condicao):
        material = self.buscar_por_id(id)
        if material is None:
            raise ValueError("Material {} não encontrado.".format(id))
        material.atualizar_condicao(nova_condicao)
        cursor = self._executar(
            "UPDATE material SET condicao = ? WHERE id = ?", (material.condicao, id)
        )
        return cursor.rowcount > 0

    def remover(self, id):
        cursor = self._executar("DELETE FROM material WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def contar(self):
        return self._consultar_um("SELECT COUNT(*) AS total FROM material")["total"]

    @staticmethod
    def _para_objeto(linha):
        if linha is None:
            return None
        return Material(
            id=linha["id"],
            tipo_id=linha["tipo_id"],
            nome=linha["nome"],
            valor_compra=linha["valor_compra"],
            valor_alocacao_diaria=linha["valor_alocacao_diaria"],
            status=linha["status"],
            condicao=linha["condicao"],
        )
