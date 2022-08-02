# quantum_phase_bloch.py
import sys
import os
import time

# import qiskit from qiskit-sdk-py folder
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'qiskit-sdk-py'))
    import Qconfig
    qx_config = {
        "APItoken": Qconfig.APItoken,
        "url": Qconfig.config['url']}
except:
    qx_config = {
        "APItoken":"da2a4002660558a35103a600bcbda7fe438cea629a6be98969ea5e367c091b6815e624bd86b6207121bd97fef79c22033318a4402eeafcbd04b021fd80f5a195",
        "url":"https://quantumexperience.ng.bluemix.net/api"
    }

import numpy as np 
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute
from qiskit.tools.visualization import plot_bloch_vector

# Define the Classical and Quantum Registers
c = ClassicalRegister(1)
q = QuantumRegister(1)

# Build the circuits
pre = QuantumCircuit(q, c)
pre.h(q)
pre.barrier()

meas_x = QuantumCircuit(q, c)
meas_x.barrier()
meas_x.h(q)
meas_x.measure(q, c)

meas_y = QuantumCircuit(q, c)
meas_y.barrier()
meas_y.s(q).inverse()
meas_y.h(q)
meas_y.measure(q, c)

meas_z = QuantumCircuit(q, c)
meas_z.barrier()
meas_z.measure(q, c)

bloch_vector = ['x', 'y', 'z']
exp_vector = range(0, 21)
circuits = []
for exp_index in exp_vector:
    middle = QuantumCircuit(q, c)
    phase = 2*np.pi*exp_index/(len(exp_vector)-1)
    middle.u1(phase, q)
    circuits.append(pre + middle + meas_x)
    circuits.append(pre + middle + meas_y)
    circuits.append(pre + middle + meas_z)

# Execute teh circuit
job = execute(circuits, backend = 'local_qasm_simulator', shots=4096)
result = job.result()

# Plot the result
for exp_index in exp_vector:
    bloch = [0, 0, 0]
    for bloch_index in range(len(bloch_vector)):
        data = result.get_counts(circuits[3*exp_index+bloch_index])
        try:
            p0 = data['0']/4096.0
        except KeyError:
            p0 = 0
        try:
            p1 = data['1']/4096.0
        except KeyError:
            p1 = 0
        bloch[bloch_index] = p0 - p1
    plot_bloch_vector(bloch)