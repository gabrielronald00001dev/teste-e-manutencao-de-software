import unittest, sqlite3
from database import BancoDeDados, TipoMaterialDAO, ClienteDAO, MaterialDAO, LocacaoDAO, ItensDaAlocacaoDAO

class TestDataBase(unittest.TestCase):

    def set_up(self):
        self.conn = sqlite3.connect(":memory:")
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Cliente VALUES (1, 'Fulano', '999999999')")
        self.conn.commit

    def tear_down(self):
        self.conn.close()

    def test_insert_cliente(self):
        resultado = ClienteDAO(self.conn, '')
