def multiplication(a, b):
    m = "100011011" 
    result = 0
    a = int(a, 2)  # Convert binary string to integer
    b = int(b, 2)  # Convert binary string to integer
    m = int(m, 2)  # Convert binary string to integer (modulus polynomial)

    for i in range(8):
        result = result << 1
        if result & 0x100:
            result = result ^ m
        if b & 0x80:
            result = result ^ a
        b = b << 1

    return bin(result)[2:]  # Convert the result back to a binary string and remove the '0b' prefix

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y

def find_inverse(b, a):
    d, x, y = extended_gcd(a, b)
    if d == 1:
        # The inverse exists
        return x % a
    else:
        raise ValueError("Inverse does not exist")


#Result: 01100110

# Example usage:
f_str = "11010000"  # Polynomial f(x) = 0
g_str = "01100110"  # Polynomial g(x) = 1
m_str = "100011011"  # Modulus polynomial m(x) = x^8 + x^4 + x^3 + x + 1

# Convert binary strings to integers
a = int(f_str, 2)
b = int(g_str, 2)
m = int(m_str, 2)


# Find the multiplicative inverse of g(x) mod m(x)
inverse_b = find_inverse(b, m)
print("Inverse of g(x) mod m(x):", bin(inverse_b)[2:])

# Multiply a(x) by the inverse of g(x) modulo m(x)
result_after_inverse = multiplication(f_str, bin(inverse_b)[2:])
print("Result after multiplication by inverse:", result_after_inverse)
