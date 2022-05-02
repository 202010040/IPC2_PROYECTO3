from ast import alias
from xml.etree import ElementTree as ET
import xmltodict, json
from mensaje import Mensaje

#FUNCION QUEREEMPLAZA LAS TILDES Y LAS VUELVE MAYUSCULAS
def tilde (text):
    text2 = text.upper()
    reemplazos = (
        ('Á', 'A'),
        ('É', 'E'),
        ('Í', 'I'),
        ('Ó', 'O'),
        ('Ú', 'U'),
        ('Ã¡', 'A'),
        ('Ã©', 'E'),
        ('Ã\xad', 'I'),
        ('Ã³', 'O'),
        ('Ãº', 'U'),
    )
    for a, b in reemplazos:
        text2 = text2.replace(a,b)
    return (text2)

#AQUI OCURRRE LA MAGIA
def ClasificarXml(xml):
    #PRIMERO CREAMOS LAS LISTAS DEFINITIVAS, ESTAS SE LLENARAN DE ULTIMO CONFORME SE VAYAN
    SentimientosPositivos=[]
    SentimientosNegativos=[]
    mensajes = []

    #PARSEA EL ARCHIVO A DICCIONARIO
    obj = xmltodict.parse(xml,encoding="utf-8")

    #SE HACE UN ARREGLO DE COSAS TOMANDO COMO BASE EL DICCIONARIO QUE ACABAMOS DE CREAR
    SentimientosPositivos = obj['solicitud_clasificacion']['diccionario']['sentimientos_positivos']['palabra']
    SentimientosNegativos = obj['solicitud_clasificacion']['diccionario']['sentimientos_negativos']['palabra']
    Empresas = obj['solicitud_clasificacion']['diccionario']['empresas_analizar']['empresa']
    ListaMensajes = obj['solicitud_clasificacion']['lista_mensajes']['mensaje']

    #LISTA TEMPORAL DE MENSAJES, LUEGO LOS CLASIFICAREMOS
    tempMensajes = []
    #LLENAMOS LA LISTA TEMPORAL
    for mensaje in ListaMensajes:
        temp2 = []
        mensaje2 = mensaje.upper().split(' ') #TAMBIEN HAY QUE ELIMINAR TILDES Y ESPACIOS
        for men2 in mensaje2:
            if men2 != '\n':
                temp2.append(men2)
        tempMensajes.append(temp2)
    #CLASIFICAMOS LOS MENSAJES
    for mensaje in tempMensajes:
        #Variables temporales, para crear un objeto mensaje
        lugar = ''
        fecha = ''
        hora = ''
        user = ''
        red = ''
        mensaje0 = []
        #Ahora, con ayuda de un iterador se llenan los campos
        i = 0
        for palabra in mensaje:
            if i == 3:
                lugar = tilde(palabra)
            elif i == 4:
                fecha = palabra
            elif i == 5:
                hora = palabra
            elif i == 7:
                user = tilde(palabra)
            elif i == 10:
                red = tilde(palabra)
            elif i >= 11:
                mensaje0.append(tilde(palabra))
            i+=1    
        #Con las variables temporales llenadas, podemos crear un objeto de tipo mensaje
        nuevo = Mensaje(lugar, fecha, hora, user, red, mensaje0)
        #Se agrega al listado de mensajes
        mensajes.append(nuevo)
    #AHORA ES TURNO DE BUSCAR LAS PALABRAS BUSCADAS
    #Ciclo que recorre los textos de mesaje
    for i in mensajes:
        #Iterador de mensajes positivos
        Positivos = 0
        #Ciclo que recorre las palabras clave
        for j in SentimientosPositivos:
            #Como i.contenido es una lista, entonces se debe recorrer
            for content in i.contenido:
                ##Si una palabra clave se encuentra en el texto, se sumara el iterdor de mensajes positivos, reueden quitar puntos y comas
                if tilde(j) in content:
                    Positivos += 1
        i.positivos = (Positivos)
    #Se procede igual con los negativos
    for i in mensajes:
        #Iterador de mensajes negativos
        Negativos = 0
        #Ciclo que recorre las palabras clave
        for j in SentimientosNegativos:
            #Como i.contenido es una lista, entonces se debe recorrer
            for content in i.contenido:
                ##Si una palabra clave se encuentra en el texto, se sumara el iterdor de mensajes negativos, reueden quitar puntos y comas
                if tilde(j) in content:
                    Negativos += 1
        i.negativos = (Negativos)


    #3USCA EL SERVICIO Y LA EMPRESA
    #Ciclo para recorrer los mensajes
    for m in mensajes:
        m.clasificarMensaje()
        #Por cada mensaje recorre las empresas
        for i in Empresas:
            #Si la empresa se menciona en el mensaje, entonces sera de la empresa el mensaje:
            tempcontenido = ''
            #Se concatena y luego se busca la empresa
            for content in m.contenido:
                tempcontenido += content
                tempcontenido += " "
            if (tilde(i['nombre'])) in tempcontenido:
                    m.empresa = (tilde(i['nombre']))
            #Luego, se buscara el servicio asignado
            #La unica diferencia es que ya busca dento de los servicios disponibles en la empresa, y como estan en el mismo orden, no hay pierde
            #Se recorren los servicios
            for service in i['servicio']:
                #Algunas no tienen alias, por eso se usa un try catch
                try:
                    #Se usa type para saber si es lista o cadena, de ello dependera si se recorre o solo se asigna
                    if (type(service['alias'])) == list:
                        for alia in (service['alias']):
                            if tilde(alia) in tilde(tempcontenido):
                                m.servicio = tilde(service['@nombre'])
                    elif (type(service['alias'])) == str:
                        if tilde(service['alias']) in tempcontenido:
                                m.servicio = tilde(service['@nombre'])
                except:
                    if tilde(service['@nombre']) in tempcontenido:
                        m.servicio = tilde(service['@nombre'])
    return (mensajes)
