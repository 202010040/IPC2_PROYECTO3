from datetime import datetime
from mensaje import empresa
from mensaje import servicio
from usuario import Usuario
from mensaje import Mensaje
import json
import XMLmanager
class Gestor: 
    def __init__(self):
        self.mensajes = []
        self.empresas = []
        self.xml = []
        self.reporte40 = []
        self.reporte4 = []
        self.reporte2 = {}
        self.reporte3 = {}
        self.mensajesTotales =0
        self.TotalesPositivos = 0
        self.TotalesNegativos = 0
        self.TotalesNeutros = 0
    
    def nuevo_mensaje(self,LyF,user,red):
        new = Mensaje(LyF,user,red)
        self.mensajes.append(new)
        return True
    
    def obtener_mensajes(self):
        json=[]
        for i in self.mensajes:
            mensaje={
                'lugar':i.lugar,
                'fecha':i.fecha,
                'user':i.user,
                'red':i.red,
                'tipo':i.tipo
            }
            json.append(mensaje)
        return json

    def clasificarXML (self, xml):
        #EL metodod defindo en el otro archivo y que retorna un listado de mensajes
        self.xml = xml
        self.mensajes = XMLmanager.ClasificarXml(xml)

    #RECORRIDO PARA SUMAR TOTALES DE LOS MENSAJES
    def enlistar (self):
        #En este ciclo, vamos a contar los mensajes positivos, negativos e interesantes
        for m in self.mensajes:
            self.mensajesTotales += 1
            if m.tipo == 'POSITIVO':
                self.TotalesPositivos += 1
            elif m.tipo == 'NEGATIVO':
                self.TotalesNegativos += 1
            elif m.tipo == 'NEUTRAL':
                self.TotalesNeutros += 1
        #COVERTIR LA FECHA A FORMATO DE FECHA
            m.fecha = datetime.strptime((str(m.fecha)), "%d/%m/%Y")
        #ORDENAR LOS MENSAJES POR FECHA
        self.mensajes = sorted(self.mensajes, key= lambda x: x.fecha)

        #Ahora se va buscar la cantidad de mensajes por empresa
        for m2 in self.mensajes:
            #Si la empresa esta vacia, haz una y agregala
            if len(self.empresas) == 0:
                new = empresa(m2.empresa)
                new.total += 1
                #Ahora revisa si es positivo, negativo o neutral
                if m2.tipo == 'POSITIVO':
                    new.positivo += 1
                elif m2.tipo == 'NEGATIVO':
                    new.negativo += 1
                elif m2.tipo == 'NEUTRAL':
                    new.neutral += 1
                #Le agregamos un servicio
                nuevo = servicio(m2.servicio)
                nuevo.total += 1
                if m2.tipo == 'POSITIVO':
                    nuevo.positivo += 1
                elif m2.tipo == 'NEGATIVO':
                    nuevo.negativo += 1
                elif m2.tipo == 'NEUTRAL':
                    nuevo.neutral += 1
                #se agraga al arreglo de servicios
                new.servicios.append(nuevo)
                self.empresas.append(new)
            else:
                #Si no esta llena, entonces:
                busqueda = 0
                #Recorre las empresas
                for emp in self.empresas:
                    #Si la empresa es igal a la del mensaje, la busqueda se aumenta en uno, asi como la cantidad de mensajes de la empresa
                    if emp.nombre == m2.empresa:
                        #Aumenta la busqueda en 1 para saber que se encontro algo
                        busqueda += 1
                        emp.total += 1
                        #Ahora revisa si es positivo, negativo o neutral
                        if m2.tipo == 'POSITIVO':
                            emp.positivo += 1
                        elif m2.tipo == 'NEGATIVO':
                            emp.negativo += 1
                        elif m2.tipo == 'NEUTRAL':
                            emp.neutral += 1

                        #AHORA, ADENTRO DEL CICLO SE VALIDAN LOS SERVICIOS
                        #Si no hay ningun servicio:
                        if (len(emp.servicios)) == 0:
                            #Se crea uno y se valida su puntaje
                            nuevo = servicio(m2.servicio)
                            nuevo.total += 1
                            if m2.tipo == 'POSITIVO':
                                nuevo.positivo += 1
                            elif m2.tipo == 'NEGATIVO':
                                nuevo.negativo += 1
                            elif m2.tipo == 'NEUTRAL':
                                nuevo.neutral += 1
                            #se agraga al arreglo de servicios
                            emp.servicios.append(nuevo)
                        else:
                            #Si no esta vacio, de igual manera se crea un ciclo con una iteracion de busqueda
                            busqueda2 = 0
                            for service in emp.servicios:
                                #Se validam que esten iguales
                                if service.nombre == m2.servicio:
                                    #Se le suma la busqueda y se verifica su sentimiento
                                    busqueda2 += 1
                                    service.total += 1
                                    if m2.tipo == 'POSITIVO':
                                        service.positivo += 1
                                    elif m2.tipo == 'NEGATIVO':
                                        service.negativo += 1
                                    elif m2.tipo == 'NEUTRAL':
                                        service.neutral += 1
                            #Saliendo del for se valida si no se hallo nada de nada en los servicios
                            if busqueda2 == 0:
                                #Se crea uno y se valida su puntaje
                                nuevo = servicio(m2.servicio)
                                nuevo.total += 1
                                if m2.tipo == 'POSITIVO':
                                    nuevo.positivo += 1
                                elif m2.tipo == 'NEGATIVO':
                                    nuevo.negativo += 1
                                elif m2.tipo == 'NEUTRAL':
                                    nuevo.neutral += 1
                                #se agraga al arreglo de servicios
                                emp.servicios.append(nuevo)

                #Saliendo del for, se valida si no se hallo nada           
                if busqueda == 0:
                    #Si no se hallo nada se crea un objeto nuevo
                    new = empresa(m2.empresa)
                    new.total += 1
                    #Ahora revisa si es positivo, negativo o neutral
                    if m2.tipo == 'POSITIVO':
                        new.positivo += 1
                    elif m2.tipo == 'NEGATIVO':
                        new.negativo += 1
                    elif m2.tipo == 'NEUTRAL':
                        new.neutral += 1
                    #Le agregamos un servicio
                    nuevo = servicio(m2.servicio)
                    nuevo.total += 1
                    if m2.tipo == 'POSITIVO':
                        nuevo.positivo += 1
                    elif m2.tipo == 'NEGATIVO':
                        nuevo.negativo += 1
                    elif m2.tipo == 'NEUTRAL':
                        nuevo.neutral += 1
                    #se agraga al arreglo de servicios
                    new.servicios.append(nuevo)
                    self.empresas.append(new)

    def retornarXML(self):
        #INICIO CONCATENANDO UN TEXTO PARA VOLVERLO HTML
        #Al principio sol es de concatenar estaticamente...
        texto = '<?xml version="1.0"?>'
        texto += '\n' + '<lista_respuestas>'
        texto += '\n' + '<respuesta>'
        texto += '\n' + '<fecha>' + ' '+ str (datetime.now().date()) +' ' +'</fecha>'
        texto += '\n' + '<mensajes>'
        texto += '\n' + '<total>' + ' '+ str (self.mensajesTotales) +' ' +'</total>'
        texto += '\n' + '<positivos>' + ' '+ str (self.TotalesPositivos) +' ' +'</positivos>'
        texto += '\n' + '<negativos>' + ' '+ str (self.TotalesNegativos) +' ' +'</negativos>'
        texto += '\n' + '<neutros>' + ' '+ str (self.TotalesNeutros) +' ' +'</neutros>'
        texto += '\n' + '</mensajes>'
        texto += '\n' + '<analisis>'
        #Aqui inicia lo feo
        for em in self.empresas:
            texto += '\n' + '<empresa nombre= \"' + em.nombre + '\">'
            texto += '\n' + '<mensajes>'
            texto += '\n' + '<total>' + ' '+ str(em.total) +' ' +'</total>'
            texto += '\n' + '<positivos>' + ' '+ str(em.positivo) +' ' +'</positivos>'
            texto += '\n' + '<negativos>' + ' '+ str(em.negativo) +' ' +'</negativos>'
            texto += '\n' + '<neutros>' + ' '+ str(em.neutral) +' ' +'</neutros>'
            texto += '\n' + '</mensajes>'
            texto += '\n' + '<servicios>'
            #Ahora dentro de las empresas se iteran los servicios en las empresas
            for services in em.servicios:
                texto += '\n' + '<servicio nombre= \"' + services.nombre + '\">'
                texto += '\n' + '<mensajes>'
                texto += '\n' + '<total>' + ' '+ str(services.total) +' ' +'</total>'
                texto += '\n' + '<positivos>' + ' '+ str(services.positivo) +' ' +'</positivos>'
                texto += '\n' + '<negativos>' + ' '+ str(services.negativo) +' ' +'</negativos>'
                texto += '\n' + '<neutros>' + ' '+ str(services.neutral) +' ' +'</neutros>'
                texto += '\n' + '</mensajes>'
                texto += '\n' + '</servicio>'
            #Se acaban los servicios
            texto += '\n' + '</servicios>'
            #Se acaba la empresa
            texto += '\n' + '</empresa>'
        #Se acaban las empresas
        texto += '\n' + '</analisis>'
        texto += '\n' + '</respuesta>'
        texto += '\n' + '</lista_respuestas>'
        
        return(texto)
