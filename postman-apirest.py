### This code was make to consume Flask API REST with MongoEngine


# imports
import requests
import json
from bson import json_util


# logs
import logging
logging.basicConfig(level=logging.DEBUG)


# requests optimal settings
url_api="http://127.0.0.1/api/"
nodo_adapter = requests.adapters.HTTPAdapter(max_retries=0,pool_maxsize=10,pool_connections=10,pool_block=False)
sessioner = requests.Session()
sessioner.mount(url_api, nodo_adapter)


# get all data from collection
def gettingAll(entity):
    try:
        response = sessioner.get(url_api+entity, timeout=(1,1))
        if response.status_code == 200 :
            bulk=json.loads(json_util.dumps(response.json()), object_hook=json_util.object_hook)
            return bulk
    except requests.exceptions.ConnectionError:
        logging.debug("Error de conexión")
    except requests.exceptions.ReadTimeout:
        logging.debug("Respuesta tarda demasiado")
    except:
        logging.exception("*** Ha ocurrido un error:")


# post document
def posting(entity, obj_dict):
    try:
        response = sessioner.post(url_api+entity,json=obj_dict, timeout=(1,1))
        if response.status_code == 200 :
            obj_dict['_id'] = response.json()['id']
            return obj_dict
    except requests.exceptions.ConnectionError:
        logging.debug("Error de conexión")
    except requests.exceptions.ReadTimeout:
        logging.debug("Respuesta tarda demasiado")
    except:
        logging.exception("*** Ha ocurrido un error:")


#########


# put document
def putting(entity, obj_dict):
    try:
        id = obj_dict['_id']
        del obj_dict['_id']
        response = sessioner.put(url_api+entity+"/"+id,json=obj_dict, timeout=(1,1))
        if response.status_code == 200 :
            obj_dict['_id'] = id
            return obj_dict
    except requests.exceptions.ConnectionError:
        logging.debug("Error de conexión")
    except requests.exceptions.ReadTimeout:
        logging.debug("Respuesta tarda demasiado")
    except:
        logging.exception("*** Ha ocurrido un error:")


# get one document
def getting(entity, ide):
    try:
        response = sessioner.get(url_api+entity+"/"+ide, timeout=(1,1))
        if response.status_code == 200 :
            data = json.loads(json_util.dumps(response.json()), object_hook=json_util.object_hook)
            return data
    except requests.exceptions.ConnectionError:
        logging.debug("Error de conexión")
    except requests.exceptions.ReadTimeout:
        logging.debug("Respuesta tarda demasiado")
    except:
        logging.exception("*** Ha ocurrido un error:")


#DELETE
def deleting(entity, obj_dict):
    id = obj_dict['_id']
    try:
        response = sessioner.delete(url_api+entity+"/"+str(id), timeout=(1,1))
        if response.status_code == 200 :
            return "Eliminado"
    except requests.exceptions.ConnectionError:
        logging.debug("Error de conexión")
    except requests.exceptions.ReadTimeout:
        logging.debug("Respuesta tarda demasiado")
    except:
        logging.exception("*** Ha ocurrido un error:")
