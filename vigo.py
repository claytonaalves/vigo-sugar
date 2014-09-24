#coding: utf8
import json
from serializers import json_serial

class CustomException(Exception):

    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code

class ENumeroInvalido(CustomException):
    pass

class DeleteError(CustomException):
    pass

class RequiredFieldsError(CustomException):
    pass

class DatabaseError(CustomException):
    pass

class Clientes:

    def __init__(self, db):
        self.db = db

    def json(self):
        self.db.execute('select %s from usuarios' % self.columns)
        return json.dumps(self.db.fetchall(), default=json_serial, encoding='latin1')

    def insert(self, json_object):
        # valida se os campos obrigatorios foram informados
        if not json_object.has_key('numero'):
            raise RequiredFieldsError('Campo numero obrigatorio!', 405) 
        if not json_object.has_key('nome'):
            raise RequiredFieldsError('Campo nome obrigatorio!', 405)

        columns = json_object.keys()
        insert_query = 'replace into usuarios (%s) values (%s)'
        insert_query = insert_query % (', '.join(columns), '%s, ' * (len(columns)-1) + '%s')

        try:
            self.db.execute(insert_query, tuple(json_object.values()))
        except self.db.IntegrityError:
            raise ENumeroInvalido('Numero duplicado. Ja existe um cliente com este numero.', 401)
        except self.db.OperationalError as e:
            raise DatabaseError(e.args[1], 406)

    def update(self, json_object):
        self.insert(json_object)

    def delete(self, id):
        try:
            self.db.execute('delete from usuarios where numero=%s', (id))
        except:
            raise DeleteError('Erro ao tentar excluir cliente %s' % id, 402)
