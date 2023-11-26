'''
    Crea un profesional random, tomando nombres y foto random
    desde "randomuser.me" y le asigna una especialidad'''

import json
import requests

def crea(codigo, especialidad):
    '''
    Crea un nuevo profesional '''

    response_api = requests.get(
        'https://randomuser.me/api/?nat=es&gender=female',
        timeout=3)
    api_dict = json.loads(response_api.text)["results"][0]
#    print('Api:', api_dict)
    crea_dict = {"codigo": codigo}
    crea_dict.update({"nombre": api_dict["name"]["first"]})
    crea_dict.update({"apellido": api_dict["name"]["last"]})
    crea_dict.update({"matricula": 'MN-' + str(1000 + codigo)})
    crea_dict.update({"especialidad": especialidad})
    crea_dict.update({"imagen": api_dict["picture"]["large"]})

    return crea_dict

