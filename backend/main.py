from flask import Flask, make_response, render_template, request
from flask.json import jsonify
from flask_cors import CORS
import pdfkit
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
#Peticion de entrada y salida de xml
@app.route('/consultar', methods = ['GET'])
def consultar():
    #Se define la entrada como el XML enviado, pero lasalida como una funcion que procesa
    entrada = gestor.xml
    salida = gestor.retornarXML()
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    data = jsonify(data)
    return data

#Reporte en pedf de entrada y salida de xml
@app.route('/generarPDF1', methods = ['POST'])
def pdf1():
    if request.method == "POST":

        entrada = gestor.xml
        salida = gestor.retornarXML()
        data = {
            'entrada' : entrada,
            'salida': salida
        }
        data = jsonify(data)

        return data
#Vista general de clasificacion por fecha
@app.route('/clasificar-por-fecha', methods = ['GET','POST'])
def clasificar():
    #Si solo es un get, entondes retornara un listado de empresa para seleccionar
    if request.method == 'GET':
        #json = request.get_json()
        empresas2 = []
        for em in gestor.empresas:
            empresas2.append(em.nombre) 
        #Rettorna solo los nombre de las empresas
        return jsonify ({'empresas':empresas2})
    #Si es un post, entonces retornara los mensajes totales
    if request.method == 'POST':
        datos = request.json
        dictionary = gestor.clasificar_por_fecha(datos['date'], datos ['empresa'])
        print(dictionary)
        return jsonify(dictionary)

#Vista general de clasificacion por fecha
@app.route('/resumen-por-rango', methods = ['GET','POST'])
def rango():
    #Si solo es un get, entondes retornara un listado de empresa para seleccionar
    if request.method == 'GET':
        #json = request.get_json()
        empresas2 = []
        for em in gestor.empresas:
            empresas2.append(em.nombre)
        #Rettorna solo los nombre de las empresas
        return jsonify ({'empresas':empresas2})
    #Si es un post, entonces retornara los mensajes totales
    if request.method == 'POST':
        datos = request.json
        dictionary = gestor.rango_de_fechas(datos['date1'],datos['date2'] , datos ['empresa'])
        print(dictionary)
        return jsonify(dictionary)
#Reportes 2 y 3
@app.route("/reporte2", methods = ['POST'])
def reporte2 ():
    return jsonify(gestor.reporte2)
@app.route("/reporte3", methods = ['POST'])
def reporte3 ():
    return jsonify(gestor.reporte3)
@app.route("/reporte4", methods = ['POST'])
def reporte4():
    #Se define la entrada como el XML enviado, pero lasalida como una funcion que procesa
    entrada = gestor.reporte40
    salida = gestor.reporte4
    data = {
        'entrada' : entrada,
        'salida': salida
    }
    data = jsonify(data)
    return data


#PRUEBA DE MENSAJE
@app.route("/prueba-de-mensaje", methods = ['GET'])
def prueba1():
    return ("{'ok':'True'}")

@app.route("/prueba-de-mensaje", methods = ['POST'])
def prueba2():
    xml2 = request.data.decode('utf-8')
    entrada = str(xml2)
    gestor.reporte40 = entrada
    salida = gestor.prueba_mensaje(xml2)
    return jsonify({'entrada':entrada, 'salida':salida})
    

@app.route("/ayuda", methods = ['GET'])
def MostrarAyuda():
    return jsonify({'creador':202010040, "documentacion" : False})

#Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True)    
