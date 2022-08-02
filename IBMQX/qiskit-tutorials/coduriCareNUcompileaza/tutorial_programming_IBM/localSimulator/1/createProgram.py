import sys
import os
# Checking the version of PYTHO; we only support > 3.5
if sys.version_info < (3,5):
    raise Exception('Please use Python version 3.5 or greater.')

# import qiskit from qiskit-sdk-py folder 
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..', 'qiskit-sdk-py'))
from qiskit import QuantumProgram
import Qconfig

# Basic elements for the 1st program: QuantumProgram, Circuit, Quantum Register and Classical Register
# 

# Creating Programs

# Option no.1
# creating your first QuantumProgram object instance
qp = QuantumProgram()

# Creating Registers
# create your first Quantum Register called "qr" with 2 qubits
qr = qp.create_quantum_register('qr', 2)

# create your first Classical Register called "qc" with 2 bits
cr = qp.create_classical_register('cr', 2)

# Creating Circuits
# create your 1st Quantum Circuit called "qc" involving your Quantum Register "qr" 
# and your Classical Register "cr"
qc = qp.create_circuit('Circuit', [qr], [cr])

# Option no.2 --> create a QuantumProgram instance is to define a dictionary
 
Q_SPECS = {
    'circuits':[{
        'name': 'Circuit1',
        'quantum_registers' : [{
            'name': 'qr1',
            'size': 4 # number of qubits
        }],
        'classical_registers': [{
            'name': 'cr1',
            'size': 4 # number of bits
        }]}],
}

# You can use this dictionary definitons as the specs of one QuantumProgram object to initialize it

qp1 = QuantumProgram(specs=Q_SPECS)

# Get the components or every component

# get the circuit by Name
circuit = qp1.get_circuit('Circuit1')

# get the Quantum Register by Name
quantum_r = qp1.get_quantum_register('qr1')

# get the Classical Register by Name
classical_r = qp1.get_classical_register('cr1')

## Add Gates to your Circuit

# Pauli X gate to qubit 1 in the Quantum Register "qr"
ciruit.x(quantum_r[1])

# Pauli Y gate to qubit 2 in the Quantum Register "qr"
circuit.y(quantum_r[2])

# Pauli Z gate to qubit 3 in the Quantum Register "qr"
circuit.z(quantum_r[3])

# CNOT (Controlled-NOT) gate from qubit 3 to qubit 2
circuit.cx(quantum_r[3], quantum_r[2])

# add a barrier to your circuit 
circuit.barrier()

# H (Hadamard) gate to qubit 0 in the Quantum Register "qr"
circuit.h(quantum_r[0])

# S Phase gate to qubit 0
circuit.s(quantum_r[0])

# T Phase gate to qubit 1
circuit.t(quantum_r[1])

# identity gate to qubit 1
circuit.iden(quantum_r[1])

# first physical gate: u1(lambda) to qubit 0
circuit.u1(0.3, quantum_r[0])

# second physical gate: u2(phi, lambda) to qubit 1
circuit.u2(0.3, 0.2, quantum_r[1])
