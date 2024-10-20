from solucion_reticulado import Coordenadas_H, Coordenadas_V
from sympy import symbols, Eq, solve

#Quiero obtener el desplazamiento en el nodo D = I
#Para obtener el desplazamiento vertical impongo una fuerza virtual igual a 1
barras = {'AB': 0, 'AL': 0, 'LK': 0, 'LB': 0, 'BC': 0, 'BK': 0, 'KJ': 0, 'JC': 0, 'JI': 0, 'CI': 0, 'IH': 0, 'IE': 0, 'HE': 0, 'HG': 0, 'GE': 0, 'GF': 0, 'EF': 0}  # En m
#Debo conocer que barras experimentan un esfuerzo de esta manera

Fuerzas_V_V = {'A': 0, 'L': 0, 'B': 0, 'K': 0, 'C': 0, 'J': 0, 'I': -1, 'E': 0, 'H': 0, 'F': 0, 'G': 0}
Fuerzas_H_V = {'A': 0, 'L': 0, 'B': 0, 'K': 0, 'C': 0, 'J': 0, 'I': 0, 'E': 0, 'H': 0, 'F': 0, 'G': 0}

#De esta manera, puedo calcular las reacciones en los nodos
Va, Vf, Ha, Hf = symbols('Va Vf Ha Hf')

# Diccionarios para reacciones
Reacciones_V = {'A': Va, 'F': Vf}
Reacciones_H = {'A': Ha, 'F': Hf}

# Ecuación de equilibrio de fuerzas verticales
R_V_total = sum(Fuerzas_V_V.values())  # Sumar todas las fuerzas externas verticales

# Calcular el momento en torno a A (M_A)
M_A = 0
# Agregar los momentos generados por las fuerzas verticales externas
for i in Fuerzas_V_V.keys():
    M_A -= Fuerzas_V_V[i] * Coordenadas_H[i]  # Momento de las fuerzas en torno a A

# Considerar el momento generado por la reacción vertical en F
M_A -= Reacciones_V['F'] * Coordenadas_H['F']

# Considerar el momento generado por la reacción horizontal en F
M_A -= Reacciones_H['F'] * Coordenadas_V['F']

# Ecuación de momento en torno a A
ecuacion_momento_A = Eq(M_A, 0)

# Ahora, calcular el momento en torno a I (M_I)
M_I = 0
# Agregar los momentos generados por las fuerzas externas en nodos relevantes
Nodos_actuantes = ['H', 'G', 'F']  # Evitamos duplicados innecesarios

for nodo in Nodos_actuantes:
    M_I -= Fuerzas_V_V[nodo] * (Coordenadas_H[nodo]-Coordenadas_H['I'])

# Considerar el momento generado por la reacción vertical en F
M_I -= Reacciones_V['F'] * (Coordenadas_H['F']-Coordenadas_H['I'])

# Considerar el momento generado por la reacción horizontal en F
M_I -= Reacciones_H['F'] * (Coordenadas_V['F']-Coordenadas_V['I'])

# Ecuación de momento en torno a I
ecuacion_momento_I = Eq(M_I, 0)

print(f'{ecuacion_momento_A=}')
print(f'{ecuacion_momento_I=}')
# Resolver el sistema de ecuaciones para las reacciones
soluciones = (solve([ecuacion_momento_A, ecuacion_momento_I], [Hf, Vf]))
Hf = soluciones[Hf]*-1 #por como se define el enunciado
Vf = soluciones[Vf]
print(f'{Hf=}, {Vf=}')

# Ecuación de fuerzas verticales: Va + Vf = R_V_total
ecuacion_fuerzas_verticales = Eq(Reacciones_V['A'] - Vf, R_V_total)

# Ecuación de fuerzas horizontales: Ha + Hf = 0
ecuacion_fuerzas_horizontales = Eq(Reacciones_H['A'] + Hf, 0)

# Resolver para Ha y Va
Ha = solve(ecuacion_fuerzas_horizontales, Ha)[0]
Va = solve(ecuacion_fuerzas_verticales, Va)[0]*-1

# Imprimir las soluciones
print(f'{Ha=}, {Va=}')

#Guardo las soluciones
Fuerzas_V_V['A'] = Va
Fuerzas_V_V['F'] = Vf
Fuerzas_H_V['A'] = Ha
Fuerzas_H_V['F'] = Hf


#Perfecto, ahora puedo calcular todas las barras que experimentan un esfuerzo horizontal
#Para esto, debo calcular las fuerzas en las barras

#Para el nodo A
def proyeccion_H (nodo1, nodo2):
    largo_barra = ((Coordenadas_H[nodo2] - Coordenadas_H[nodo1])**2 + (Coordenadas_V[nodo2] - Coordenadas_V[nodo1])**2)**0.5
    cateto_A = abs(Coordenadas_H[nodo2] - Coordenadas_H[nodo1])
    
    if abs(Coordenadas_V[nodo2] - Coordenadas_V[nodo1]) == 0:
        return 1
    return (cateto_A/largo_barra)

def proyeccion_V (nodo1, nodo2):  
    largo_barra = ((Coordenadas_H[nodo2] - Coordenadas_H[nodo1])**2 + (Coordenadas_V[nodo2] - Coordenadas_V[nodo1])**2)**0.5
    cateto_O = abs(Coordenadas_V[nodo2] - Coordenadas_V[nodo1])

    if abs(Coordenadas_H[nodo2] - Coordenadas_H[nodo1]) == 0:
        return 1
    return (cateto_O/largo_barra)


#Voy con el nodo F
EF = symbols('EF')

#Suma vertical de fuerzas
Suma_V = Fuerzas_V_V['F']
#Agrego las proyecciones de las barras
Suma_V += EF*proyeccion_V('E', 'F')

#Ecuación de equilibrio vertical
ecuacion_V = Eq(Suma_V, 0)

soluciones = solve(ecuacion_V, EF)
print(f'EF = {soluciones[0]}')

#guardo la solución
barras['EF'] = soluciones[0]*-1

#AHora voy con el nodo E
IE = symbols('IE')  

#Suma vertical de fuerzas
Suma_V = Fuerzas_V_V['E']
#Agrego las proyecciones de las barras
Suma_V += IE*proyeccion_V('I', 'E') + EF*proyeccion_V('F', 'E')

#Ecuación de equilibrio vertical
ecuacion_V = Eq(Suma_V, 0)

soluciones = solve(ecuacion_V, IE)
print(f'IE = {soluciones[0]}')




#Ahora importo los esfuerzos reales
from solucion_reticulado import barras as esfuerzo_barras_r
print('------------------')
print(barras)
print(esfuerzo_barras_r)

#Bien, ahora hago la sumatoria
def largo(barra):
    return ((Coordenadas_H[barra[0]] - Coordenadas_H[barra[1]])**2 + (Coordenadas_V[barra[0]] - Coordenadas_V[barra[1]])**2)**0.5


desplazamiento_vertical = 0
for barra in barras:
    desplazamiento_vertical += (esfuerzo_barras_r[barra] * barras[barra] * largo(barra))/(210000*559.399)
                                                                       #Asumo una barra de diametro 10 y 28.5)

print(desplazamiento_vertical)                                                                       