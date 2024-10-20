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
R_V_total = sum(Fuerzas_V_V.values())  # Sumar todas las fuerzas Vernas verticales

# Calcular el momento en torno a A (M_A)
M_A = 0
# Agregar los momentos generados por las fuerzas verticales Vernas
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
# Agregar los momentos generados por las fuerzas Vernas en nodos relevantes
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


#Vamos con el Nodo A
AB, AL = symbols('AB AL')
#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['A']
#Agrego las proyecciones de las barras
suma_V += AB*proyeccion_V('A', 'B') + AL*proyeccion_V('A', 'L')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['A']
#Agrego las proyecciones de las barras
suma_H += AB*proyeccion_H('A', 'B') + AL*proyeccion_H('A', 'L')

#Ecuacion de equilibrio en A
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [AB, AL])
print(f'{soluciones=}')

#bien, ahora actualizo las fuerzas en las barras
barras['AB'] = soluciones[AB]*-1
barras['AL'] = soluciones[AL]*-1

#Ahora voy con el nodo L
LB, LK = symbols('LB LK')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['L']
#Agrego las proyecciones de las barras
suma_V += LB*proyeccion_V('L', 'B') + LK*proyeccion_V('L', 'K') + barras['AL']*proyeccion_V('L', 'A')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['L']
#Agrego las proyecciones de las barras
suma_H += LB*proyeccion_H('L', 'B') + LK*proyeccion_H('L', 'K') + barras['AL']*proyeccion_H('L', 'A')

#Ecuacion de equilibrio en L
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [LB, LK])
print(f'{soluciones=}')

#bien, ahora actualizo las fuerzas en las barras
barras['LB'] = soluciones[LB]*-1
barras['LK'] = soluciones[LK]*-1

#Ahora voy con el nodo B
BK, BC = symbols('BK BC')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['B']
#Agrego las proyecciones de las barras
suma_V += BK*proyeccion_V('B', 'K') + BC*proyeccion_V('B', 'C') + barras['LB']*proyeccion_V('B', 'L') + barras['AB']*proyeccion_V('B', 'A')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['B']
#Agrego las proyecciones de las barras
suma_H += BK*proyeccion_H('B', 'K') + BC*proyeccion_H('B', 'C') + barras['LB']*proyeccion_H('B', 'L') + barras['AB']*proyeccion_H('B', 'A')

#Ecuacion de equilibrio en B
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [BK, BC])
print(f'{soluciones=}')

#bien, ahora actualizo las fuerzas en las barras
barras['BK'] = soluciones[BK]*-1
barras['BC'] = soluciones[BC]*-1

#AHora voy con el nodo K
KJ = symbols('KJ')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['K']
#Agrego las proyecciones de las barras
suma_V += KJ*proyeccion_V('K', 'J') + barras['BK']*proyeccion_V('K', 'B') + barras['LK']*proyeccion_V('K', 'L')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['K']
#Agrego las proyecciones de las barras
suma_H += KJ*proyeccion_H('K', 'J') + barras['BK']*proyeccion_H('K', 'B') + barras['LK']*proyeccion_H('K', 'L')

#Ecuacion de equilibrio en K
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

print(ecuacion_H)
print(ecuacion_V)

soluciones = solve(ecuacion_H, KJ)
print(f'{soluciones=}')

#bien, ahora actualizo las fuerzas en las barras
barras['KJ'] = soluciones[0]*-1


#Ahora voy con el nodo J
JI, JC = symbols('JI JC')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['J']
#Agrego las proyecciones de las barras
suma_V += -JI*proyeccion_V('J', 'I') - JC*proyeccion_V('J', 'C') + barras['KJ']*proyeccion_V('J', 'K')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['J']
#Agrego las proyecciones de las barras
suma_H += JI*proyeccion_H('J', 'I') + JC*proyeccion_H('J', 'C') + barras['KJ']*proyeccion_H('J', 'K')

#Ecuacion de equilibrio en J
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [JI, JC])
print(f'{soluciones=}')

#Ahora guardo las soluciones
barras['JI'] = soluciones[JI]*-1
barras['JC'] = soluciones[JC]*-1

#voy con el nodo F
GF, EF = symbols('GF EF')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['F']
#Agrego las proyecciones de las barras
suma_V += +GF*proyeccion_V('F', 'G') + EF*proyeccion_V('F', 'E')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['F']
#Agrego las proyecciones de las barras
suma_H += -GF*proyeccion_H('F', 'G') - EF*proyeccion_H('F', 'E')

#Ecuacion de equilibrio en F
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [GF, EF])
print(f'{soluciones=}')

#Guardo las soluciones
barras['GF'] = soluciones[GF]*-1
barras['EF'] = soluciones[EF]*-1

#Ahora voy con el nodo G
GE, HG = symbols('GE HG')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['G']
#Agrego las proyecciones de las barras
suma_V += -GE*proyeccion_V('G', 'E') + HG*proyeccion_V('G', 'H') + barras['GF']*proyeccion_V('G', 'F')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['G']
#Agrego las proyecciones de las barras
suma_H += -GE*proyeccion_H('G', 'E') + HG*proyeccion_H('G', 'H') + barras['GF']*proyeccion_H('G', 'F')

#Ecuacion de equilibrio en G
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [GE, HG])
print(f'{soluciones=}')

#Guardo las soluciones
barras['GE'] = soluciones[GE]*-1
barras['HG'] = soluciones[HG]*-1

#Ahora voy con el nodo H
HE, IH = symbols('HE IH')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['H']
#Agrego las proyecciones de las barras
suma_V += -HE*proyeccion_V('H', 'E') - IH*proyeccion_V('H', 'I') - barras['HG']*proyeccion_V('H', 'G')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['H']
#Agrego las proyecciones de las barras
suma_H += -HE*proyeccion_H('H', 'E') - IH*proyeccion_H('H', 'I') - barras['HG']*proyeccion_H('H', 'G')

#Ecuacion de equilibrio en H
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], [HE, IH])
print(f'{soluciones=}')

#Guardo las soluciones
barras['HE'] = soluciones[HE]*-1
barras['IH'] = soluciones[IH]*-1

#Ahora voy con el nodo E

IE = symbols('IE')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['E']
#Agrego las proyecciones de las barras
suma_V += -IE*proyeccion_V('E', 'I') + barras['HE']*proyeccion_V('E', 'H') - barras['EF']*proyeccion_V('E', 'F')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['E']
#Agrego las proyecciones de las barras
suma_H += IE*proyeccion_H('E', 'I') + barras['HE']*proyeccion_H('E', 'H') - barras['EF']*proyeccion_H('E', 'F')

#Ecuacion de equilibrio en E
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve(ecuacion_V, IE)
print(f'IE = {soluciones[0]}')

#Guardo las soluciones
barras['IE'] = soluciones[0]*-1



#Ahora voy con el nodo I
CI = symbols('CI')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_V['I']
#Agrego las proyecciones de las barras
suma_V += -CI*proyeccion_V('I', 'C') + barras['IE']*proyeccion_V('I', 'E') 

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_V['I']
#Agrego las proyecciones de las barras
suma_H += -CI*proyeccion_H('I', 'C') - barras['IE']*proyeccion_H('I', 'E') + barras['IH']*proyeccion_H('I', 'H') + barras['JI']*proyeccion_H('I', 'J')

#Ecuacion de equilibrio en I
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

print(ecuacion_H)
print(ecuacion_V)

soluciones = solve(ecuacion_H, CI)
print(f'CI = {soluciones[0]}')

#Guardo las soluciones
barras['CI'] = soluciones[0]*-1

print('')





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