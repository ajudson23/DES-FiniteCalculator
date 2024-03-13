import binascii
import time
import random
import numpy as np
import matplotlib.pyplot as plt

# Initial and Inverse Initial Permutation tables
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]


def hex_to_bin(hex_val):
    bin_val = bin(int(hex_val, 16))[2:].zfill(64)
    return bin_val


def permute(bin_str, table):
    return ''.join([bin_str[i - 1] for i in table])


def round_function(right_half, key):
    xor_result = int(right_half, 2) ^ int(key, 2)
    return bin(xor_result)[2:].zfill(len(right_half))


def des_encrypt(plaintext_hex, key_hex, num_rounds):
    key_bin = hex_to_bin(key_hex)
    plaintext_bin = hex_to_bin(plaintext_hex)
    permuted_input = permute(plaintext_bin, IP)
    left, right = permuted_input[:32], permuted_input[32:]

    for _ in range(num_rounds):
        round_key = key_bin
        new_right = round_function(right, round_key)
        left, right = right, new_right

    final_bin = left + right
    cipher_bin = permute(final_bin, IP_1)
    cipher_hex = hex(int(cipher_bin, 2))[2:].zfill(16).upper()
    return cipher_hex


def read_input_and_encrypt():
    file_path = input("Please enter the path to your input file: ").strip()
    # Extract index number from file name
    index_number = file_path.split('_')[-1].split('.')[0]

    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_rounds = int(lines[0].strip())
        key_hex = lines[1].strip()
        plaintext_hex = lines[2].strip()

    ciphertext_hex = des_encrypt(plaintext_hex, key_hex, num_rounds)

    # Construct output file name based on the input file's index number
    output_file_name = f"Mayberry_output_{index_number}.txt"  # Replace 'Smith' with the actual last name
    with open(output_file_name, 'w') as file:
        file.write(ciphertext_hex)
    print(f"Ciphertext saved to {output_file_name}")


def generate_random_hex_string(length=16):
    # Generate a random hex string of the specified length.
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def main_test(num_tests=1000, num_rounds=16, key_hex="FFFFFFFFFFFFFFFE"):
    encryption_times = []  # List to store the time taken for each encryption

    for _ in range(num_tests):
        start_time = time.time()

        plaintext_hex = generate_random_hex_string()
        des_encrypt(plaintext_hex, key_hex, num_rounds)

        end_time = time.time()
        encryption_times.append(end_time - start_time)

    # Calculate the average time
    average_time = np.mean(encryption_times)
    print(f"Average encryption time: {average_time:.5f} seconds")

    # Plot the empirical CDF
    plt.figure(figsize=(8, 6))
    plt.hist(encryption_times, bins=100, cumulative=True, density=True, histtype='step', color='blue', label='Empirical CDF')
    plt.xlabel('Encryption Time (seconds)')
    plt.ylabel('CDF')
    plt.title('Empirical Cumulative Distribution Function (CDF) of DES Encryption Time')
    plt.grid(True)
    plt.legend()
    plt.show()


prompt = input("Make a selection: \n1 for single file test with I/O\n2 for random 1K encryption test\n")
if prompt == '1':
    read_input_and_encrypt()
elif prompt == '2':
    main_test()