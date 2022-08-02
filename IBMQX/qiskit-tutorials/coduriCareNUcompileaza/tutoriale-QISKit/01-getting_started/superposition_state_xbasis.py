# superposition_state_xbasis.py
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

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute

# Define the Classical and Quantum Register
c = ClassicalRegister(1)
q = QuantumRegister(1)

# Build the circuit
superposition_state_xbasis = QuantumCircuit(q, c)
superposition_state_xbasis.h(q)
superposition_state_xbasis.barrier()
superposition_state_xbasis.h(q)
superposition_state_xbasis.measure(q, c)

# Execute the circuit
job = execute(superposition_state_xbasis, backend='local_qasm_simulator', shots=4096)
result = job.result()

# Print the result
print(result.get_counts(superposition_state_xbasis))