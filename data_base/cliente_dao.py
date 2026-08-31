"""CRUD de Cliente."""

from ..modelos.cliente import Cliente
from .base_dao import BaseDAO

COLUNAS = "id, nome, endereco, telefone"


class ClienteDAO(BaseDAO):

    def inserir(self, cliente):
        """Valida os campos obrigatórios antes de persistir."""
        cliente.validar()
        cursor = self._executar(
            "INSERT INTO cliente (nome, endereco, telefone) VALUES (?, ?, ?)",
            (cliente.nome, cliente.endereco, cliente.telefone),
        )
        cliente.id = cursor.lastrowid
        return cliente.id

    def buscar_por_id(self, id):
        linha = self._consultar_um(
            "SELECT {} FROM cliente WHERE id = ?".format(COLUNAS), (id,)
        )
        return self._para_objeto(linha)

    def buscar_por_nome(self, nome):
        linhas = self._consultar_todos(
            "SELECT {} FROM cliente WHERE nome LIKE ? ORDER BY nome".format(COLUNAS),
            ("%{}%".format(nome),),
        )
        return [self._para_objeto(linha) for linha in linhas]

    def listar_todos(self):
        linhas = self._consultar_todos(
            "SELECT {} FROM cliente ORDER BY id".format(COLUNAS)
        )
        return [self._para_objeto(linha) for linha in linhas]

    def atualizar(self, cliente):
        if cliente.id is None:
            raise ValueError("Não é possível atualizar um cliente sem id.")
        cliente.validar()
        cursor = self._executar(
            "UPDATE cliente SET nome = ?, endereco = ?, telefone = ? WHERE id = ?",
            (cliente.nome, cliente.endereco, cliente.telefone, cliente.id),
        )
        return cursor.rowcount > 0

    def remover(self, id):
        cursor = self._executar("DELETE FROM cliente WHERE id = ?", (id,))
        return cursor.rowcount > 0

    def contar(self):
        return self._consultar_um("SELECT COUNT(*) AS total FROM cliente")["total"]

    @staticmethod
    def _para_objeto(linha):
        if linha is None:
            return None
        return Cliente(
            id=linha["id"],
            nome=linha["nome"],
            endereco=linha["endereco"],
            telefone=linha["telefone"],
        )
