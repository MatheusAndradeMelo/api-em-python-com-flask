from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import UserLogin, Usuario, UserRegister, UserLogout
from flask_jwt_extended import JWTManager
from resources.site import Site, Sites

# iniciando o flask
app = Flask(__name__)

#faz todo geranciamento da api
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' # pode substituir o caminho para outros bancos como postgresql por ex
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # para parar de ficar dando aviso
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all
    
@jwt.token_in_blocklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out.'}), 401 #unauthorized


# adicionando o recurso para a api
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

# configuração básica do flask
if __name__ == 'main':
    # conexão com o banco feita nessa condição para que não venha ter um arquivo c outro nome, somente o arquivo principal
    from sql_alchemy import banco
    banco.init_app(app)
    # após finalizar a api mudar pra false ou retirar
    app.run(debug=True)
    
# testar aplicação python app.py