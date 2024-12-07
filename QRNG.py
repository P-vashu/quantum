import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# Function to Generate Quantum Random Numbers
def generate_quantum_random_number(num_bits):
    """
    Generate a random number using quantum superposition and measurement probabilities.
    
    Args:
        num_bits (int): Number of random bits to generate.
    
    Returns:
        str: A binary string representing the random number.
    """
    # Step 1: Initialize quantum circuit with 'num_bits' qubits
    qc = QuantumCircuit(num_bits)
    
    # Step 2: Apply Hadamard gate to all qubits to create superposition
    for i in range(num_bits):
        qc.h(i)
    
    # Step 3: Get the final statevector
    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict()  # Extract probabilities for all outcomes
    
    # Step 4: Randomly sample an outcome based on the probabilities
    outcome = np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
    return outcome, qc

# Main Function
if __name__ == "__main__":
    print("=== Quantum Random Number Generator ===\n")
    
    # Number of random bits to generate
    num_bits = 8  # Adjust this for more or fewer bits
    
    # Generate quantum random number
    random_number, circuit = generate_quantum_random_number(num_bits)
    
    # Display the results
    print(f"Generated {num_bits}-bit Quantum Random Number: {random_number}")
    
    # Visualization
    print("\n--- Quantum Circuit ---")
    circuit.draw('mpl')  # Visualize the quantum circuit
    plt.show()
