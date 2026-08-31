"""CRUD de TipoMaterial."""

from ..modelos.tipo_material import TipoMaterial
from .base_dao import BaseDAO


class TipoMaterialDAO(BaseDAO):

    def inserir(self, tipo_material):
        """Valida e persiste. Retorna o id gerado (também atribuído ao objeto)."""
        tipo_material.validar()
        cursor = self._executar(
            "INSERT INTO tipo_material (nome) VALUES (?)",
            (tipo_material.nome,),
        )
        tipo_material.id = cursor.lastrowid
        return tipo_material.id

    def buscar_por_id(self, id):
        linha = self._consultar_um(
            "SELECT id, nome FROM tipo_material WHERE id = ?", (id,)
        )
        return self._para_objeto(linha)

    def buscar_por_nome(self, nome):
        linha = self._consultar_um(
            "SELECT id, nome FROM tipo_material WHERE nome = ?", (nome,)
        )
        return self._para_objeto(linha)

    def listar_todos(self):
        linhas = self._consultar_todos("SELECT id, nome FROM tipo_material ORDER BY id")
        return [self._para_objeto(linha) for linha in linhas]

    def atualizar(self, tipo_material):
        """Retorna True se alguma linha foi alterada."""
        if tipo_material.id is None:
            raise ValueError("Não é possível atualizar um tipo sem id.")
        tipo_material.validar()
        cursor = self._executar(
            "UPDATE tipo_material SET nome = ? WHERE id = ?",
            (tipo_material.nome, tipo_material.id),
        )
        return cursor.rowcount > 0

    def remover(self, id):
        """Retorna True se alguma linha foi removida."""
        cursor = self._executar("DELETE FROM tipo_material WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def contar(self):
        return self._consultar_um("SELECT COUNT(*) AS total FROM tipo_material")["total"]

    @staticmethod
    def _para_objeto(linha):
        if linha is None:
            return None
        return TipoMaterial(id=linha["id"], nome=linha["nome"])
