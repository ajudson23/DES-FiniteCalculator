import os

def readFile():
    fileName = input("\n\nInput your test file: ")
    filePath = os.path.abspath(fileName)
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            line = file.readline().strip()
            tokens = line.split()                               # Split lines into tokens
            try:
                functF = tokens[0]                              # retrieve f(x)
                functG = tokens[1]                              # retrieve g(x)
            except ValueError:
                print("Invalid binary number format.")
                return None, None, None
            sign = tokens[-1]                                   # retrieve sing (+,-,/,*)
            return functF, functG, sign
    else:
        print(f"File '{filePath}' not found.")
        return None, None, None

def addOrSubtract(functF, functG):
    result = bin(int(functF, 2) ^ int(functG, 2))[2:].zfill(8)
    return result

def multiply(functF, functG):
    result = 0
    for i in range(8):
        if (functG & (1 << i)) != 0:
            result ^= (functF << i)
    result = result % 256
    return bin(result)[2:].zfill(8)

def find_multiplicative_inverse_GF28(a):
    r, prev_r = 0x11B, a
    t, prev_t = 0, 1

    while prev_r != 0:
        quotient = r // prev_r
        r, prev_r = prev_r, r - quotient * prev_r
        t, prev_t = prev_t, t - quotient * prev_t

    if r > 1:
        raise ValueError("Element is not invertible in GF(2^8).")

    if prev_t < 0:
        prev_t += 256

    return prev_t

def divide(a, b):
    inverse_b = find_multiplicative_inverse_GF28(b)
    return multiply(a, inverse_b)

# main
functF, functG, sign = readFile()
print("First number:", functF)
print("Second number:", functG)
print("Sign:", sign)
result = 0

if functF is None and functG is None and sign is None:
    print("Error in input files")
elif sign == '+':
    result = addOrSubtract(functF, functG)
elif sign == '-':
    result = addOrSubtract(functF, functG)
elif sign == '*':
    result = multiply(functF, functG)
elif sign == '/':
    result = divide(functF, functG)

if result is not '0':
    print("Result:", result)
    # go to output function
