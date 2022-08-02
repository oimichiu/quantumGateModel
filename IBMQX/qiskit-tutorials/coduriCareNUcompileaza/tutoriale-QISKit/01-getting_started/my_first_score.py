# my_first_scire.py
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

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute

# Define the Quantum and Classical Registers
q = QuantumRegister(2)
c = ClassicalRegister(2)

# Build the circuit
my_first_score = QuantumCircuit(q, c)

# Build the operations
# Pauli operations
my_first_score.x(q[0])
my_first_score.y(q[1])
my_first_score.z(q[0])
my_first_score.barrier(q)

# Clifford operations
my_first_score.h(q)
my_first_score.s(q[0])
my_first_score.s(q[1]).inverse()
my_first_score.cx(q[0], q[1])
my_first_score.barrier(q)

# non-Clifford operations
my_first_score.t(q[0])
my_first_score.t(q[1]).inverse()
my_first_score.barrier(q)

# measurement operations
my_first_score.measure(q, c)

# Execute the circuite 
job = execute(my_first_score, backend = 'local_qasm_simulator', shots=4096)
result = job.result()

# Print the result
print(result.get_counts(my_first_score))