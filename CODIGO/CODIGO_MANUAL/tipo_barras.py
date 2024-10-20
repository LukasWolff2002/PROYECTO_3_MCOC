from solucion_reticulado import barras as esfuerzo_barras, Coordenadas_H, Coordenadas_V
print('')


#Algunos parametros del acero a utilizar
#Se utilizara un acero A630-420H
Fluencia = 210 #MPa
Resistencia = 440 #MPa
E = 200000 #GPa
#https://barracamyc.cl/2024/03/05/todo-lo-que-necesitas-saber-sobre-los-fierros-de-construccion/

barras = {'AB': 0, 'AL': 0, 'LK': 0, 'LB': 0, 'BC': 0, 'BK': 0, 'KJ': 0, 'JC': 0, 'JI': 0, 'CI': 0, 'IH': 0, 'IE': 0, 'HE': 0, 'HG': 0, 'GE': 0, 'GF': 0, 'EF': 0}  # En m

#Aqui la nomenclatura es (Diametro interno, Diametro externo)
secciones_barras = {'AB': (10,20), 'AL': (10,20), 'LK': (10,20), 'LB': (10,20), 'BC': (10,20), 'BK': (10,20), 'KJ': (10,20), 'JC': (10,20), 'JI': (10,20), 'CI': (10,20), 'IH': (10,20), 'IE': (10,20), 'HE': (10,20), 'HG': (10,20), 'GE': (10,20), 'GF': (10,20), 'EF': (10,20)}

#Primero calculemos el area de cada barra
def area (seccion):
    return (3.14159/4)*(seccion[1]**2 - seccion[0]**2)

#Ahora la inercia
def inercia (seccion):
    return (3.14159/64)*(seccion[1]**4 - seccion[0]**4)

#Ahora la rigidez
def rigidez (seccion, E):
    return E*inercia(seccion)

#Revisemos que cada seccion soporte la fluencia
def fluencia (barra):
    esfuerzo = esfuerzo_barras[barra] *1000
    A = area(secciones_barras[barra]) 
    return esfuerzo/A #Tengo N/mm2

tensiones_barras = {}

for secciones in secciones_barras:
    #print('La barra', secciones, 'tiene un area de', area(secciones_barras[secciones]), 'mm^2, una inercia de', inercia(secciones_barras[secciones]), 'mm^4 y una rigidez de', rigidez(secciones_barras[secciones], E), 'KN/mm^2')
    tension = fluencia(secciones)
    if tension > Fluencia/1.3:
        #print('Modifico el area')
        while tension > Fluencia/1.3:
            secciones_barras[secciones] = (secciones_barras[secciones][0], secciones_barras[secciones][1] + 0.5)
            tension = fluencia(secciones)
            #print(tension)

    tensiones_barras[secciones] = tension

print('Ninguna barra falla por fluencia')

    #print(tension, area(secciones_barras[secciones]), secciones_barras[secciones])

#Bien, ahora debo comprobar que ninguna barra falle por pandeo
#Para esto, debo calcular la longitud efectiva de pandeo de cada barra

pcrit_barras = {}

def Pcr (barra):
    largo = (((Coordenadas_H[barra[0]] - Coordenadas_H[barra[1]])**2 + (Coordenadas_V[barra[0]] - Coordenadas_V[barra[1]])**2)**0.5)*1000
    I = inercia(secciones_barras[barra])
    return 3.14159**2*E*I/(largo**2)

for barra in barras:
    if esfuerzo_barras[barra] > Pcr(barra)/1.3:
        print('La barra', barra, 'falla por pandeo')

    pcrit_barras[barra] = Pcr(barra)

print('Ninguna barra falla por pandeo')
print('')

#De esta forma, los resultados finales son

print(esfuerzo_barras)
print(secciones_barras)
print(tensiones_barras)
print(pcrit_barras)

FS_tension = {}
for tension in tensiones_barras:
    FS_tension[tension] = Fluencia/tensiones_barras[tension]

FS_pandeo = {}
for pandeo in pcrit_barras:
    FS_pandeo[pandeo] = pcrit_barras[pandeo]/esfuerzo_barras[pandeo]

print('')
print(FS_tension)
print(FS_pandeo)




    












    