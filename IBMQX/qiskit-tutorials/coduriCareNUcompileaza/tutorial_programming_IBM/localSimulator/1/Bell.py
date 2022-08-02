import sys
import os
# Checking the version of PYTHO; we only support > 3.5
if sys.version_info < (3,5):
    raise Exception('Please use Python version 3.5 or greater.')

# import qiskit from qiskit-sdk-py folder 
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..', 'qiskit-sdk-py'))
from qiskit import QuantumProgram

# creating QuantumProgram object
qp = QuantumProgram()

# creating Quantum Register with 2 qubits
qr = qp.create_quantum_register('qr', 2)
# creating Classical Register with 2 bits
cr = qp.create_classical_register('cr', 2)
# creating Quantum Circuit
qc = qp.create_circuit('Bell', [qr], [cr])

# defining Quantum Gates
qc.h(qr[0])
qc.cx(qr[0], qr[1])

# measurements 
qc.measure(qr[0], cr[0])
qc.measure(qr[1], cr[1])

# results
result = qp.execute('Bell')
print(result.get_counts('Bell'))