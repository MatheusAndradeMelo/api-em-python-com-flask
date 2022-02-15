from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

# iniciando o flask
app = Flask(__name__)

#faz todo geranciamento da api
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' # pode substituir o caminho para outros bancos como postgresql por ex
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # para parar de ficar dando aviso

@app.before_first_request
def cria_banco():
    banco.create_all

# adicionando o recurso para a api
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# configuração básica do flask
if __name__ == 'main':
    # conexão com o banco feita nessa condição para que não venha ter um arquivo c outro nome, somente o arquivo principal
    from sql_alchemy import banco
    banco.init_app(app)
    # após finalizar a api mudar pra false ou retirar
    app.run(debug=True)
    
# testar aplicação python app.py