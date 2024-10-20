from sympy import symbols, Eq, solve
print('')
# Definir las fuerzas, coordenadas y reacciones simbólicas
Fuerzas_V_ext = {'A': 0, 'B': 0, 'C': 0, 'E': 0, 'F': 0, 'L': -15, 'K': -30, 'J': -30, 'I': -30, 'H': -30, 'G': -15}  # En KN
Fuerzas_H_ext = {'A': 0, 'B': 0, 'C': 0, 'E': 0, 'F': 0, 'L': 0, 'K': 0, 'J': 0, 'I': 0, 'H': 0, 'G': 0}  # En KN

Coordenadas_H = {'A': 0, 'L': 0, 'B': 8, 'K': 8, 'C': 16, 'J': 16, 'I': 24, 'E': 30, 'H': 30, 'F': 36, 'G': 36}  # En m
Coordenadas_V = {'A': 0, 'L': 12, 'B': 0, 'K': 12, 'C': 0, 'J': 12, 'I': 12, 'E': 0, 'H': 12, 'F': 4, 'G': 12}  # En m

# Definir las incógnitas
Va, Vf, Ha, Hf = symbols('Va Vf Ha Hf')

# Diccionarios para reacciones
Reacciones_V = {'A': Va, 'F': Vf}
Reacciones_H = {'A': Ha, 'F': Hf}

# Ecuación de equilibrio de fuerzas verticales
R_V_total = sum(Fuerzas_V_ext.values())  # Sumar todas las fuerzas externas verticales

# Calcular el momento en torno a A (M_A)
M_A = 0
# Agregar los momentos generados por las fuerzas verticales externas
for i in Fuerzas_V_ext.keys():
    M_A -= Fuerzas_V_ext[i] * Coordenadas_H[i]  # Momento de las fuerzas en torno a A

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
    M_I -= Fuerzas_V_ext[nodo] * (Coordenadas_H[nodo]-Coordenadas_H['I'])

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

#Bien, implemento las reacciones en los nodos
Fuerzas_V_ext['A'] = Va
Fuerzas_V_ext['F'] = Vf
Fuerzas_H_ext['A'] = Ha
Fuerzas_H_ext['F'] = Hf

print('')
#Ahora debo calcular las alturas

# Definir las incógnitas
Hb, Hc, He = symbols('Hb Hc He')

#Se que el momento en E tiene que ser 0
M_E = 0

#Nodos actuantes 
Nodos_actuantes = ['G', 'F']

for nodo in Nodos_actuantes:
    M_E += Fuerzas_V_ext[nodo] * (Coordenadas_H[nodo]-Coordenadas_H['E'])

#demas actua la reaccion horizontal en F
M_E -= Fuerzas_H_ext['F'] * (Coordenadas_V['F']-He)

#Ecuacion de momento en torno a E
ecuacion_momento_E = Eq(M_E, 0)
print(f'{ecuacion_momento_E=}')
soluciones = solve(ecuacion_momento_E, He)
He = soluciones[0]
print(f'{He=}')
Coordenadas_V['E'] = He

#Ahora, calculo el momento en torno a B
M_B = 0
#Los nodos actuantes son 
Nodos_actuantes = ['A', 'L']

for nodo in Nodos_actuantes:
    M_B -= Fuerzas_V_ext[nodo] * (Coordenadas_H['B'])


#Además actua la reacción horizontal en A
M_B += Fuerzas_H_ext['A'] * (Hb)

#Ecuacion de momento en torno a B
ecuacion_momento_B = Eq(M_B, 0)
print(f'{ecuacion_momento_B=}')
soluciones = solve(ecuacion_momento_B, Hb)
Hb = soluciones[0]
print(f'{Hb=}')
Coordenadas_V['B'] = Hb


#Finalmente lo hago para C
M_C = 0
#Los nodos actuantes son
Nodos_actuantes = ['A', 'L', 'K']
for nodo in Nodos_actuantes:
    
    M_C -= Fuerzas_V_ext[nodo] * (Coordenadas_H['C']-Coordenadas_H[nodo])

#ctua la reacción horizontal en A
M_C += Fuerzas_H_ext['A'] * (Hc)

#Ecuacion de momento en torno a C
ecuacion_momento_C = Eq(M_C, 0)
print(f'{ecuacion_momento_C=}')
soluciones = solve(ecuacion_momento_C, Hc)
Hc = soluciones[0]
print(f'{Hc=}')
Coordenadas_V['C'] = Hc

