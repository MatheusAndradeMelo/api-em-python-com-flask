from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
import psycopg2
from config_json import *

# path /hoteis?cidade=Rio de janeiro&estrelas_min=4&diaria_max=400

path_params = reqparse.RequestParser
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=Float )
path_params.add_argument('estrelas_max', type=Float )
path_params.add_argument('diaria_min', type=Float )
path_params.add_argument('diaria_max', type=Float )
# quantidade de items que a gente quer exibir por pág
path_params.add_argument('limit', type=Float )
# quantidade de elementos que desejamos pular
path_params.add_argument('offset', type=Float )

# recurso da api
class Hoteis(Resource):
    # requisicao pra leitura dos hoteis
    def get(self):
        
        connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
        cursor = connection.cursor()
        
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        
        # se existir cidade faz uma consulta no banco
        # substituido estrelas_min, estrelas_max, diaria_min, diaria_max, limit, offset por "?"
        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta_sem_cidade, tupla )
            resultado = cursor.fetchall()
        else:
            # consulta contendo cidade
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta_com_cidade, tupla )
            resultado = cursor.fetchall()
        
        hoteis = []
        if resultado:
            for linha in resultado:
                hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
                })    
        
        return {'hoteis': hoteis} # Select * from Hoteis
    
class Hotel(Resource):
    # selecionando argumentos especificos para aceitar na requisição
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="This field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=float, required=True, help="This field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria', type=float, required=True, help="This field 'diaria' cannot be left blank")
    atributos.add_argument('cidade', type=str, required=True, help="This field 'cidade' cannot be left blank")
    atributos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")
    
    # método get para mostrar um hotel
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found
    
    # método post pra inserir um novo hotel
    @jwt_required # Precisa estar logado
    def post(self, hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad request
        
        # adicionando um construtor
        dados = Hotel.argumentos.parse_args()
        # criando um novo hotel
        hotel = HotelModel(hotel_id, **dados)
        
        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site_id'}, 400 # bad request
        
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Internal server error
        return hotel.json()
        
        
    # método para atualizar um hotel
    @jwt_required # Precisa estar logado
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 #Ok
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Internal server error
        return hotel.json(), 201 #Created
    
    # método para deletar um hotel
    @jwt_required # Precisa estar logado
    def delete(self, hotel_id):
        # global para o python não achar que a várivael hoteis foi criada neste momento e já está sendo usada
        #global hoteis
       hotel = HotelModel.find_hotel(hotel_id)
       if hotel:
           try:
                hotel.delete_hotel()
           except:
               return {'message': 'An error ocurred trying to delete hotel.'}, 500
                
           return {'message': 'Hotel deleted.'}
       return {'message': 'Hotel not found.'}, 404
