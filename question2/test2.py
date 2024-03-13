import os

# TABLES needed for DES BELOW
# IT // use for key prior to first round, takes 64 bit key and takes out every 8th bit out & rearranges values
initialPermutation = [58, 50, 42, 34, 26, 18, 10, 2,
				60, 52, 44, 36, 28, 20, 12, 4,
				62, 54, 46, 38, 30, 22, 14, 6,
				64, 56, 48, 40, 32, 24, 16, 8,
				57, 49, 41, 33, 25, 17, 9, 1,
				59, 51, 43, 35, 27, 19, 11, 3,
				61, 53, 45, 37, 29, 21, 13, 5,
				63, 55, 47, 39, 31, 23, 15, 7]

# inverse inital Permutation // changes order of 64 bit 
inverseInitPerm = [40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25]

# PC-1 table // 64 bit key will become 56-bit key
permutatedChoice_1 = [57, 49, 41, 33, 25, 17, 9,
                    1, 58, 50, 42, 34, 26, 18,
                    10, 2, 59, 51, 43, 35, 27,
                    19, 11, 3, 60, 52, 44, 36,
                    63, 55, 47, 39, 31, 23, 15,
                    7, 62, 54, 46, 38, 30, 22,
                    14, 6, 61, 53, 45, 37, 29,
                    21, 13, 5, 28, 20, 12, 4]

# PC2 // Compression of key f/ 56 bits to 48 bits
permutatedChoice_2 = [14, 17, 11, 24, 1, 5,
                    3, 28, 15, 6, 21, 10,
                    23, 19, 12, 4, 26, 8,
                    16, 7, 27, 20, 13, 2,
                    41, 52, 31, 37, 47, 55,
                    30, 40, 51, 45, 33, 48,
                    44, 49, 39, 56, 34, 53,
                    46, 42, 50, 36, 29, 32]

# Schedule of Left Circular shifts depends on round 
shiftTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# E Bit Selection Table // expands bit string f/ 32 bits --> 48 bits
eBitExpansion = [32, 1, 2, 3, 4, 5, 4, 5,
                6, 7, 8, 9, 8, 9, 10, 11,
                12, 13, 12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21, 20, 21,
                22, 23, 24, 25, 24, 25, 26, 27,
                28, 29, 28, 29, 30, 31, 32, 1]

# Permutation Table // used after the sBox to rearrange values
permutationTable = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# S-box // there is 8 unique s boxes, takes each 6 bit and assigns new value of 4 bits 
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

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
		
def makeFile(newText):
    fileName = input("Filename: ") + ".txt"
    with open(fileName, 'w') as file:
        file.write(newText)

def bin2dec(binary):                    # DELETE Binary to decimal conversion

	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

def dec2bin(num):                       # DELETE Decimal to binary conversion
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

# Permute function to rearrange the bits
def permute(key, permChoice, length_n):
	permutation = ""
	for i in range(0, length_n):
		permutation = permutation + key[permChoice[i] - 1]
	return permutation

# shifting the key bits left by nth shifts (n is desinated by the round #)
def shiftLeft(key, roundShift):
	shiftedKey = ""
	for i in range(roundShift):
		for j in range(1, len(key)):
			shiftedKey = shiftedKey + key[j]
		shiftedKey = shiftedKey + key[0]
		key = shiftedKey
		shiftedKey = ""
	return key

# calculating xor of two strings of binary number a and b
def xor(bitStringA, bitStringB):
    result = int(bitStringA, 2) ^ int(bitStringB, 2)
    # Convert the result back to binary string
    result = bin(result)[2:].zfill(len(bitStringA))
    return result


def encrypt(plaintext, keyBinary, numRounds):
	plaintext = bin(int(plaintext, 16))[2:]
	# Initial Permutation
	plaintext = permute(plaintext, initialPermutation, 64)
	left = plaintext[0:32]                  	# Splitting
	right = plaintext[32:64]
	for i in range(0, numRounds):
		# Expansion D-box: Expanding the 32 bits data into 48 bits
		rightExpanded = permute(right, eBitExpansion, 48)
		xorValue = xor(rightExpanded, keyBinary[i])
		# S-box: substituting the value from s-box table by calculating row and column
		sboxValue = ""
		for j in range(0, 8):
			row = bin2dec(int(xorValue[j * 6] + xorValue[j * 6 + 5]))
			col = bin2dec(int(xorValue[j * 6 + 1] + xorValue[j * 6 + 2] + xorValue[j * 6 + 3] + xorValue[j * 6 + 4]))
			val = sbox[j][row][col]
			sboxValue = sboxValue + dec2bin(val)
		# Straight D-box: After substituting rearranging the bits
		sboxValue = permute(sboxValue, permutationTable, 32)
		result = xor(left, sboxValue)                       # XOR left and sboxValue
		left = result
		# Swapper
		if(i != 15):
			left, right = right, left
		# print("Round ", i + 1, " ", hex(int(left, 2))[2:].upper()," ", hex(int(right, 2))[2:].upper(), " ", keyHex[i]) 
	cipherText = left + right                                      # Concatenate cipherText
	cipherText = permute(cipherText, inverseInitPerm, 64)          # Final permutation: final rearranging of bits to get cipher text
	return cipherText

def keyGenerator(key, numRounds):
    key = bin(int(key, 16))[2:]                     # covert hex to binary
    key = permute(key, permutatedChoice_1, 56)      # input 64bit key & output 56 bit key, use the PC1 table to create new key
    # split key into two halves, i.e., C0 and D0
    left = key[0:28] 
    right = key[28:56] 
    keyBinary = []
    # generate a list of keys for each round
    for i in range(0, numRounds):
        # Shifting the bits by nth shifts by checking from the shift table
        left = shiftLeft(left, shiftTable[i])
        right = shiftLeft(right, shiftTable[i])
        combinedHalves = left + right  # concatenate strings together
        # Compression of key from 56 to 48 bits
        round_key = permute(combinedHalves, permutatedChoice_2, 48)
        keyBinary.append(round_key)
    return keyBinary


# main
numRounds, key, plaintext = readFile()
keyBinary = keyGenerator(key, numRounds)

print(" ************** Encryption **************")
cipherText = encrypt(plaintext, keyBinary, numRounds)
cipherText = hex(int(cipherText, 2))[2:].upper()
print("Ciphertext : ", cipherText)
userAnswer = input("Would you like to write this cipher to a file? \nType '1' (Yes):")
if userAnswer == '1':
    makeFile(cipherText)


