"""Conexao e schema do banco SQLite do Sistema de Alocacao de Materiais."""

import sqlite3
from datetime import date, datetime

SCRIPT_CRIACAO = """
CREATE TABLE IF NOT EXISTS tipo_material (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS material (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_id               INTEGER NOT NULL,
    nome                  TEXT    NOT NULL,
    valor_compra          REAL    NOT NULL,
    valor_alocacao_diaria REAL    NOT NULL,
    status                TEXT    NOT NULL CHECK (status IN ('Disponível', 'Alocado')),
    condicao              TEXT    NOT NULL CHECK (condicao IN ('Novo', 'Bom', 'Ruim', 'Inutilizado')),
    FOREIGN KEY (tipo_id) REFERENCES tipo_material (id)
);

CREATE TABLE IF NOT EXISTS locacao (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    data               TEXT    NOT NULL,
    cliente_id         INTEGER NOT NULL,
    previsao_devolucao TEXT    NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente (id)
);

CREATE TABLE IF NOT EXISTS itens_da_alocacao (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    locacao_id     INTEGER NOT NULL,
    material_id    INTEGER NOT NULL,
    valor          REAL    NOT NULL,
    data_devolucao TEXT,
    valor_pago     REAL,
    FOREIGN KEY (locacao_id)  REFERENCES locacao (id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES material (id),
    UNIQUE (locacao_id, material_id)
);
"""

TABELAS = (
    "itens_da_alocacao",
    "locacao",
    "material",
    "cliente",
    "tipo_material",
)


def data_para_texto(valor):
    """Converte date/datetime para o texto ISO gravado no banco."""
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date().isoformat()
    if isinstance(valor, date):
        return valor.isoformat()
    return str(valor)


def texto_para_data(valor):
    """Converte o texto ISO lido do banco de volta para date."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor))


class Database:
    """Encapsula a conexao SQLite.

    Use Database(':memory:') dentro do setUp() dos testes para que cada
    caso rode em um banco novo e completamente isolado.
    """

    def __init__(self, caminho=":memory:", criar_tabelas=True):
        self.caminho = caminho
        self.conexao = sqlite3.connect(caminho)
        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")
        if criar_tabelas:
            self.criar_tabelas()

    def criar_tabelas(self):
        self.conexao.executescript(SCRIPT_CRIACAO)
        self.conexao.commit()

    def apagar_tabelas(self):
        cursor = self.conexao.cursor()
        for tabela in TABELAS:
            cursor.execute("DROP TABLE IF EXISTS {}".format(tabela))
        self.conexao.commit()

    def limpar_dados(self):
        """Esvazia as tabelas mantendo o schema (alternativa ao drop/create)."""
        cursor = self.conexao.cursor()
        for tabela in TABELAS:
            cursor.execute("DELETE FROM {}".format(tabela))
        cursor.execute("DELETE FROM sqlite_sequence")
        self.conexao.commit()

    def executar(self, sql, parametros=()):
        cursor = self.conexao.cursor()
        cursor.execute(sql, parametros)
        self.conexao.commit()
        return cursor

    def fechar(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None
