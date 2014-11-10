import bottle
import vigo
from database import plugin
from bottle import request, response
from cors import EnableCors

app = bottle.Bottle()
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
    clientes = vigo.Clientes(db)
    return clientes.find_by_id(id)

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

