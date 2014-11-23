import sys
sys.path.append('..')

import unittest
import datetime
import MySQLdb
import MySQLdb.cursors as cursors
from atendimentos import Atendimentos

class TestAtendimentosAPI(unittest.TestCase):

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
        self.query.execute("INSERT INTO `ocorrencias` (`numero`, `dt_abertura`, `dt_fechamento`, `h_abertura`, `h_fechamento`, `n_usuario`, `descricao`, `historico`, `operador`, `n_tecnico`, `encaminhamentos`, `tipo`, `valor`, `anotacao`, `fec_por`, `idempresa`, `dt_agendamento`) "
                           "VALUES ('1211000121426','2014-11-12','2014-12-25','00:01:48','11:12:13','12','valar morghulis',NULL,'sugarCRM','1',NULL,'Outros',0,NULL,NULL,'1',NULL)")

    def test_insercao(self):
        a = Atendimentos(self.query)
        dados = {'n_usuario': 2,
                 'descricao': 'Testando um novo problema'}
        retorno = a.insert(dados)
        self.assertEqual('2', retorno['n_usuario'])

    def test_insercao2(self):
        a = Atendimentos(self.query)
        dados = {
            'n_usuario': 12,
            'descricao': 'teste de insercao',
            'dt_abertura': datetime.datetime(2014, 1, 1),
        }
        retorno = a.insert(dados)
        self.assertEqual('010100012', retorno['numero'][0:9])
        self.assertEqual(datetime.date(2014, 1, 1), retorno['dt_abertura'])

    def test_atualizacao_chamado(self):
        a = Atendimentos(self.query)
        dados = {'numero': '1211000121426',
                 'descricao': 'valar dohaeris',
                 'n_usuario': 2308,
                 'dt_fechamento': datetime.datetime(2014, 12, 25),
                 'h_fechamento': '11:12:13'}
        retorno = a.update(dados)
        self.assertEqual('valar dohaeris', retorno['descricao'])

if __name__=="__main__":
    unittest.main()

