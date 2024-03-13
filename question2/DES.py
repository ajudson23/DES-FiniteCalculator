
import os


def readFile():
        fileName = input("\n\nInput your test file: ")
        filePath = os.path.abspath(fileName)
        if os.path.exists(filePath):
            with open(filePath, 'r') as file:
                rounds = int(file.readline().strip())
                key = file.readline().strip()
                plaintext = file.readline().strip()
                return rounds, key, plaintext
        else:
            print(f"File '{filePath}' not found.")
            return None, None, None
# Now you can use the variables num_rounds, key_hex, and plaintext_hex in your code

rounds, key, plaintext = readFile()

print("Number of Rounds:", rounds)
print("Key in Hex:", key)
print("Plaintext in Hex:", plaintext)
