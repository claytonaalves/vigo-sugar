import bottle
import vigo
import json
from contrib import bottle_mysql
from bottle import request, response
from serializers import json_serial
from cors import EnableCors

app = bottle.Bottle()
plugin = bottle_mysql.Plugin(dbuser="root", dbpass="", dbname="vigo_teste", charset="latin1")

app.install(EnableCors())
app.install(plugin)

# Criar um novo cliente
# POST		https://servidor_vigo/api/clientes
@app.route("/clientes", method="POST")
def novo_cliente(db):
    clientes = vigo.Clientes(db)
    try:
        clientes.insert(request.json)
    except vigo.ENumeroInvalido as e:
        response.status = e.code
        return {"errors": [{"code": e.code, "description": e.message}]} 

# Recuperar cliente existente
# GET		https://servidor_vigo/api/clientes/{ID_DO_CLIENTE}
@app.route('/clientes/<id:int>', method='GET')
def obter_cliente(id, db):
    db.execute('select * from usuarios where numero=%s', (id, ))
    return json.dumps(db.fetchone(), default=json_serial, encoding='latin1')

# Atualizar cliente
# POST		https://servidor_vigo/api/clientes/{ID_DO_CLIENTE}
@app.route('/clientes/<id:int>', method='POST')
def atualizar_cliente(id, db):
    pass

# Remover cliente
# DELETE	https://servidor_vigo/api/clientes/{ID_DO_CLIENTE}
@app.route('/clientes/<id:int>', method='DELETE')
def remover_cliente(id, db):
    clientes = vigo.Clientes(db)
    try:
        clientes.delete(id)
    except vigo.DeleteError as e:
        response.status = e.code
        return {"errors": [{"code": e.code, "description": e.message}]} 

# Listar clientes
# GET		https://servidor_vigo/api/clientes
@app.route("/clientes", method="GET")
def listar_clientes(db):
    clientes = vigo.Clientes(db)
    return clientes.json()

if __name__=="__main__":
    bottle.debug(True)
    app.run()

