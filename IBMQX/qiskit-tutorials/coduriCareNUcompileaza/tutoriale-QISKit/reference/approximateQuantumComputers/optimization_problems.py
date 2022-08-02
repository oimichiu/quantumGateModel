# Optimization Problem
import sys
import os

# useful additional packages
import matplotlib.pyplot as plt 
import matplotlib.axes as axes 
import numpy as np 
from scipy import linalg as la 
from itertools import permutations
from functools import partial
import networkx as nx 

################# import Qconfig and set APIToken and API url and  prepare backends ############

try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'qiskit-sdk-py'))
    import Qconfig
    qx_config = {
        "APItoken": Qconfig.APItoken,
        "url": Qconfig.config['url']}
except Exception as e:
    print(e)
    qx_config = {
        "APItoken":"da2a4002660558a35103a600bcbda7fe438cea629a6be98969ea5e367c091b6815e624bd86b6207121bd97fef79c22033318a4402eeafcbd04b021fd80f5a195",
        "url":"https://quantumexperience.ng.bluemix.net/api"
    }

# importing the QISKit
from qiskit import QuantumCircuit, QuantumProgram
from qiskit import register, available_backends, get_backend

# set api
register(qx_config['APItoken'], qx_config['url'])
backends = available_backends()

print("Backends: ", backends)
################### end of preparing backends ########################

# import basic plot tools
from qiskit.tools.visualization import plot_histogram

# import optimization tools
from qiskit.tools.apps.optimization import trial_circuit_ry, SPSA_optimization, SPSA_calibration
from qiskit.tools.apps.optimization import Energy_Estimate, make_Hamiltonian, eval_hamiltonian, group_paulis
from qiskit.tools.qi.pauli import Pauli 

def obj_funct(Q_program, pauli_list, entagler_map, coupling_map, initial_layout, n, m, backend, shots, theta):
    
    """ Evaluate the objective function for a classical optimization problem.

    Q_program is an instance object of the class quantum program
    pauli_list defines the cost function as list of ising terms with weights
    theta are the control parameters 
    n is the number of qubits
    m is the depth of the trial function 
    backend is the type of backend to run it on
    shots is the number of shots to run. Taking shots = 1 only works in simulation
    and computes an exact average of the cost function on the quantum state
    """

    std_cost=0 # to add later
    circuits = ['trial_circuit']

    if shots==1:
        Q_program.add_circuit('trial_circuit', trial_circuit_ry(n, m, theta, entagler_map, None, False))
        result = Q_program.execute(circuits, backend=backend, coupling_map=coupling_map, initial_layout=initial_layout, shots=shots)
        state = result.get_data('trial_circuit')['quantum_state']
        cost=Energy_Estimate_Exact(state, pauli_list, True)
    else:
        Q_program.add_circuit('trial_circuit', trial_circuit_ry(n, m, theta, entagler_map, None, True))
        result = Q_program.execute(circuits, backend=backend, coupling_map=coupling_map, initial_layout=initial_layout, shots=shots)
        data = result.get_counts('trial_circuit')
        cost = Energy_Estimate(data, pauli_list)

    return cost, std_cost

# Generating a graph of 4 nodes
n = 4 # Number of nodes in graph

G = nx.Graph()
G.add_nodes_from(np.arange(0,n,1))
elist=[(0,1,1.0),(0,2,1.0),(0,3,1.0),(1,2,1.0),(2,3,1.0)]
# tuple is (i, j , weight) where (i,j) is the edge
G.add_weighted_edges_from(elist)

colors = ['r' for node in G.nodes()]
default_axes = plt.axes(frameon=True)
pos=nx.spring_layout(G)
nx.draw_networkx(G, node_color=colors, node_size= 600, alpha=.8, ax=default_axes, pos=pos)
#plt.draw()
#plt.show()

# Computing the weight matrix from the random graph
    
w = np.zeros([n,n])
for i in range(n):
    for j in range(n):
        temp = G.get_edge_data(i,j,default=0)
        if temp !=0:
            w[i,j] = temp['weight']
print(w)

# Brute Force approach
best_cost_brute = 0
for b in range(2**n):
    x = [int(t) for t in reversed(list(bin(b)[2:].zfill(n)))]
    cost = 0
    for i in range(n):
        for j in range(n):
            cost = cost + w[i,j]*x[i]*(1-x[j])
    if best_cost_brute < cost:
        best_cost_brute = cost
        xbest_brute = x

    print('case = ' + str(x)+ ' cost = ' + str(cost))
colors = []
for i in range(n):
    if xbest_brute[i] == 0:
        colors.append('r')
    else:
        colors.append('b')
nx.draw_networkx(G, node_color=colors, node_size=600, alpha=.8, pos=pos)
plt.show()
print('\nBest solution = ' + str(xbest_brute) + ' cost = ' + str(best_cost_brute))

# Mapping to the Ising problem
# Determining the constant shift and initialize a pauli_list that contains the ZZ Ising terms

pauli_list = []
cost_shift = 0
for i in range(n):
    for j in range(i):
        if w[i,j] !=0:
            cost_shift = cost_shift + w[i,j]
            wp = np.zeros(n)
            vp = np.zeros(n)
            vp[n-i-1] = 1
            vp[n-j-1] = 1
            pauli_list.append((w[i,j], Pauli(vp,wp)))
cost_shift
print(cost_shift)

# Making the Hamiltonian in its full form and getting the lowest eigenvalue and eigenvector

H = make_Hamiltonian(pauli_list)
we, ve = la.eigh(H, eigvals=(0,1))
exact = we[0]
exact_maxcut = -we[0]/2 + cost_shift/2
print(exact_maxcut)
print(exact)
H = np.diag(H) 