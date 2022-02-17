# função
def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0,**dados):
    # se tiver cidade retorna esse dicionário
    if cidade:
        return {'estrelas_min': estrelas_min,
                'estrela_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_min,
                'cidade': cidade,
                'limit': limit,
                'offset': offset}
    
    # se não tiver não vai retornar cidade
    return {'estrelas_min': estrelas_min,
                'estrela_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_min,
                'limit': limit,
                'offset': offset}
    
consulta_sem_cidade = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            LIMIT ? OFFSET ?"
            
consulta_com_cidade = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            and cidade = ? LIMIT ? OFFSET ?"
