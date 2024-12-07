from qiskit import QuantumCircuit
import numpy as np

# Function to simulate a quantum state vector for a 2-qubit system
def simulate_quantum_circuit(qc):
    """
    Simulate the state vector of the quantum circuit manually without using Aer.
    This function will compute the quantum state after applying the gates.
    """
    # Initialize the quantum state |00>
    state = np.array([1, 0, 0, 0])  # State |00> as a 2-qubit system

    # Apply X gate (bit-flip)
    if any(inst.operation.name.lower() == 'x' for inst in qc.data):
        state = np.array([0, 1, 0, 0])  # Apply X to the first qubit (|1> on the first qubit)

    # Apply Hadamard gate (H) on the second qubit (this creates superposition)
    if any(inst.operation.name.lower() == 'h' for inst in qc.data):
        hadamard = np.array([1, 1]) / np.sqrt(2)
        state = np.kron(state[:2], hadamard)  # Apply Hadamard to the second qubit

    # Apply CNOT gate (controlled-X)
    if any(inst.operation.name.lower() == 'cx' for inst in qc.data):
        # CNOT gate flips the second qubit if the first qubit is |1>
        if state[1] == 1:  # The control qubit is 1
            state[3] = state[2]
            state[2] = 0

    # Return the state vector
    return state

# Function to generate a quantum signature for a given message
def generate_signature(message):
    """
    Alice generates a quantum signature for the given message.
    The message is a binary string ('0' or '1') representing the quantum state.
    """
    if message not in ['0', '1']:
        raise ValueError("Message must be '0' or '1'.")
    
    # Create a quantum circuit with 2 qubits (1 for message bit and 1 for signature bit)
    qc = QuantumCircuit(2, 1)

    # Encode the message as a quantum state (for simplicity, use 0 for "no signature" and 1 for "signature")
    if message == '1':
        qc.x(0)  # Apply X gate to the first qubit if message bit is '1' (this creates the state |1>)

    # Entangle the qubits
    qc.h(1)  # Hadamard gate on the second qubit (creates superposition)
    qc.cx(0, 1)  # CNOT gate between qubit 0 (message) and qubit 1 (signature)
    
    # Measure the signature qubit
    qc.measure(1, 0)
    
    return qc

# Function to simulate the verification of the signature (based on quantum state simulation)
def verify_signature(qc):
    """
    Bob verifies the quantum signature by simulating the quantum circuit and checking the result.
    """
    # Simulate the quantum circuit and get the final quantum state
    state = simulate_quantum_circuit(qc)
    
    # Check if the signature qubit is |1> (the second qubit in the state vector)
    # After the CNOT gate, the signature qubit (qubit 1) should have the value |1> if it was correctly entangled.
    signature = state[3]  # The second qubit is the signature qubit
    
    if signature == 1:
        return '1'  # Signature verified successfully
    else:
        return '0'  # Signature verification failed

# Function to simulate sending and verifying multiple messages
def simulate_communication(messages):
    """
    Simulate sending and verifying multiple messages with quantum signatures.
    """
    for message in messages:
        print(f"Alice's message: {message}")
        
        try:
            # Alice generates quantum signature for the message
            signature_circuit = generate_signature(message)
            print("Quantum Circuit for Signature Generation:")
            print(signature_circuit.draw())

            # Bob verifies the signature by simulating the circuit
            verification_result = verify_signature(signature_circuit)
            print(f"Verification result: {verification_result}")

            # Check if the message was verified correctly
            if verification_result == '1':
                print("Signature verified successfully!")
            else:
                print("Verification failed!")
        except ValueError as e:
            print(f"Error: {e}")

