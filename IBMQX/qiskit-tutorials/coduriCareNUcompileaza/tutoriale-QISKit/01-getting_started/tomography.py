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

# importing the QISKit
import qiskit
from qiskit import QuantumCircuit, QuantumProgram

# import tomography libary
import qiskit.tools.qcvv.tomography as tomo

# useful additional packages 
from qiskit.tools.visualization import plot_state
from qiskit.tools.qi.qi import *

Q_program = QuantumProgram()

# Creating registers
qr = Q_program.create_quantum_register("qr", 2)
cr = Q_program.create_classical_register("cr", 2)

# hadamard on qubit-1 only
had = Q_program.create_circuit("had", [qr], [cr])
had.h(qr[1])

# CNOT gate with qubit 1 control, qubit 0 target (target for ibmqx4)
cnot = Q_program.create_circuit("cnot", [qr], [cr])
cnot.cx(qr[1], qr[0])

U_had = np.array([[1,1],[1,-1]])/np.sqrt(2)
# compute Choi-matrix from unitary
had_choi = outer(vectorize(U_had))
plot_state(had_choi)




# process tomography set for a quantum operation on qubit 1
had_tomo_set =  tomo.process_tomography_set([1])

# Generate process tomography preparation and measurement circuits
had_tomo_circuits = tomo.create_tomography_circuits(Q_program, 'had', qr, cr, had_tomo_set)
print('Tomography circuit labels for "had" circuit:')
for label in had_tomo_circuits:
    print(label)


backend = 'local_qasm_simulator'
shots = 4096
had_tomo_results = Q_program.execute(had_tomo_circuits, shots=shots, backend=backend)

had_process_data = tomo.tomography_data(had_tomo_results, 'had', had_tomo_set)
had_choi_fit = tomo.fit_tomography_data(had_process_data, options={'trace':2})
print('Process Fidelity = ', state_fidelity(vectorize(U_had)/2, had_choi_fit))
plot_state(had_choi_fit)

