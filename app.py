from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

# iniciando o flask
app = Flask(__name__)

#faz todo geranciamento da api
api = Api(app)

# adicionando o recurso para a api
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# configuração básica do flask
if __name__ == 'main':
    # após finalizar a api mudar pra false ou retirar
    app.run(debug=True)
    
# testar aplicação python app.py