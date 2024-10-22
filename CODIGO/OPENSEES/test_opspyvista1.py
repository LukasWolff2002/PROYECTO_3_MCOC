# Importar librerías necesarias
import openseespy.opensees as ops
import numpy as np
import math
import pyvista as pv

# Inicializar OpenSees
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# Definir nodos como diccionario
nodes = {
    1: [0, 0],        # Nodo 1
    2: [0, 12],       # Nodo 2
    3: [8, 7.73332],  # Nodo 3
    4: [8, 12],       # Nodo 4
    5: [16, 11.7333], # Nodo 5
    6: [16, 12],      # Nodo 6
    7: [24, 12],      # Nodo 7
    8: [30, 9.4],     # Nodo 8
    9: [30, 12],      # Nodo 9
    10: [36, 12],     # Nodo 10
    11: [36, 4]       # Nodo 11
}

# Definir elementos como lista de tuplas
elements = [
    (1, 2),   # Elemento 1
    (1, 3),   # Elemento 2
    (2, 3),   # Elemento 3
    (2, 4),   # Elemento 4
    (3, 4),   # Elemento 5
    (3, 5),   # Elemento 6
    (4, 6),   # Elemento 7
    (4, 5),   # Elemento 8
    (5, 6),   # Elemento 9
    (5, 7),   # Elemento 10
    (6, 7),   # Elemento 11
    (7, 9),   # Elemento 12
    (7, 8),   # Elemento 13
    (8, 9),   # Elemento 14
    (8, 10),  # Elemento 15
    (9, 10),  # Elemento 16
    (8, 11),  # Elemento 17
    (10, 11)  # Elemento 18
]

# Definir los nodos en OpenSees
for node_id, coords in nodes.items():
    ops.node(node_id, *coords)

# Fijar los apoyos (nodos 1 y 11 están fijos en X y Y)
ops.fix(1, 1, 1)
ops.fix(11, 1, 1)

# Definir propiedades del material y secciones
E = 207e9  # Módulo de elasticidad en Pa

D1 = 0.1      # Diámetro para A1 en m
esp1 = 0.03    # Espesor para A1 en m

D2 = 0.15       # Diámetro para A2 en m
esp2 = 0.07    # Espesor para A2 en m

A1 = math.pi * ((D1 / 2)**2 - ((D1 - 2 * esp1) / 2)**2)  # Área A1
A2 = math.pi * ((D2 / 2)**2 - ((D2 - 2 * esp2) / 2)**2)  # Área A2

ops.uniaxialMaterial('Elastic', 1, E)

# Definir elementos y asignar áreas: solo elementos conectados a nodos 1 y 11 tienen A2
for elem_num, (iNode, jNode) in enumerate(elements, start=1):
    if iNode in [1, 11] or jNode in [1, 11]:
        # Elementos conectados a nodo 1 o 11 usan A2
        ops.element('Truss', elem_num, iNode, jNode, A2, 1)
    else:
        # Resto de elementos usan A1
        ops.element('Truss', elem_num, iNode, jNode, A1, 1)

# Aplicar cargas y establecer tiempo dinámico
ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)

# Cargas en los nodos
ops.load(2, 0.0, -15000.0)   # Nodo 2: 15 kN hacia abajo
ops.load(4, 0.0, -30000.0)   # Nodo 4: 30 kN hacia abajo
ops.load(6, 0.0, -30000.0)   # Nodo 6: 30 kN hacia abajo
ops.load(7, 0.0, -30000.0)   # Nodo 7: 30 kN hacia abajo
ops.load(9, 0.0, -30000.0)   # Nodo 9: 30 kN hacia abajo
ops.load(10, 0.0, -15000.0)  # Nodo 10: 15 kN hacia abajo

# Definir parámetros de análisis
ops.system('BandSPD')
ops.numberer('RCM')
ops.constraints('Plain')
ops.integrator('LoadControl', 1.0)
ops.algorithm('Linear')
ops.analysis('Static')

# Realizar el análisis
ops.analyze(1)

# Calcular y almacenar las fuerzas axiales en los elementos
print("Fuerzas en los elementos")
mbr_forces = np.array([])
for elem_num, (iNode, jNode) in enumerate(elements, start=1):
    axial_force = ops.basicForce(elem_num)[0]  # Fuerza axial en N
    mbr_forces = np.append(mbr_forces, axial_force)
    print(f"Elemento {elem_num}: Fuerza axial = {axial_force / 1000:.3f} kN")
print("--------------------\n")

# Imprimir desplazamientos en los nodos
print("Desplazamientos")
for node_id in nodes:
    ux = ops.nodeDisp(node_id, 1) * 1000  # Convertir a mm
    uy = ops.nodeDisp(node_id, 2) * 1000  # Convertir a mm
    print(f"Nodo {node_id}: ux = {ux:.3f} mm, uy = {uy:.3f} mm")

# Factor de escala para los desplazamientos
scale_factor = 200  # Ajusta este valor según sea necesario

# Obtener los desplazamientos nodales
nodes_items = sorted(nodes.items())  # Ordenar los nodos por ID
displacements = []
for node_id, coords in nodes_items:
    ux = ops.nodeDisp(node_id, 1)
    uy = ops.nodeDisp(node_id, 2)
    displacements.append([ux, uy])
displacements = np.array(displacements)

# Calcular las coordenadas deformadas
deformed_coords = np.array([
    np.array(coords) + scale_factor * displacements[i]
    for i, (node_id, coords) in enumerate(nodes_items)
])

# Visualizar las formas no deformada y deformada utilizando PyVista
plotter = pv.Plotter()

# Agregar la estructura no deformada
points_undeformed = np.array([
    [x, y, 0.0] for _, (x, y) in nodes_items
])

# Definir las líneas correctamente
lines = []
for e in elements:
    lines.extend([2, e[0] - 1, e[1] - 1])
lines = np.array(lines, dtype=np.int_)

# Crear el objeto PolyData para la estructura no deformada
truss_undeformed = pv.PolyData()
truss_undeformed.points = points_undeformed
truss_undeformed.lines = lines
truss_undeformed.verts = None  # Eliminar celdas de vértices

plotter.add_mesh(truss_undeformed, color='blue', line_width=2, label="No Deformada")

# Agregar la estructura deformada
points_deformed = np.array([
    [x, y, 0.0] for x, y in deformed_coords
])

truss_deformed = pv.PolyData()
truss_deformed.points = points_deformed
truss_deformed.lines = lines
truss_deformed.verts = None  # Eliminar celdas de vértices

# Verificar el número de celdas
print(f"Número de celdas en truss_deformed: {truss_deformed.n_cells}")

# Añadir las fuerzas axiales como campo escalar en los elementos
# Convertir fuerzas a magnitudes absolutas en kN
mbr_forces_abs = np.abs(mbr_forces) / 1000  # Convertir a kN

# Asignar las fuerzas a los elementos (celdas)
truss_deformed.cell_data["Fuerza Axial (kN)"] = mbr_forces_abs

# Añadir la malla con mapeo de color basado en las fuerzas axiales
plotter.add_mesh(truss_deformed, scalars="Fuerza Axial (kN)", cmap="jet", line_width=5, label="Deformada", show_edges=True)

# Agregar una barra de colores
plotter.add_scalar_bar(title="Fuerza Axial (kN)")

# Mostrar ejes y leyenda
plotter.show_axes()
plotter.add_legend()

# Mostrar la gráfica
plotter.show()