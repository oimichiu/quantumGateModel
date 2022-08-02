# t1.py
import sys
import os

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
import matplotlib.pyplot as plt 

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, register

import Qconfig
register(Qconfig.APItoken, Qconfig.config['url'])

# Define the Classical and Quantum Register
c = ClassicalRegister(1)
q = QuantumRegister(1)

# Build the circuits
pre = QuantumCircuit(q, c)
pre.x(q)
pre.barrier()
meas = QuantumCircuit(q, c)
meas.measure(q, c)
circuits = []
exp_vector = range(1,51)
for exp_index in exp_vector:
    middle = QuantumCircuit(q, c)
    for i in range(45*exp_index):
        middle.iden(q)
    circuits.append(pre + middle + meas)

# Execute the circuits
shots = 1024
job = execute(circuits, 'ibmqx4', shots=shots, max_credits=10)
result = job.result()

# Plot the result
exp_data = []
exp_error = []
for exp_index in exp_vector:
    data = result.get_counts(circuits[exp_index-1])
    try:
        p0 = data['0']/shots
    except KeyError:
        p0 = 0
    exp_data.append(p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [45*gate time]')
plt.ylabel('Pr(0)')
plt.grid(True)
plt.show()