#CLASIFICA POR RANGO DE FECHAS
    def clasificar_por_fecha(self, fecha, empresa):
        #Se convierte la fecha a datetime, sin embargo viene en formato gringo y hay que cambiarla
        fecha = str(fecha).replace('-','/')
        fecha = datetime.strptime(fecha, "%Y/%m/%d")
        fecha = fecha.strftime("%d/%m/%Y")
        fecha = datetime.strptime(fecha, "%d/%m/%Y")
        clasificacion = []
        if empresa == 'todas':
            #Si se debe recorrer todas las empresas, entonces solo se recorreran los mensajes y se verificara lafecha
            for mensaje in self.mensajes:
                if mensaje.fecha == fecha:
                    #Ahora se verifica que la empresa exista, si existe, entonces se debe agregarle mas mensajes , si no existe se debe crear
                    busqueda1 =0 
                    #Itreacion de busqueda
                    for i in clasificacion:
                        if i['nombre'] == mensaje.empresa:
                            #Ahora, debe encontrar la fecha y la empresa 
                            #Se le sumaran 1 a sus respectivos totales
                            i['total'] += 1
                            if mensaje.tipo == 'POSITIVO':
                                i['positivos'] += 1
                            elif mensaje.tipo == 'NEGATIVO':
                                i['negativos'] += 1
                            elif mensaje.tipo == 'NEUTRAL':
                                i['neutrales'] += 1
                            busqueda1 += 1
                    #Se verifica si la iteracion de la busqueda 
                    if busqueda1 == 0:
                        positivos=0
                        negativos = 0 
                        neutros = 0
                        #Se verifica que tipo de mensaje sean
                        if mensaje.tipo == 'POSITIVO':
                            positivos += 1
                        elif mensaje.tipo == 'NEGATIVO':
                            negativos += 1
                        elif mensaje.tipo == 'NEUTRAL':
                            neutros += 1
                        #Si es nueva se agrega una empresa
                        nuevo = {
                            'nombre':mensaje.empresa,
                            'fecha': mensaje.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutrales': neutros,
                        }
                        clasificacion.append(nuevo)

        else :
            for mensaje in self.mensajes:
                
                if mensaje.fecha == fecha and mensaje.empresa == empresa:
                    print(mensaje.fecha, empresa)
                    #Ahora se verifica que la empresa exista, si existe, entonces se debe agregarle mas mensajes , si no existe se debe crear
                    busqueda1 =0 
                    #Itreacion de busqueda
                    for i in clasificacion:
                        if i['nombre'] == mensaje.empresa:
                            #Ahora, debe encontrar la fecha y la empresa 
                            #Se le sumaran 1 a sus respectivos totales
                            i['total'] += 1
                            if mensaje.tipo == 'POSITIVO':
                                i['positivos'] += 1
                            elif mensaje.tipo == 'NEGATIVO':
                                i['negativos'] += 1
                            elif mensaje.tipo == 'NEUTRAL':
                                i['neutrales'] += 1
                            busqueda1 += 1
                    #Se verifica si la iteracion de la busqueda 
                    if busqueda1 == 0:
                        print(mensaje.empresa)
                        positivos=0
                        negativos = 0 
                        neutros = 0
                        #Se verifica que tipo de mensaje sean
                        if mensaje.tipo == 'POSITIVO':
                            positivos += 1
                        elif mensaje.tipo == 'NEGATIVO':
                            negativos += 1
                        elif mensaje.tipo == 'NEUTRAL':
                            neutros += 1
                        #Si es nueva se agrega una empresa
                        nuevo = {
                            'nombre':mensaje.empresa,
                            'fecha': mensaje.fecha,
                            'total': 1,
                            'positivos': positivos,
                            'negativos': negativos,
                            'neutrales': neutros,
                        } 
                        clasificacion.append(nuevo)

        reporte2 = {
            'Listado': clasificacion,
            'fecha': fecha
        }   
        print(reporte2)
        self.reporte2 = reporte2
        return (reporte2)     
                

