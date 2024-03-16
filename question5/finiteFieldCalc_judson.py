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

''' 
    This function XORs the two functions using the "^", we use an XOR, since we are not carrying any binary values.
    Adding & subtracting have the same procedure and output.
    f(x) & f(x) are sent in as strings, we convert them to ints for the XOR, & then we make them binary values 
    .zfill gets rid of the '0b' value when you convert to binary 'bin()'
'''
def addOrSubtract(functF, functG):
    result = bin(int(functF, 2) ^ int(functG, 2))[2:].zfill(8)
    return result

'''
This function multiplys the g(x) & f(x). It has checks to see if an 2^8 or 2^7 exists then XORs with appropriate value
for loop will loop 8 times to iterate through all 8 bits and shift g(x) to left & the result being built
'''
def multiply(functF, functG):
    # Convert binary string to integer
    m = int("100011011", 2)
    functF = int(functF, 2)  
    functG = int(functG, 2) 
    result = 0
    for i in range(8):
        result = result << 1                # left shift by 1
        # checks IF there exists a 9th bit then XOR with the m(x) function, meaning it is greater than 256 (2^8)
        if result & 0x100:
            result = result ^ m
        # checks IF the 8th bit is set meaning is it greater than 128 (2^7), then XOR f(x) w/ the result being built
        if functG & 0x80:
            result = result ^ functF
        functG = functG << 1                # left shift by 1
    return bin(result)[2:]                  # covert to binary & take of first two values f/ conversion

'''
calculates  multiplicativeInverse of g(x) in GF(2^8). 
GF(2^8) is represented by an irreducible polynomial
the multiplicativeInverse is found using the extended Euclidean algorithm
'''
def find_multiplicative_inverse_GF28(a):
    r, prev_r = 0x11B, a
    t, prev_t = 0, 1
    # perform extended Euclidean
    while prev_r != 0:
        quotient = r // prev_r
        r, prev_r = prev_r, r - quotient * prev_r
        t, prev_t = prev_t, t - quotient * prev_t
    # if r is greater than 1 then 'a' is not invertible in GF(2^8)
    if r > 1:
        raise ValueError("Element is not invertible in GF(2^8).")
    # check if less than 0, add 256 if negative
    if prev_t < 0:
        prev_t += 256
    #return prev_t
    return format(prev_t, '08b')

'''
This function takes f(x) & g(x). It calculates the inverse of f(g). Then it multiplies f(x) by g(x)^-1
'''
def divide(functF, functG):
    inverse_b = find_multiplicative_inverse_GF28(int(functG, 2))
    return multiply(functF, inverse_b)


# main
functF, functG, sign = readFile()
print("First number:", functF)
print("Second number:", functG)
print("Sign:", sign)
result = '-1'

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

if result != '-1':
    print("Result:", result)
