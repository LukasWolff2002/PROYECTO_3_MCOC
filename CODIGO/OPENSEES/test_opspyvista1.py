#En linux, con openseespy customizado:
import openseespy.opensees as ops

# En linux/windows con openseespy instalado desde pip
# import opensees.opensees as ops
import numpy as np
import pyvista as pv

#arch -x86_64 python3 /Users/lukaswolff/Desktop/24_20/METODOS_COMPUTACIONALES/PROYECTO_2/ENTREGA_0/CODIGO/OPENSEES/test_opspyvista1.py
#arch -x86_64 python3 /Users/lukaswolff/Desktop/24_20/METODOS_COMPUTACIONALES/PROYECTO_2/ENTREGA_0/CODIGO/OPENSEES/E0_Wolff.py
# Initialize OpenSees
ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 3)

# Define the geometry of the truss (nodes)
nodes = {
    1: [0, 0, 0],
    2: [1, 0, 0],
    3: [0, 1, 0],
    4: [1, 1, 0],
    5: [0.5, 0.5, 1]
}

for node, coords in nodes.items():
    ops.node(node, *coords)

# Fix supports (nodes 1, 2, 3, and 4 are fixed in all directions)
fixed_nodes = [1, 2, 3, 4]
for node in fixed_nodes:
    ops.fix(node, 1, 1, 1)

# Define material properties and sections
E = 200e9  # Young's modulus in Pa
A = 0.01   # Cross-sectional area in m^2

ops.uniaxialMaterial('Elastic', 1, E)

# Define elements (truss members)
elements = [
    [1, 5],  # Node 1 to Node 5
    [2, 5],  # Node 2 to Node 5
    [3, 5],  # Node 3 to Node 5
    [4, 5]   # Node 4 to Node 5
]

for i, (iNode, jNode) in enumerate(elements, start=1):
    ops.element('Truss', i, iNode, jNode, A, 1)

# Apply loads (apply a load in the Z direction at node 5)
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(5, 0, 0, -50000.0)  # 50 kN downwards force

# Define analysis parameters
ops.system('BandGeneral')
ops.numberer('Plain')
ops.constraints('Plain')
ops.integrator('LoadControl', 1.0)
ops.algorithm('Linear')
ops.analysis('Static')

# Perform the analysis
ops.analyze(1)

# Extract node displacements
displacements = np.array([[ops.nodeDisp(node, i) for i in range(1, 4)] for node in nodes])

print(f"{displacements=}")

# For visualization, let's scale the displacements for better visibility
scale_factor = 1e4
deformed_nodes = {node: np.array(coords) + scale_factor * displacements[i] for i, (node, coords) in enumerate(nodes.items())}

# Visualize the undeformed and deformed shapes using PyVista
# Create a PyVista plotter
plotter = pv.Plotter()

# Add undeformed truss structure
points_undeformed = np.array(list(nodes.values()))
lines = np.array([[2, e[0] - 1, e[1] - 1] for e in elements])

truss_undeformed = pv.PolyData(points_undeformed)
truss_undeformed.lines = lines
plotter.add_mesh(truss_undeformed, color='blue', line_width=2, label="Undeformed")

# Add deformed truss structure
points_deformed = np.array(list(deformed_nodes.values()))

truss_deformed = pv.PolyData(points_deformed)
truss_deformed.lines = lines
plotter.add_mesh(truss_deformed, color='red', line_width=2, label="Deformed")

# Add legend and show plot
plotter.add_legend()
plotter.show()