#RESUMEN POR RANGO DE FECHAS
    def rango_de_fechas(self, fecha1, fecha2, empresa):
        #Creamos un listado de fechas para irle agregando las fechas que encontremos
        Fechas_listado = []
        #Parseamos ambas fechas para que el formato coincida
        #Parseo de fecha1
        fecha1 = str(fecha1).replace('-','/')
        fecha1 = datetime.strptime(fecha1, "%Y/%m/%d")
        fecha1 = fecha1.strftime("%d/%m/%Y")
        fecha1 = datetime.strptime(fecha1, "%d/%m/%Y")
        #parseo de fecha2
        fecha2 = str(fecha2).replace('-','/')
        fecha2 = datetime.strptime(fecha2, "%Y/%m/%d")
        fecha2 = fecha2.strftime("%d/%m/%Y")
        fecha2 = datetime.strptime(fecha2, "%d/%m/%Y")
        #Ahora verificamos si algunas de las fechas de los mensajes estan en el rango seleccionado
        for mensaje in self.mensajes:
            if (mensaje.fecha >= fecha1) and (mensaje.fecha <= fecha2):
                    if empresa == 'todas':
                        #Se busca si la empresa ya fue egregada
                        busqueda2 = 0
                        for i in Fechas_listado:
                            if i['nombre'] == mensaje.empresa and i['fecha']== mensaje.fecha:
                                busqueda2 += 1
                        #Se verifica que la empresa sea nueva
                        if busqueda2 == 0:
                            positivos=0
                            negativos = 0 
                            neutros = 0
                            #Se verifica que tipo de mensaje sean
                            if mensaje.tipo == 'POSITIVO':
                                positivos += 1
                            elif mensaje.tipo == 'NEGATIVO':
                                negativos += 1
                            elif mensaje.tipo == 'NEUTRAL':
                                neutros += 1
                            #Si es nueva se agrega una empresa
                            nuevo = {
                                'nombre':mensaje.empresa,
                                'fecha': mensaje.fecha,
                                'total': 1,
                                'positivos': positivos,
                                'negativos': negativos,
                                'neutrales': neutros,
                            }
                            Fechas_listado.append(nuevo)
                        else:
                            #Si la empresa no es nueva se busca por empresa y fecha
                            for i in Fechas_listado:
                                if i['nombre'] == mensaje.empresa and i['fecha']== mensaje.fecha:
                                    #Se le sumaran 1 a sus respectivos totales
                                    i['total'] += 1
                                    if mensaje.tipo == 'POSITIVO':
                                        i['positivos'] += 1
                                    elif mensaje.tipo == 'NEGATIVO':
                                        i['negativos'] += 1
                                    elif mensaje.tipo == 'NEUTRAL':
                                        i['neutrales'] += 1
                    else:
                        busqueda2 = 0
                        for i in Fechas_listado:
                            if i['nombre'] == mensaje.empresa == empresa and i['fecha']== mensaje.fecha:
                                busqueda2 += 1
                            
                        if busqueda2 == 0 and mensaje.empresa == empresa:
                            positivos=0
                            negativos = 0 
                            neutros = 0
                            #Se verifica que tipo de mensaje sean
                            if mensaje.tipo == 'POSITIVO':
                                positivos += 1
                            elif mensaje.tipo == 'NEGATIVO':
                                negativos += 1
                            elif mensaje.tipo == 'NEUTRAL':
                                neutros += 1
                            #Si es nueva se agrega una empresa
                            nuevo = {
                                'nombre':empresa,
                                'fecha': mensaje.fecha,
                                'total': 1,
                                'positivos': positivos,
                                'negativos': negativos,
                                'neutrales': neutros,
                            }
                            Fechas_listado.append(nuevo)
                        else:
                            #Si la empresa no es nueva se busca por empresa y fecha
                            for i in Fechas_listado:
                                if i['nombre'] == empresa and i['fecha']== mensaje.fecha:
                                    #Se le sumaran 1 a sus respectivos totales
                                    i['total'] += 1
                                    if mensaje.tipo == 'POSITIVO':
                                        i['positivos'] += 1
                                    elif mensaje.tipo == 'NEGATIVO':
                                        i['negativos'] += 1
                                    elif mensaje.tipo == 'NEUTRAL':
                                        i['neutrales'] += 1
                        
        #Agregamos el listado a un json mas grande que vamos a retornar y recorrer en el html
        json = {
            'listado' : Fechas_listado
        }
        self.reporte3 = (json)
        return (json)

    
    
    #FUNCION PARA RETORNAR UN LISTADO DE EMPRESAS
    def retornar_empresas (self):
        #Crea un diccionario, recorre el arreglo llenandolo y luego retorna el arreglo
        dictionary = {}
        print ('hola')
        for em in self.empresas:
            print (em.nombre)
            dictionary.append(em.nombre)
        print (dictionary)
        return (dictionary)

    #pruueba de mensaje
    def prueba_mensaje(self, xml2):
        #Le mandamos el xml para que lo convierta en tipo de mensaje
        mensajePrueba = XMLmanager.PruebaMensaje(xml2)
        #Cuando obtenga un tipo de mensaje entonces se concatena para retornar un json con un texto xml
        #Este xml sera un string concatenado
        texto = '<?xml version="1.0"?>' + '\n'
        texto += '<respuesta>' + '\n'
        texto += '<fecha> ' + str(mensajePrueba.fecha) +' </fecha>' + '\n'
        texto += '<red_social> ' + str(mensajePrueba.red) +' </red_social>' + '\n'
        texto += '<usuario> ' + str(mensajePrueba.user) +' </usuario>' + '\n'
        texto += '<empresas>' '\n'
        texto += '<empresa nombre = ' + str(mensajePrueba.empresa) + ' >'  + '\n'
        texto += '<servicio> ' + str(mensajePrueba.servicio) +' </fecha>' + '\n'
        texto += '</empresa> '+ '\n'
        texto += '</empresas> '+ '\n'
        texto += '<palabras_positivas> ' + str(mensajePrueba.positivos) +' </palabras_positivas>' + '\n'
        texto += '<palabras_negativas> ' + str(mensajePrueba.negativos) +' </palabras_negativas>' + '\n'
        texto += '<sentimiento_positivo> ' + str(mensajePrueba.balancePositivo) + '%' +' </sentimiento_positivo>' + '\n'
        texto += '<sentimiento_negativo> ' + str(mensajePrueba.balanceNegativo) + '%' +' </sentimiento_negativo>' + '\n'
        texto += '<sentimiento_analizado> ' + str(mensajePrueba.tipo) + '%' +' </sentimiento_analizado>' + '\n'
        texto += '</respuesta>' + '\n'
        self.reporte4 = texto
        return (texto)



