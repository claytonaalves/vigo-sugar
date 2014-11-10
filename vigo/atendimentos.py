#coding: utf8
import json
from serializers import json_serial
from dbexceptions import RequiredFieldsError

class Atendimentos:

    REQUIRED_FIELDS = ('id_cliente', 'descricao')

    def __init__(self, db):
        self.db = db

    def json(self):
        self.db.execute('select * from cadastro_atendimentos limit 10')
        return json.dumps(self.db.fetchall(), default=json_serial, encoding='latin1')

    def valida_campos_obrigatorios(self, json_object):
        """ valida se os campos obrigatorios foram informados
        """
        for field in self.REQUIRED_FIELDS:
            if not json_object.has_key(field):
                raise RequiredFieldsError('Campo {0} obrigatorio!'.format(field), 405) 

    def insert(self, json_object):
        self.valida_campos_obrigatorios(json_object)
        columns = json_object.keys()
        insert_query = 'insert into cadastro_atendimentos (%s) values (%s)'
        insert_query = insert_query % (', '.join(columns), '%s, ' * (len(columns)-1) + '%s')

        import pdb; pdb.set_trace()
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

    def find_by_id(self, id):
        self.db.execute('select * from usuarios where numero=%s', (id, ))
        return json.dumps(self.db.fetchone(), default=json_serial, encoding='latin1')


