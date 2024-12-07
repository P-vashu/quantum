from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt

# Function to simulate quantum coin toss without Aer
def quantum_coin_toss():
    """
    Simulate a coin toss using quantum mechanics without using the Aer simulator.
    
    Returns:
        tuple: Result of the coin toss ('Heads' or 'Tails'), 
               dictionary of measurement probabilities {'0': probability, '1': probability}.
    """
    # Step 1: Create a quantum circuit with one qubit
    qc = QuantumCircuit(1)
    
    # Step 2: Apply the Hadamard gate to create superposition
    qc.h(0)
    
    # Step 3: Get the final statevector
    state = Statevector.from_instruction(qc)
    
    # Step 4: Visualize the quantum state before measurement (superposition)
    plot_state_city(state, title="Quantum State After Hadamard Gate")
    plt.show()
    
    # Step 5: Extract the probabilities of the states |0> and |1>
    probabilities = state.probabilities_dict()  # {'0': probability, '1': probability}
    
    # Step 6: Sample the result based on probabilities
    toss_result = np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
    
    # Step 7: Map the result to 'Heads' or 'Tails'
    if toss_result == '0':
        return 'Heads', probabilities
    else:
        return 'Tails', probabilities

# Main function
if __name__ == "__main__":
    print("=== Quantum Coin Toss ===\n")
    
    # Simulate the coin toss and get the result and probabilities
    result, probabilities = quantum_coin_toss()
    
    print(f"The coin landed on: {result}")
    
    # Visualize the probabilities of the outcomes
    plot_histogram(probabilities, title="Measurement Probabilities")
    plt.show()
