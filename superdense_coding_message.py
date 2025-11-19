"""
Below is the code to implement a chosen message into the superdense coding protocol.
REQUIREMENT TO RUN: must install qiskit using 'pip install qiskit'
MESSAGE WILL TAKE A LONG TIME TO RUN THE LONGER IT IS
"""

# import necessities
from superdense_coding_functions import *
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
from qiskit import generate_preset_pass_manager


"""
Now I want to make a function that takes a string input message of my choice and 
converts it into a bitstring which is split up into pairs, coded into qubits
using superdense coding, and sent to a receiver to be decoded.
"""
message = 'testing' # replace this message with whatever you want to send!
binary_rep = text_to_binary(message) # changed to binary code

# split into pairs of two which go through the superdense coding protocol and
# then rejoin to form a message
binary_list = split_binary_message(binary_rep)

# finding backend for circuit
service = QiskitRuntimeService()
backend = service.least_busy()
sampler = Sampler(mode=backend)
pm = generate_preset_pass_manager(optimization_level=2, backend=backend)


# go through superdense coding protocol for each pair of bits, then recombine the output
# and add it to the string 'coded'. This is the message that was received by Bob.
coded = ''
for bin_element in binary_list:
    # setting up Alice's half of the ebit based on what she wants to send
    qc = initialize_circuit()
    qc = desired_bits(qc, bin_element)

    # Alice now sends her qubit to Bob

    # Bob decodes the qubit, then measures the system of his qubit and the decoded version of
    # the one he received from Alice
    qc = decode(qc)
    qc.measure(range(2), range(1, -1, -1))  # reverse bitstring since output is backwards

    # transpiling circuit for the backend
    transpiled = pm.run(qc)
    job = sampler.run([transpiled], shots=100)
    results = job.result()
    data = results[0].data.c.get_counts()

    # since there is error, determine which is most likely to be correct based on the
    # bitstring count. Only return the bitstring that is most likely.
    num_counts = 0
    probable_key = ''
    for key in data:
        if data[key] > num_counts:
            num_counts = data[key]
            probable_key = key

    coded += probable_key

# Bob decodes the binary message he received from Alice using the given function
decoded_message = binary_to_text(coded)

# Should be same as the inputted message!
print(decoded_message)

