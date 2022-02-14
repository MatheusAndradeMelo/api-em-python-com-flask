from flask_restful import Resource

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
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'Hotel not found.'}, 404 # not found
    
    def post(self, hotel_id):
        pass
    
    def put(self, hotel_id):
        pass
    
    def delete(self, hotel_id):
        pass
