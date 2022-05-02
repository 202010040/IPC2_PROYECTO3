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
            m.fecha = datetime.strptime(m.fecha + " " + m.hora, '%d/%m/%Y %H:%M')
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



        
