#coding: utf8
import json
from dbexceptions import CustomException, RequiredFieldsError
from _mysql_exceptions import DatabaseError

class ENumeroInvalido(CustomException):
    pass

class Clientes:

    def __init__(self, db):
        self.db = db

    def json(self):
        self.db.execute('select * from usuarios')
        return self.db.fetchall()

    def valida_campos_obrigatorios(self, campos, json_object):
        """ valida se os campos obrigatorios foram informados
        """
        for field in campos:
            if not json_object.has_key(field):
                raise RequiredFieldsError('Campo {0} obrigatorio!'.format(field), 405) 

    def insert(self, json_object):
        self.valida_campos_obrigatorios(('nome',), json_object)

        columns = json_object.keys()
        insert_query = 'INSERT INTO usuarios (%s) VALUES (%s)'
        insert_query = insert_query % (', '.join(columns), '%s, ' * (len(columns)-1) + '%s')

        self.execute_query(insert_query, tuple(json_object.values()))
        self.db.execute('SELECT LAST_INSERT_ID() AS numero FROM usuarios')
        numero = self.db.fetchone()['numero']
        return self.find_by_id(numero)

    def update(self, numero, json_object):
        cliente = json_object

        fields = []
        for field in cliente.keys():
            fields.append('{0}=%s'.format(field))
        fields = ', '.join(fields)

        update_query = 'update usuarios set {0} where numero={1}'.format(fields, numero)
        self.execute_query(update_query, tuple(cliente.values()))

        return self.find_by_id(numero)

    def delete(self, id):
        try:
            self.db.execute('delete from usuarios where numero=%s', (id))
        except:
            raise DeleteError('Erro ao tentar excluir cliente %s' % id, 402)

    def find_by_id(self, id):
        self.db.execute('select * from usuarios where numero=%s', (id, ))
        return self.db.fetchone()

    def execute_query(self, query, values):
        try:
            return self.db.execute(query, values)
        except self.db.IntegrityError:
            raise ENumeroInvalido('Numero duplicado. Ja existe um cliente com este numero.', 401)
        except self.db.OperationalError as e:
            raise DatabaseError(e.args[1], 406)

