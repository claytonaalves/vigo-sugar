#coding: utf8
import json
import random
from dbexceptions import RequiredFieldsError, DeleteError, DatabaseError
from datetime import date, datetime

class Atendimentos:

    def __init__(self, db):
        self.db = db

    def all(self):
        self.db.execute('select * from ocorrencias limit 10')
        return self.db.fetchall()

    def valida_campos_obrigatorios(self, campos, json_object):
        """ valida se os campos obrigatorios foram informados
        """
        for field in campos:
            if not json_object.has_key(field):
                raise RequiredFieldsError('Campo {0} obrigatorio!'.format(field), 405) 

    def gera_numero_chamado(self, chamado):
        data = chamado['dt_abertura']
        id_cliente = chamado['n_usuario']
        random_number = int(random.random()*10000)
        numero_os = "{0:02d}{1:02d}{2:05d}{3:04d}".format(data.day, data.month, id_cliente, random_number)
        return numero_os

    def insert(self, json_object):
        """ Insere um chamado no banco de dados.
            Retorna um dicionário com os dados do chamado cadastrado.
        """
        chamado = json_object
        self.valida_campos_obrigatorios(('n_usuario', 'descricao'), chamado)

        chamado['idempresa']   = 1
        chamado['dt_abertura'] = chamado.get('dt_abertura', date.today())
        chamado['h_abertura']  = chamado.get('h_abertura', datetime.now().strftime('%H:%M:%S'))
        chamado['operador']    = chamado.get('operador', 'sugarCRM')
        chamado['n_tecnico']   = chamado.get('n_tecnico', 1)
        chamado['tipo']        = chamado.get('tipo', 'Outros')
        chamado['valor']       = chamado.get('valor', 0)
        chamado['numero']      = self.gera_numero_chamado(chamado)

        columns = json_object.keys()
        insert_query = 'insert into ocorrencias (%s) values (%s)'
        insert_query = insert_query % (', '.join(columns), '%s, ' * (len(columns)-1) + '%s')
        self.execute_query(insert_query, tuple(json_object.values()))

        return self.find_by_numero_os(chamado['numero'])

    def update(self, numero_os, json_object):
        chamado = json_object

        fields = []
        for field in chamado.keys():
            fields.append('{0}=%s'.format(field))
        fields = ', '.join(fields)

        update_query = 'update ocorrencias set {0} where numero="{1}"'.format(fields, numero_os)
        self.execute_query(update_query, tuple(chamado.values()))

        return self.find_by_numero_os(numero_os)

    def delete(self, numero):
        try:
            self.db.execute('delete from ocorrencias where numero=%s', (numero))
        except:
            raise DeleteError('Erro ao tentar excluir chamado %s' % numero, 402)

        return {'msg': 'Chamado removido com sucesso!'}

    def find_by_numero_os(self, numero_os):
        """ Localiza um chamado pelo numero da OS.
        """
        self.db.execute('select * from ocorrencias where numero=%s', (numero_os, ))
        return self.db.fetchone()

    def execute_query(self, query, values):
        try:
            self.db.execute(query, values)
        except self.db.IntegrityError:
            raise ENumeroInvalido('Numero duplicado. Ja existe um chamado com este id.', 401)
        except self.db.OperationalError as e:
            raise DatabaseError(e.args[1], 406)

