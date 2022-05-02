
#Ahora se va buscar la cantidad de mensajes por empresa
for m2 in mensajes:
#Se recorren las empresas, si las hay, si no hay se toma el mensaje como referencia para crear una
if len(empresas) == 0:
    nuevo = empresa(m2.empresa)
    empresas.append(nuevo)
#Si no esta vacia, entonces:
else:
    #Se hace un ciclo de busqueda
    busqueda = 0
    for em in empresas: 
        #Si se encuentra, entonces el total de la empresa se sumara en 1 y se valida el tipo de mensaje
        if em.nombre == m2.empresa:
            em.total +=1
            if m2.tipo == 'POSITIVO':
                em.positivo += 1
            elif m2.tipo == 'NEGATIVO':
                em.negativo += 1
            elif m2.tipo == 'NEUTRAL':
                em.neutral += 1
            #Ya con esto se hace lo mismo con el servicio
            for service in em.servicios:
                if service.nombre == m2.servicio:
                    service.total += 1 
                    if m2.tipo == 'POSITIVO':
                        service.positivo += 1
                    elif m2.tipo == 'NEGATIVO':
                        service.negativo += 1
                    elif m2.tipo == 'NEUTRAL':
                        service.neutral += 1