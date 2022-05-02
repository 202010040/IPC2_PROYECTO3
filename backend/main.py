from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS
from mensaje import Mensaje
from gestor import Gestor
from xml.etree import ElementTree as ET

app = Flask(__name__)
app.config["DEBUG"]=True

CORS(app)

gestor=Gestor()

@app.route('/')
def home():
    return "Esta corriendo bien bro"

@app.route('/login/<user>/<password>')
def login(user=None,password=None):
    res = gestor.obtener_usuario(user,password)
    if res == None:
        return '{"data":false}'
    return '{"data":true}'

#Agregar cancion
@app.route('/agregarCancion',methods=['POST'])
def agregarCancion():
    json=request.get_json()
    gestor.agregar_cancion(json['name'],json['artist'],json['image'],json['album'])
    return jsonify({'ok':True, 'data':'Cancion añadida con exito'}),200

#Cargar Archivo
@app.route('/CargaMasiva',methods=['POST'])
def agregarCanciones():
    xml=request.data.decode('utf-8')
    gestor.clasificarXML(xml)
    gestor.enlistar()
    return (jsonify({'ok':True}))
    

#Obtener Canciones
@app.route('/canciones',methods=['GET'])
def get_canciones():
    c=gestor.obtener_canciones()
    return jsonify(c),200

#AQUI ESTAN LOS ENDPOINTS DE FUNCIONES
#CARGAR EL XML
@app.route("/CargaMasiva", methods = ["POST"])
def CargaMasiva ():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        gestor.recorrerXML(raiz)
    return jsonify({'ok':True, 'data':raiz.text}),200

@app.route("/CargaMasiva", methods = ["GET"])
def MostrarSalida():
    return ({'ok':False}),200

#MENU DE PETICIONES
@app.route("/peticiones", methods =["GET"] )
def MostrrPetciones ():
    if len(gestor.empresas) > 0:
        return jsonify({'data':True})
    else:
        return jsonify({'data':False})

@app.route('/consultar', methods = ['GET'])
def consultar():
    entrada = gestor.xml
    salida = gestor.retornarXML()
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    data = jsonify(data)
    return data



@app.route("/ayuda", methods = ['GET'])
def MostrarAyuda():
    return jsonify({'creador':202010040, "documentacion" : False})

#Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True)    