print('')
#Ahora calculo las reaccione sen cada barra

from math import cos, sin

barras = {'AB': 0, 'AL': 0, 'LK': 0, 'LB': 0, 'BC': 0, 'BK': 0, 'KJ': 0, 'JC': 0, 'JI': 0, 'CI': 0, 'IH': 0, 'IE': 0, 'HE': 0, 'HG': 0, 'GE': 0, 'GF': 0, 'EF': 0}  # En m

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
suma_V = Fuerzas_V_ext['A']
#Agrego las proyecciones de las barras
suma_V += AB*proyeccion_V('A', 'B') + AL*proyeccion_V('A', 'L')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['A']
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
suma_V = Fuerzas_V_ext['L']
#Agrego las proyecciones de las barras
suma_V += LB*proyeccion_V('L', 'B') + LK*proyeccion_V('L', 'K') + barras['AL']*proyeccion_V('L', 'A')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['L']
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
suma_V = Fuerzas_V_ext['B']
#Agrego las proyecciones de las barras
suma_V += BK*proyeccion_V('B', 'K') + BC*proyeccion_V('B', 'C') + barras['LB']*proyeccion_V('B', 'L') + barras['AB']*proyeccion_V('B', 'A')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['B']
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
suma_V = Fuerzas_V_ext['K']
#Agrego las proyecciones de las barras
suma_V += KJ*proyeccion_V('K', 'J') + barras['BK']*proyeccion_V('K', 'B') + barras['LK']*proyeccion_V('K', 'L')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['K']
#Agrego las proyecciones de las barras
suma_H += KJ*proyeccion_H('K', 'J') + barras['BK']*proyeccion_H('K', 'B') + barras['LK']*proyeccion_H('K', 'L')

#Ecuacion de equilibrio en K
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve([ecuacion_V, ecuacion_H], KJ)
print(f'{soluciones=}')

#bien, ahora actualizo las fuerzas en las barras
barras['KJ'] = soluciones[KJ]*-1


#Ahora voy con el nodo J
JI, JC = symbols('JI JC')

#Suma vertical de fuerzas
suma_V = Fuerzas_V_ext['J']
#Agrego las proyecciones de las barras
suma_V += -JI*proyeccion_V('J', 'I') - JC*proyeccion_V('J', 'C') + barras['KJ']*proyeccion_V('J', 'K')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['J']
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
suma_V = Fuerzas_V_ext['F']
#Agrego las proyecciones de las barras
suma_V += +GF*proyeccion_V('F', 'G') + EF*proyeccion_V('F', 'E')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['F']
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
suma_V = Fuerzas_V_ext['G']
#Agrego las proyecciones de las barras
suma_V += -GE*proyeccion_V('G', 'E') + HG*proyeccion_V('G', 'H') + barras['GF']*proyeccion_V('G', 'F')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['G']
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
suma_V = Fuerzas_V_ext['H']
#Agrego las proyecciones de las barras
suma_V += -HE*proyeccion_V('H', 'E') - IH*proyeccion_V('H', 'I') - barras['HG']*proyeccion_V('H', 'G')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['H']
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
suma_V = Fuerzas_V_ext['E']
#Agrego las proyecciones de las barras
suma_V += -IE*proyeccion_V('E', 'I') + barras['HE']*proyeccion_V('E', 'H') - barras['EF']*proyeccion_V('E', 'F')

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['E']
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
suma_V = Fuerzas_V_ext['I']
#Agrego las proyecciones de las barras
suma_V += -CI*proyeccion_V('I', 'C') + barras['IE']*proyeccion_V('I', 'E') 

#Suma horizontal de fuerzas
suma_H = Fuerzas_H_ext['I']
#Agrego las proyecciones de las barras
suma_H += CI*proyeccion_H('I', 'C') - barras['IE']*proyeccion_H('I', 'E')

#Ecuacion de equilibrio en I
ecuacion_V = Eq(suma_V, 0)
ecuacion_H = Eq(suma_H, 0)

soluciones = solve(ecuacion_V, CI)
print(f'CI = {soluciones[0]}')

#Guardo las soluciones
barras['CI'] = soluciones[0]*-1

print('')

print(Coordenadas_H)
print(Coordenadas_V)



