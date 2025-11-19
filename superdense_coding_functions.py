# import necessities
# REQUIREMENT TO RUN: must install qiskit using 'pip install qiskit'
from qiskit.circuit import QuantumCircuit


# initialize quantum circuit for the protocol
# Creates a shared e-bit between Alice and Bob
def initialize_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    return qc

# depending on what two bits Alice wants to send....
# function converts 2 qubit circuit into binary message to be sent
def desired_bits(self: QuantumCircuit, desire: str) -> QuantumCircuit:
    circuit = self.copy()
    if desire == '00':
        pass
    elif desire == '01':
        circuit.x(0)
    elif desire == '10':
        circuit.z(0)
    elif desire == '11':
        circuit.z(0)
        circuit.x(0)
    circuit.barrier()
    return circuit

# Bob's function to decode the 2 qubits in his possession and see Alice's message
def decode(self: QuantumCircuit) -> QuantumCircuit:
    circuit = self.copy()
    circuit.cx(0,1)
    circuit.h(0)
    circuit.barrier()
    return circuit



'''
Converts a text string into a binary string (8 bits per character).

    Example:
        'Hi' -> '0100100001101001'
'''
def text_to_binary(message: str) -> str:
    return ''.join(format(ord(char), '08b') for char in message)



'''
Opposite process:
Converts a binary string (multiple of 8 bits) into the original text.

    Example:
        "0100100001101001" → "Hi"
'''
def binary_to_text(binary: str) -> str:
    binary = binary.replace(" ", "").replace("\n", "").replace("\t", "")
    # Safety check: must be multiple of 8
    if len(binary) % 8 != 0:
        raise ValueError(f"Binary string length ({len(binary)}) is not a multiple of 8")

    # Convert every 8 bits → one character
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        text += chr(int(byte, 2))

    return text



'''
function to split binary message into list of pairs of two

    Example: 
        '0100101101' -> ['01','00','10','11','01']
'''
def split_binary_message(message: str) -> list:
    split = []
    for n in range(0, len(message), 2):
        split.append(message[n:n + 2])
    return split
