import sqlite3


class BancoDeDados:
    """Classe responsável por inicializar e gerenciar as tabelas do banco de dados SQLite."""

    def __init__(self, db_name=":memory:"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        # Tabela TipoMaterial
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS TipoMaterial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """
        )

        # Tabela Cliente
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """
        )

        # Tabela Material
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                valor_compra REAL NOT NULL,
                valor_alocacao_diaria REAL NOT NULL,
                status TEXT CHECK(status IN ('Disponível', 'Alocado')) NOT NULL DEFAULT 'Disponível',
                condicao TEXT CHECK(condicao IN ('Novo', 'Bom', 'Ruim', 'Inutilizado')) NOT NULL DEFAULT 'Novo',
                FOREIGN KEY (tipo_id) REFERENCES TipoMaterial (id)
            )
        """
        )

        # Tabela Locacao
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Locacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                previsao_devolucao TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES Cliente (id)
            )
        """
        )

        # Tabela ItensDaAlocacao (Relacionamento entre Locacao e Material)
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ItensDaAlocacao (
                id_locacao INTEGER NOT NULL,
                id_material INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_devolucao TEXT,
                valor_pago REAL,
                PRIMARY KEY (id_locacao, id_material),
                FOREIGN KEY (id_locacao) REFERENCES Locacao (id),
                FOREIGN KEY (id_material) REFERENCES Material (id)
            )
        """
        )
        self.conn.commit()

    def fechar(self):
        self.conn.close()


class TipoMaterialDAO:

    def __init__(self, db):
        self.db = db

    def criar(self, nome):
        if not nome:
            raise ValueError("O nome do tipo de material é obrigatório.")
        self.db.cursor.execute(
            "INSERT INTO TipoMaterial (nome) VALUES (?)", (nome,)
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def buscar_por_id(self, id_tipo):
        self.db.cursor.execute(
            "SELECT id, nome FROM TipoMaterial WHERE id = ?", (id_tipo,)
        )
        return self.db.cursor.fetchone()

    def atualizar(self, id_tipo, nome):
        if not nome:
            raise ValueError("O nome do tipo de material é obrigatório.")
        self.db.cursor.execute(
            "UPDATE TipoMaterial SET nome = ? WHERE id = ?", (nome, id_tipo)
        )
        self.db.conn.commit()

    def deletar(self, id_tipo):
        self.db.cursor.execute(
            "DELETE FROM TipoMaterial WHERE id = ?", (id_tipo,)
        )
        self.db.conn.commit()


class ClienteDAO:

    def __init__(self, db):
        self.db = db

    def criar(self, nome, endereco, telefone):
        if not nome or not endereco or not telefone:
            raise ValueError("Todos os campos do cliente são obrigatórios.")
        self.db.cursor.execute(
            "INSERT INTO Cliente (nome, endereco, telefone) VALUES (?, ?, ?)",
            (nome, endereco, telefone),
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def buscar_por_id(self, id_cliente):
        self.db.cursor.execute(
            "SELECT id, nome, endereco, telefone FROM Cliente WHERE id = ?",
            (id_cliente,),
        )
        return self.db.cursor.fetchone()

    def atualizar(self, id_cliente, nome, endereco, telefone):
        if not nome or not endereco or not telefone:
            raise ValueError("Todos os campos do cliente são obrigatórios.")
        self.db.cursor.execute(
            "UPDATE Cliente SET nome = ?, endereco = ?, telefone = ? WHERE id = ?",
            (nome, endereco, telefone, id_cliente),
        )
        self.db.conn.commit()

    def deletar(self, id_cliente):
        self.db.cursor.execute(
            "DELETE FROM Cliente WHERE id = ?", (id_cliente,)
        )
        self.db.conn.commit()


class MaterialDAO:

    def __init__(self, db):
        self.db = db

    def criar(
        self,
        tipo_id,
        nome,
        valor_compra,
        valor_alocacao_diaria,
        status="Disponível",
        condicao="Novo",
    ):
        if not tipo_id or not nome or valor_compra is None or valor_alocacao_diaria is None:
            raise ValueError(
                "Campos obrigatórios do material não foram preenchidos."
            )
        self.db.cursor.execute(
            """
            INSERT INTO Material (tipo_id, nome, valor_compra, valor_alocacao_diaria, status, condicao)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                tipo_id,
                nome,
                valor_compra,
                valor_alocacao_diaria,
                status,
                condicao,
            ),
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def buscar_por_id(self, id_material):
        self.db.cursor.execute(
            "SELECT id, tipo_id, nome, valor_compra, valor_alocacao_diaria, status, condicao FROM Material WHERE id = ?",
            (id_material,),
        )
        return self.db.cursor.fetchone()

    def atualizar_status(self, id_material, novo_status):
        self.db.cursor.execute(
            "UPDATE Material SET status = ? WHERE id = ?",
            (novo_status, id_material),
        )
        self.db.conn.commit()

    def atualizar_condicao(self, id_material, nova_condicao):
        self.db.cursor.execute(
            "UPDATE Material SET condicao = ? WHERE id = ?",
            (nova_condicao, id_material),
        )
        self.db.conn.commit()

    def deletar(self, id_material):
        self.db.cursor.execute(
            "DELETE FROM Material WHERE id = ?", (id_material,)
        )
        self.db.conn.commit()


class LocacaoDAO:

    def __init__(self, db):
        self.db = db

    def criar(self, cliente_id, data, previsao_devolucao):
        if not cliente_id or not data or not previsao_devolucao:
            raise ValueError(
                "Todos os campos da locação devem ser preenchidos."
            )
        self.db.cursor.execute(
            "INSERT INTO Locacao (cliente_id, data, previsao_devolucao) VALUES (?, ?, ?)",
            (cliente_id, data, previsao_devolucao),
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def buscar_por_id(self, id_locacao):
        self.db.cursor.execute(
            "SELECT id, cliente_id, data, previsao_devolucao FROM Locacao WHERE id = ?",
            (id_locacao,),
        )
        return self.db.cursor.fetchone()

    def deletar(self, id_locacao):
        self.db.cursor.execute(
            "DELETE FROM Locacao WHERE id = ?", (id_locacao,)
        )
        self.db.conn.commit()


class ItensDaAlocacaoDAO:

    def __init__(self, db):
        self.db = db

    def adicionar_item(
        self, id_locacao, id_material, valor, data_devolucao=None, valor_pago=None
    ):
        if not id_locacao or not id_material or valor is None:
            raise ValueError(
                "Identificadores da alocação/material e o valor são obrigatórios."
            )
        self.db.cursor.execute(
            """
            INSERT INTO ItensDaAlocacao (id_locacao, id_material, valor, data_devolucao, valor_pago)
            VALUES (?, ?, ?, ?, ?)
        """,
            (id_locacao, id_material, valor, data_devolucao, valor_pago),
        )
        self.db.conn.commit()

    def registrar_devolucao(self, id_locacao, id_material, data_devolucao, valor_pago):
        self.db.cursor.execute(
            """
            UPDATE ItensDaAlocacao 
            SET data_devolucao = ?, valor_pago = ? 
            WHERE id_locacao = ? AND id_material = ?
        """,
            (data_devolucao, valor_pago, id_locacao, id_material),
        )
        self.db.conn.commit()

    def buscar_por_locacao(self, id_locacao):
        self.db.cursor.execute(
            "SELECT id_locacao, id_material, valor, data_devolucao, valor_pago FROM ItensDaAlocacao WHERE id_locacao = ?",
            (id_locacao,),
        )
        return self.db.cursor.fetchall()