# Main function to interact with the user
def main():
    print("Welcome to the Quantum Digital Signature Simulator!")
    
    # Interactive input for messages
    while True:
        # Ask user for a message (can be '0' or '1')
        message = input("Enter a message to send (binary '0' or '1', or type 'exit' to quit): ")
        
        if message == 'exit':
            print("Exiting the simulation...")
            break

        # Ensure valid input
        if message not in ['0', '1']:
            print("Invalid input. Please enter '0' or '1'.")
            continue
        
        # Run the simulation for the single message
        simulate_communication([message])

        # Ask if the user wants to send more messages
        more_messages = input("Do you want to send another message? (yes/no): ")
        if more_messages.lower() != 'yes':
            print("Exiting the simulation...")
            break

# Run the main function
if __name__ == "__main__":
    main()



#with "aer"
# from qiskit import QuantumCircuit, Aer, execute

# # Function to generate a quantum signature for a given message
# def generate_signature(message):
#     """
#     Alice generates a quantum signature for the given message.
#     The message is a binary string ('0' or '1') representing the quantum state.
#     """
#     if message not in ['0', '1']:
#         raise ValueError("Message must be '0' or '1'.")
    
#     # Create a quantum circuit with 2 qubits (1 for message bit and 1 for signature bit)
#     qc = QuantumCircuit(2, 1)

#     # Encode the message as a quantum state (for simplicity, use 0 for "no signature" and 1 for "signature")
#     if message == '1':
#         qc.x(0)  # Apply X gate to the first qubit if message bit is '1' (this creates the state |1>)

#     # Entangle the qubits
#     qc.h(1)  # Hadamard gate on the second qubit (creates superposition)
#     qc.cx(0, 1)  # CNOT gate between qubit 0 (message) and qubit 1 (signature)
    
#     # Measure the signature qubit
#     qc.measure(1, 0)
    
#     return qc

# # Function to simulate the verification of the signature using Aer
# def verify_signature(qc):
#     """
#     Bob verifies the quantum signature by simulating the quantum circuit and checking the result.
#     """
#     # Use the Aer simulator to simulate the quantum circuit
#     simulator = Aer.get_backend('qasm_simulator')
    
#     # Execute the quantum circuit
#     job = execute(qc, simulator, shots=1)
    
#     # Get the result of the simulation
#     result = job.result()
    
#     # Get the measurement outcomes
#     counts = result.get_counts(qc)
    
#     # The signature is verified if the measurement result is '1'
#     if '1' in counts:
#         return '1'  # Signature verified successfully
#     else:
#         return '0'  # Signature verification failed

# # Function to simulate sending and verifying multiple messages
# def simulate_communication(messages):
#     """
#     Simulate sending and verifying multiple messages with quantum signatures.
#     """
#     for message in messages:
#         print(f"Alice's message: {message}")
        
#         try:
#             # Alice generates quantum signature for the message
#             signature_circuit = generate_signature(message)
#             print("Quantum Circuit for Signature Generation:")
#             print(signature_circuit.draw())

#             # Bob verifies the signature by simulating the circuit
#             verification_result = verify_signature(signature_circuit)
#             print(f"Verification result: {verification_result}")

#             # Check if the message was verified correctly
#             if verification_result == '1':
#                 print("Signature verified successfully!")
#             else:
#                 print("Verification failed!")
#         except ValueError as e:
#             print(f"Error: {e}")

# # Main function to interact with the user
# def main():
#     print("Welcome to the Quantum Digital Signature Simulator!")
    
#     # Interactive input for messages
#     while True:
#         # Ask user for a message (can be '0' or '1')
#         message = input("Enter a message to send (binary '0' or '1', or type 'exit' to quit): ")
        
#         if message == 'exit':
#             print("Exiting the simulation...")
#             break

#         # Ensure valid input
#         if message not in ['0', '1']:
#             print("Invalid input. Please enter '0' or '1'.")
#             continue
        
#         # Run the simulation for the single message
#         simulate_communication([message])

#         # Ask if the user wants to send more messages
#         more_messages = input("Do you want to send another message? (yes/no): ")
#         if more_messages.lower() != 'yes':
#             print("Exiting the simulation...")
#             break

# # Run the main function
# if __name__ == "__main__":
#     main()


