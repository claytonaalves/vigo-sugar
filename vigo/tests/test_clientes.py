import sys
sys.path.append('..')

import unittest
import datetime
import MySQLdb
import MySQLdb.cursors as cursors
from clientes import Clientes
from dbexceptions import RequiredFieldsError
from _mysql_exceptions import DatabaseError

class TestClientesAPI(unittest.TestCase):

    def setUp(self):
        self.conn = MySQLdb.connect('localhost', 'root', '', 'vigo',
                               charset='latin1',
                               use_unicode=True, 
                               cursorclass=cursors.DictCursor)
        self.query = self.conn.cursor()
        self.load_fixtures()

    def tearDown(self):
        self.conn.rollback()

    def load_fixtures(self):
        self.query.execute("INSERT INTO usuarios (numero, nome) VALUES (1, 'clayton')")

    def test_insercao(self):
        clientes = Clientes(self.query)
        dados = {'nome'    : 'Clayton',
                 'celular' : '1234-5678'}
        retorno = clientes.insert(dados)
        self.assertEqual('Clayton', retorno['nome'])
        self.assertEqual('1234-5678', retorno['celular'])

    def test_campos_obrigatorios(self):
        clientes = Clientes(self.query)
        dados = {'celular' : '0000-0000'}
        self.assertRaises(RequiredFieldsError, clientes.insert, dados)

    def test_campo_invalido(self):
        clientes = Clientes(self.query)
        dados = {'nome'   : 'Fulano da Silva'}
        retorno = clientes.update(1, dados)
        self.assertEqual('Fulano da Silva', retorno['nome'])

    def test_atualiza_cadastro(self):
        clientes = Clientes(self.query)


if __name__=="__main__":
    unittest.main()


