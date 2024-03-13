import time
import random
import numpy as np
import matplotlib.pyplot as plt
import DES_judson


def generate_random_hex_string(length=16):
    # Generate a random hex string of the specified length.
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))


def main_test(num_tests=1000, num_rounds=16, key_hex="FFFFFFFFFFFFFFFE"):
    encryption_times = []  # List to store the time taken for each encryption
    roundKeys = DES_judson.keyGenerator(key_hex, num_rounds)
    for _ in range(num_tests):
        start_time = time.time()

        plaintext_hex = generate_random_hex_string()
        DES_judson.encrypt(plaintext_hex, roundKeys, num_rounds)

        end_time = time.time()
        encryption_times.append(end_time - start_time)

    # Calculate the average time
    average_time = np.mean(encryption_times)
    print(f"Average encryption time: {average_time:.5f} seconds")

 
    # # Plot the empirical CDF
    # plt.figure(figsize=(8, 6))
    # plt.hist(encryption_times, bins=100, cumulative=True, density=True, histtype='step', color='blue', label='Empirical CDF')
    # plt.xlabel('Encryption Time (seconds)')
    # plt.ylabel('CDF')
    # plt.title('Empirical Cumulative Distribution Function (CDF) of DES Encryption Time')
    # plt.grid(True)
    # plt.legend()
    # plt.show()


main_test()