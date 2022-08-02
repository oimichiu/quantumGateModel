import sys, getpass, os
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'qiskit-sdk-py'))
    import Qconfig
    qx_config = {
        "APItoken": Qconfig.APItoken,
        "url": Qconfig.config['url']}
    print('Qconfig loaded from %s.' %Qconfig.__file__) 
except:
    APItoken = getpass.getpass('Please imput your token and hit enter: ', da2a4002660558a35103a600bcbda7fe438cea629a6be98969ea5e367c091b6815e624bd86b6207121bd97fef79c22033318a4402eeafcbd04b021fd80f5a195)
    qx_config = {
        "APItoken": APItoken,
        "url":"https://quantumexperience.ng.bluemix.net/api"}
    print('Qconfig.py not found in qiskit-tutorial directory; Qconfig loaded using user input.')

import qiskit as qk 
import numpy as np 
from scipy.optimize import curve_fit
from qiskit.tools.qcvv.fitters import exp_fit_fun, osc_fit_fun, plot_coherence

# function for padding with QId gates
def pad_QId(circuit, N, qr):
    # circuit to add to, N = number of QId gates to add, qr = qubit register
    for ii in range(N):
        circuit.barrier(qr)
        circuit.iden(qr)
    return circuit

qk.register(qx_config['APItoken'], qx_config['url'])

# backend and token settings
backend = qk.get_backend('ibmqx4') # the device to run on
shots = 1024 # number of shots in the experiment

# Select qubit on which to measure T2*
qubit = 1

# Create registers
qr = qk.QuantumRegister(5)
cr = qk.ClassicalRegister(5)

params = backend.parameters['qubits'][qubit]
pulse_length=params['gateTime']['value'] # single-qubit gate time
buffer_length=params['buffer']['value'] # spacing between pulses
unit = params['gateTime']['unit']

steps = 35
gates_per_step = 20
max_gates=(steps-1)*gates_per_step+2

num_osc = 5
tot_length=buffer_length+pulse_length
time_per_step=gates_per_step*tot_length
qc_dict={}
for ii in range(steps):
    step_num='step_%s'%(str(ii))
    qc_dict.update({step_num:qk.QuantumCircuit(qr,cr)})
    qc_dict[step_num].h(qr[qubit])
    qc_dict[step_num]=pad_QId(qc_dict[step_num],gates_per_step*ii,qr[qubit])
    qc_dict[step_num].u1(2*np.pi*num_osc*ii/(steps-1),qr[qubit])
    qc_dict[step_num].h(qr[qubit])
    qc_dict[step_num].barrier(qr[qubit])
    qc_dict[step_num].measure(qr[qubit], cr[qubit])
circuits=list(qc_dict.values())

# run the program 
status = backend.status
if status['available'] == False or status['pending_jobs'] > 10:
    print('Warning: the selected backend appears to be busy or unavailable at present; consider choosing a different one if possible')
t2star_job=qk.execute(circuits, backend, shots=shots)

# arrange the data from the run

result_t2star = t2star_job.result()
keys_0_1=list(result_t2star.get_counts(qc_dict['step_0']).keys()) # get the key of the excited state '00001'

# change unit from ns to microseconds
plot_factor = 1
if unit.find('ns')>-1:
    plot_factor=1000
    punit='$\mu$s'
xvals=time_per_step*np.linspace(0,len(qc_dict.keys()),len(qc_dict.keys()))/plot_factor # calculate the time steps

data = np.zeros(len(qc_dict.keys())) # numpy array for data
sigma_data = np.zeros(len(qc_dict.keys()))

for ii,key in enumerate(qc_dict.keys()):
    # get the data in terms of counts for the excited state normalized to the total number of counts
    data[ii]=float(result_t2star.get_counts(qc_dict[key])[keys_0_1[1]])/shots
    sigma_data[ii] = np.sqrt(data[ii]*(1-data[ii]))/np.sqrt(shots)

fitT2s, fcov = curve_fit(osc_fit_fun, xvals, data, p0=[0.5, 100, 1/10, np.pi, 0], bounds=([0.3,0,0,0,0], [0.5, 200, 1/2,2*np.pi,1]))
ferr = np.sqrt(np.diag(fcov))

plot_coherence(xvals, data, sigma_data, fitT2s, osc_fit_fun, punit, '$T_2^*$ ', qubit)

print("a: " + str(round(fitT2s[0],2)) + u" \u00B1 " + str(round(ferr[0],2)))
print("T2*: " + str(round(fitT2s[1],2))+ " µs"+u" \u00B1 " + str(round(ferr[1],2)) + ' µs')
print("f: " + str(round(10**3*fitT2s[2],3)) + 'kHz' + u" \u00B1 " + str(round(10**6*ferr[2],3)) + 'kHz')
print("phi: " + str(round(fitT2s[3],2)) + u" \u00B1 " + str(round(ferr[3],2)))
print("c: " + str(round(fitT2s[4],2)) + u" \u00B1 " +str(round(ferr[4],2)))