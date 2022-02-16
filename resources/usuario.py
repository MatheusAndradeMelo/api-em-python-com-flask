from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

from models.usuario import UsuarioModel

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field login cannot be left blank.')
atributos.add_argument('senha', type=str, required=True, help='The field senha cannot be left blank.')

class Usuario(Resource):
   
    # método get para mostrar um usuario /usuarios/{user_id}
    def get(self, user_id):
        usuario = UsuarioModel.find_user(user_id)
        if usuario:
            return usuario.json()
        return {'message': 'User not found.'}, 404 # not found
    
    # método para deletar um usuario
    @jwt_required
    def delete(self, user_id):
       usuario = UsuarioModel.find_user(user_id)
       if usuario:
           try:
                usuario.delete_user()
           except:
               return {'message': 'An error ocurred trying to delete user.'}, 500
                
           return {'message': 'User deleted.'}
       return {'message': 'User not found.'}, 404
   
class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        
        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'The login {} already exists.'.format(dados['login'])}
        
        user = UsuarioModel(**dados)
        user.save_user()
        return {'message': 'User created successfully.'}, 201 #Created
    
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UsuarioModel.find_by_login(dados['login'])
        
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401
    
# instalar o jwt - pip install Flask-JWT-Extended

class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # Identificador do token
        BLACKLIST.add(jwt_id)
        return {'message': 'Logge out successfuly.'}, 200
            