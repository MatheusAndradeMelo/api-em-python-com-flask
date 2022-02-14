from flask_restful import Resource, reqparse

from models.HotelModel import HotelModel

#lista de hoteis
hoteis = [
    {
    'hotel_id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'Rio de janeiro'
    },
    {
    'hotel_id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 4.4,
    'diaria': 380.90,
    'cidade': 'Teresópolis'
    },
    {
    'hotel_id': 'charlie',
    'nome': 'Charlie Hotel',
    'estrelas': 3.9,
    'diaria': 320.20,
    'cidade': 'Niterói'
    },
    
    ]

# recurso da api
class Hoteis(Resource):
    
    # requisicao pra leitura
    def get(self):
        return {'hoteis': hoteis}
    
class Hotel(Resource):
    # selecionando argumentos especificos para aceitar na requisição
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    # verifica se o hotel já existe
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return print('Hotel não existe.')
    
    # método get para mostrar um hotel
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404 # not found
    
    # método post pra inserir um novo hotel
    def post(self, hotel_id):
        # adicionando um construtor
        dados = Hotel.argumentos.parse_args()
        # criando um novo hotel
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        # adicionando o novo hotel na lista de hoteis
        hoteis.append(novo_hotel)
        return novo_hotel, 201 #Created
    
    # método para atualizar um hotel
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 #Ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201 #Created
    
    # método para deletar um hotel
    def delete(self, hotel_id):
        # global para o python não achar que a várivael hoteis foi criada neste momento e já está sendo usada
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}
