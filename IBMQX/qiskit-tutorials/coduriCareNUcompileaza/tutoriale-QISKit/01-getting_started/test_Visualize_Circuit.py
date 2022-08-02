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

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, execute, register, get_backend

# Build your Circuit

# Create a Quantum Register called "q" with 3 qubits
qr = QuantumRegister(3)

# Create a Classical Register called "c" with 3 bits
cr = ClassicalRegister(3)

# Create a Quantum Circuit called involving "qr" and "cr"
circuit = QuantumCircuit(qr, cr)

# Not gate on qubit 0
circuit.x(qr[0])

# Not gate on qubit 1
circuit.x(qr[1])

# Barrier to seperator the input from the circuit
circuit.barrier(qr[0])
circuit.barrier(qr[1])
circuit.barrier(qr[2])

# Toffoli gate from qubit 0,1 to qubit 2
circuit.ccx(qr[0], qr[1], qr[2])

# CNOT (Controlled-NOT) gate from qubit 0 to qubit 1
circuit.cx(qr[0], qr[1])

# measure gate from qr to cr
circuit.measure(qr, cr)

# QASM from a program

QASM_source = circuit.qasm()

print(QASM_source)

# Visualize Circuit

from qiskit.tools.visualization import circuit_drawer
circuit_drawer(circuit)

# Execute
backend = 'local_qasm_simulator'

# Create a Quantum Program for execution 
job = execute(circuit, backend)

job.status
result = job.result()

result.get_counts(circuit)

