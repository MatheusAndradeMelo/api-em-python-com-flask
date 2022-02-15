from flask_restful import Resource, reqparse

from models.HotelModel import HotelModel

# recurso da api
class Hoteis(Resource):
    # requisicao pra leitura dos hoteis
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # Select * from Hoteis
    
class Hotel(Resource):
    # selecionando argumentos especificos para aceitar na requisição
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="This field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="This field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="This field 'diaria' cannot be left blank")
    argumentos.add_argument('cidade', type=str, required=True, help="This field 'cidade' cannot be left blank")
    
    # método get para mostrar um hotel
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found
    
    # método post pra inserir um novo hotel
    def post(self, hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad request
        
        # adicionando um construtor
        dados = Hotel.argumentos.parse_args()
        # criando um novo hotel
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Internal server error
        return hotel.json()
        
        
    # método para atualizar um hotel
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
