"""Infraestrutura comum aos DAOs."""


class BaseDAO:
    """Recebe o Database por injeção, o que permite trocar o banco nos testes."""

    def __init__(self, db):
        if db is None or getattr(db, "conexao", None) is None:
            raise ValueError("É necessário informar um Database com conexão aberta.")
        self._db = db
        self._conexao = db.conexao

    def _executar(self, sql, parametros=()):
        cursor = self._conexao.cursor()
        cursor.execute(sql, parametros)
        self._conexao.commit()
        return cursor

    def _consultar_um(self, sql, parametros=()):
        cursor = self._conexao.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchone()

    def _consultar_todos(self, sql, parametros=()):
        cursor = self._conexao.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()
