import bottle
import vigo
from database import plugin
from bottle import request, response
from cors import EnableCors
from serializers import json_serial
import json

app = bottle.Bottle()
app.install(EnableCors())
app.install(plugin)

@app.route("/clientes", method="GET")
def listar_clientes(db):
    response.content_type = 'application/json'
    clientes = vigo.Clientes(db)
    return json.dumps(clientes.json(), default=json_serial)

@app.route('/clientes/<id:int>', method='GET')
def obter_cliente(id, db):
    response.content_type = 'application/json'
    clientes = vigo.Clientes(db)
    return json.dumps(clientes.find_by_id(id), default=json_serial)

@app.route("/clientes", method="POST")
def novo_cliente(db):
    response.content_type = 'application/json'
    clientes = vigo.Clientes(db)
    try:
        retorno = clientes.insert(request.json)
    except vigo.clientes.ENumeroInvalido as e:
        response.status = e.code
        return {"errors": [{"code": e.code, "description": e.message}]} 
    return json.dumps(retorno, default=json_serial)

@app.route("/clientes/<numero:int>", method="PUT")
def atualizar_cliente(numero, db):
    response.content_type = 'application/json'
    clientes = vigo.Clientes(db)
    retorno = clientes.update(numero, request.json)
    return json.dumps(retorno, default=json_serial)

@app.route('/clientes/<id:int>', method='DELETE')
def remover_cliente(id, db):
    clientes = vigo.Clientes(db)
    try:
        clientes.delete(id)
    except vigo.DeleteError as e:
        response.status = e.code
        return {"errors": [{"code": e.code, "description": e.message}]} 

@app.route("/chamados", method="GET")
def listar_atendimentos(db):
    response.content_type = 'application/json'
    atendimentos = vigo.Atendimentos(db)
    return json.dumps(atendimentos.all(), default=json_serial, encoding='latin1')

@app.route("/chamados/<numero>", method="GET")
def chamado_por_numero(numero, db):
    response.content_type = 'application/json'
    atendimento = vigo.Atendimentos(db)
    return json.dumps(atendimento.find_by_numero_os(numero), default=json_serial)

@app.route("/chamados", method="POST")
def inserir_atendimento(db):
    response.content_type = 'application/json'
    atendimento = vigo.Atendimentos(db)
    retorno = atendimento.insert(request.json)
    return json.dumps(retorno, default=json_serial)

@app.route("/chamados/<numero>", method="PUT")
def altera_chamado(numero, db):
    response.content_type = 'application/json'
    atendimento = vigo.Atendimentos(db)
    retorno = atendimento.update(numero, request.json)
    return json.dumps(retorno, default=json_serial)

@app.route("/chamados/<numero>", method="DELETE")
def remove_chamado(numero, db):
    response.content_type = 'application/json'
    atendimento = vigo.Atendimentos(db)
    try:
        retorno = atendimento.delete(numero)
    except vigo.DeleteError as e:
        response.status = e.code
        return {"errors": [{"code": e.code, "description": e.message}]} 
    return json.dumps(retorno, default=json_serial)

if __name__=="__main__":
    bottle.debug(True)
    app.run()

