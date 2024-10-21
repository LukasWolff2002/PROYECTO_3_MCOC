import numpy as np
import math
import matplotlib.pyplot as plt
import openseespy.opensees as ops
import pyvista as pv

#arch -x86_64 python3 /Users/lukaswolff/Desktop/24_20/METODOS_COMPUTACIONALES/PROYECTO_3_MCOC/CODIGO/OPENSEES/E0_Wolff.py

# Parámetros del material y área
E = 210e9  # Módulo de elasticidad en Pa
D1 = 0.1355 # Diámetro en m
esp = 0.009  # Espesor en m
A1 = math.pi * ((D1 / 2) ** 2 - ((D1 - 2 * esp) / 2) ** 2)  # Área de la sección transversal

print(A1)

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# Definir el material uniaxial elástico
matTag = 1  # Material tag
ops.uniaxialMaterial('Elastic', 1, E)

# Definir nodos y miembros
nodes = {
    1: (0, 0),
    2: (0, 12),
    3: (8, 7.73),
    4: (8, 12),
    5: (16, 11.73),
    6: (16, 12),
    7: (24, 12),
    8: (30, 9.4),
    9: (30, 12),
    10: (36, 12),
    11: (36, 4)
}

for node_id, coords in nodes.items():
    ops.node(node_id, *coords)

# Definir los elementos truss
elements = [
    (1, 2), #1
    (1, 3), #2BC
    (2, 3), #3
    (2, 4), #4
    (3, 4), #5
    (3, 5), #6
    (4, 6), #7
    (4, 5), #8
    (5, 6), #9
    (5, 7), #10
    (6, 7), #11
    (7, 9), #12
    (7, 8), #13
    (8, 9), #14
    (8, 10), #15
    (9, 10), #16
    (8, 11), #17
    (10, 11) #18
]

for i, (ni, nj) in enumerate(elements, start=1):
    ops.element('Truss', i, ni, nj, A1, matTag)

# Definir condiciones de frontera
ops.fix(1, 1, 1)  # Nodo 1 empotrado
ops.fix(11, 1, 1)  # Nodo 11 empotrado

# Definir cargas en los nodos
ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)
ops.load(2, 0.0, -15000.0)
ops.load(4, 0.0, -30000.0)
ops.load(6, 0.0, -30000.0)
ops.load(7, 0.0, -30000.0)
ops.load(9, 0.0, -30000.0)
ops.load(10, 0.0, -15000.0)

# Configuración del análisis estático
ops.system('BandSPD')
ops.numberer('RCM')
ops.constraints('Plain')
ops.integrator('LoadControl', 1.0)
ops.algorithm('Linear')
ops.analysis('Static')

# Ejecutar análisis
if ops.analyze(1) != 0:
    print("Error en el análisis estático")
else:
    print("Análisis estático exitoso")

#Obtenemos los desplazamientos
displacements = {node: ops.nodeDisp(node) for node in nodes.keys()}

# Obtener los esfuerzos internos (fuerza axial) de cada barra
print("\nEsfuerzos internos en las barras (fuerzas axiales):")
for ele in range(1, len(elements) + 1):  # Recorre todos los elementos
    axial_force = ops.eleResponse(ele, 'axialForce')  # Obtener la fuerza axial
    
    # Verificar si el valor devuelto es una lista u otro tipo de contenedor
    if isinstance(axial_force, (list, tuple)):
        axial_force = (axial_force[0])/1000  # Extraer el primer valor si es una lista
    
    print(f"Barra {ele}: Fuerza axial = {axial_force:.2f} KN")

#Obtengo el desplazamiento del nodo D
nodeTag = 7  # Identificador del nodo
ux = ops.nodeDisp(nodeTag, 1)  # Desplazamiento en la dirección X
uy = ops.nodeDisp(nodeTag, 2)  # Desplazamiento en la dirección Y

print(f"Desplazamientos del nodo {nodeTag}: ux = {ux}, uy = {uy}")



# Factor de escala para los desplazamientos
xfact = 100  # Ajusta este valor según sea necesario

# Crear la figura para el gráfico
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect('equal', adjustable='box')

# Dibujar la estructura original (sin deformación)
for ele in elements:
    node_i, node_j = ele
    ix, iy = nodes[node_i]
    jx, jy = nodes[node_j]
    
    # Estructura sin deformación
    ax.plot([ix, jx], [iy, jy], 'grey', lw=0.75, label='Original')

# Dibujar la estructura deformada
for ele in elements:
    node_i, node_j = ele
    ix, iy = nodes[node_i]
    jx, jy = nodes[node_j]
    
    # Obtener desplazamientos nodales
    ux_i = ops.nodeDisp(node_i, 1) * xfact
    uy_i = ops.nodeDisp(node_i, 2) * xfact
    ux_j = ops.nodeDisp(node_j, 1) * xfact
    uy_j = ops.nodeDisp(node_j, 2) * xfact

    # Estructura deformada
    ax.plot([ix + ux_i, jx + ux_j], [iy + uy_i, jy + uy_j], 'red', lw=1.5, label='Deformed')

from matplotlib.lines import Line2D

# Crear manejadores personalizados
custom_lines = [
    Line2D([0], [0], color='grey', lw=2, label='Original'),
    Line2D([0], [0], color='red', lw=2, label='Deformed')
]

# Agregar la leyenda usando los manejadores personalizados
plt.legend(handles=custom_lines, loc='lower right', fontsize=12)

# Configurar etiquetas y el gráfico
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Distance (m)')
ax.grid(True)

plt.tight_layout()

# Guardar y mostrar el gráfico
plt.savefig('deformed_truss.png')

# Definir las coordenadas deformadas
deformed_nodes = {node: np.array(coords) + xfact * np.array(displacements[node]) for node, coords in nodes.items()}

# Añadir coordenada z (0) para todas las coordenadas 2D
def add_z_coord(points_2d):
    return np.hstack([points_2d, np.zeros((points_2d.shape[0], 1))])

# Crear la visualización tridimensional con PyVista
plotter = pv.Plotter()

# Coordenadas originales (no deformadas) con z=0
points_undeformed = np.array(list(nodes.values()))
points_undeformed = add_z_coord(points_undeformed)  # Convertir a 3D

# Coordenadas deformadas con z=0
points_deformed = np.array(list(deformed_nodes.values()))
points_deformed = add_z_coord(points_deformed)  # Convertir a 3D

# Definir las líneas (elementos)
lines = np.array([[2, e[0] - 1, e[1] - 1] for e in elements])

# Añadir la estructura no deformada
truss_undeformed = pv.PolyData(points_undeformed)
truss_undeformed.lines = lines
plotter.add_mesh(truss_undeformed, color='blue', line_width=2, label="Undeformed")

# Añadir la estructura deformada
truss_deformed = pv.PolyData(points_deformed)
truss_deformed.lines = lines
plotter.add_mesh(truss_deformed, color='red', line_width=2, label="Deformed")

# Añadir la leyenda y mostrar el gráfico
plotter.add_legend()
plotter.show()


