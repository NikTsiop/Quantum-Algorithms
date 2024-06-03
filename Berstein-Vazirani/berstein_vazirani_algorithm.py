import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit import Aer, transpile
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import plot_histogram
from qiskit_ibm_provider import IBMProvider
from qiskit import *

#Creates the oracle with the hidden number
def create_oracle(number):
    
    qubit_len = len(number)+1
    classical_reg = len(number)
    qubit_counter = qubit_len-2
    circuit = QuantumCircuit(qubit_len, classical_reg)
    
    for digit in number:
        if digit == '1':
            circuit.cx(qubit_counter, qubit_len-1)
        qubit_counter -= 1
        if qubit_counter > qubit_len:
            break

    return circuit

qubits_number = 5
classical_registers = qubits_number - 1
qc = QuantumCircuit(qubits_number, classical_registers)

provider = IBMProvider()
qcomp = provider.get_backend('ibm_osaka')

#number to find
oracle_number = "1011"

#Bernstein-Vazirani algorithm
qc.x(4)
qc.barrier()
qc.h(range(qubits_number))
qc.barrier()
qc = qc.compose(create_oracle(oracle_number))
qc.barrier()
qc.h(range(qubits_number))
qc.barrier()
qc.measure(range(qubits_number-1),range(qubits_number-1))
print(qc)

#Simulation
simulator = Aer.get_backend('aer_simulator')
qc = transpile(qc, simulator)

result = simulator.run(qc).result()
count = result.get_counts()
plot_histogram(count, title='Bernstein-Vazirani')

#Real Quantum Computer
job_bernstein_vazirani = execute(qc, backend=qcomp)
job_monitor(job_bernstein_vazirani)
result_qc = job_bernstein_vazirani.result()
counts = result_qc.get_counts()
plot_histogram(counts)

plt.show()