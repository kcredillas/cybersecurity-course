""" 
Name: Kenneth Redillas
Student-ID: 800100241
Assignment: 1
Date: February 6, 2019

State: This program only works for encryption.
"""

import re

#INITIAL PERMUTATION TABLE
IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6, 
64, 56, 48, 40, 32, 24, 16, 8, 
57, 49, 41, 33, 25, 17, 9, 1, 
59, 51, 43, 35, 27, 19, 11, 3, 
61, 53, 45, 37, 29, 21, 13, 5, 
63, 55, 47, 39, 31, 23, 15, 7]

#INVERSE PERMUTATION TABLE
INV_IP_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41, 9, 49, 17, 57, 25]

#KEY GENERATION TABLES
PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

#E_BIT_SELECTION TABLE
E_BIT_SELECTION = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1] 

#S BOX TABLES
S_BOX = [
# Box 1
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
# Box 2

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

# Box 3

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

],

# Box 4
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

# Box 5
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
# Box 6

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

],
# Box 7
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
# Box 8

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]

#P FUNCTION
PERMUTATION_TABLE = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
def textprocessing(text):
	#text = "Today is Tuesday"
	match = re.split("[^a-zA-Z0-9]", text)
	processed = ""
	for word in match:
		processed += word
	print("Text to encrypt: " + processed)
	return processed
def ascii2bin(s=''):
	b = []
	n = len(s)
	if n > 16:
		print("Error: The size of your plain text is more than 64 bits!!!!")

	if n < 16:
		diff = 16 - n
		pad = "\0" * diff
		s += pad
		
	b =[bin(ord(x))[2:].zfill(8) for x in s]
	return b
def getParity(n):
	counter = 0
	for ones in n:
		if ones == '1':
			counter+=1
	if counter % 2 == 0:
		return 1 #EVEN PARITY
	return 0 #ODD PARITY 
def permuteKey(masterKey, table):
	compressedKey = ''
	for i in table:
		compressedKey += masterKey[i-1]
	return compressedKey
def leftShift(bits, numberOfLeftShifts):
	newBits = bits[numberOfLeftShifts:] + bits[:numberOfLeftShifts]
	return newBits
def permute(block, table):
	permutedBlock = ''
	for i in table:
		permutedBlock += block[i-1]
	return permutedBlock
def keyGeneration(key):
	pc1_key = permuteKey(key, PC1)
	c = pc1_key[:28]
	d = pc1_key[28:]
	subKeys = list()

	for i in range(16):
		c_i = leftShift(c, SHIFTS[i])
		d_i = leftShift(d, SHIFTS[i])
		roundKey = permuteKey(c_i+d_i, PC2)
		subKeys.append(roundKey)
		c = c_i
		d = d_i
	
	return subKeys
def functionF(bit32text, bit48key):
	E = permute(bit32text, E_BIT_SELECTION)
	print("Expansion permutation:\n" + E)
	R_iminus1 = E
	xor_result = XOR(R_iminus1, bit48key)
	#S BOX Computation
	#S_BOX[boxnumber][rownumber][column_number]
	#[0:8], [8:16], [16:24], ...
	s_input = list()
	for i in range(0, len(xor_result), 6):
		s_input.append(xor_result[i:i+6])
	print("XOR with key:")
	for i in range(len(s_input)):
		print(s_input[i])
	s_output = s_box(s_input)
	print("S-box substitution: " +  s_output)
	p_function = permute(s_output, PERMUTATION_TABLE)
	print("P-box permutation: " + p_function)
	output = p_function #32bit output
	return output
	#P function
	#return output
def s_box(s_input):
	s_output = list()
	i=0
	for str in s_input:
		first_and_last_bit = str[0]+str[-1]
		middle_bits = str[1:5]
		first_and_last_bit = int(first_and_last_bit, 2)
		middle_bits = int(middle_bits, 2)
		result = S_BOX[i][first_and_last_bit][middle_bits]
		s_output.append(bin(result)[2:].zfill(4)) #convert back to bin string
		i+=1
	s_output = ''.join(s_output)
	return s_output
def XOR(A,B):
	xor = ""
	for i in range(len(A)):
		if A[i] == B[i]:
			xor += '0'
		else:
			xor += '1'
	return xor
def cycle(L_prev, R_prev, subKeys, i = 0):
	print("\nIteration %d:" %(i+1))
	#R0 == L_n
	#L0 == R_n
	print("L_i-1: " + L_prev)
	print("R_i-1: " + R_prev)

	if (i == 15):
		R16 = XOR(L_prev, functionF(R_prev, subKeys[i]))
		L16 = R_prev
		preoutput = R16 + L16
		output = permute(preoutput, INV_IP_TABLE)
		print("XOR with L_i-1 [this is R_i-1]:\n%s" %(R16))
		print("End of iteration: %d\n" %(i+1))
		print("Final permutation:\n%s" %(output))
		return output
	
	f = functionF(R_prev, subKeys[i])
	L_i = R_prev
	R_i = XOR(L_prev, f)
	print("XOR with L_i-1 [this is R_i]: " + R_i)
	print("End of iteration: %d" %(i+1))
	return cycle(L_i, R_i, subKeys, i+1)



def main():	
	#Text preprocessing
	# text = input("What text would you like to encrypt?\r\n")
	fobj = open("plaintext.txt", 'r')
	text = fobj.read()
	fobj.close()
	text = textprocessing(text)
	binText = ascii2bin(text)

	print("Data processing: ")

	countBytes = 0
	for x in binText:
		print(x)
		if countBytes == (len(binText)/2)-1:
			print('')
		countBytes += 1
	binText = ''.join(binText)

	#Key generation!
	q = 1
	key  = ''
	while q != 0:
		key = input("What key would you like? [must be 8 ASCII characters long]\r\n")
		key = textprocessing(key)
		if len(key) != 8:
			print("Invalid key length! Your key was " + str(len(key)) + " ASCII characters long. Your key length must be 8.")
			continue
		q = 0
	binKey =[bin(ord(i))[2:].zfill(7) for i in key]
	i = 0
	for e in binKey:
		flag = getParity(e)
		if (flag == 1): #EVEN PARITY CHECK
			e += '1'
		else:
			e += '0'
		binKey[i] = e
		i += 1
	bit64 = ''.join(binKey)
	
	print("Key before permute but after parity is:\n" + bit64)
	print("Key after permute is:\n" + permuteKey(bit64, PC1))
	roundKeys = keyGeneration(bit64)
	for i in range(len(roundKeys)):
		print("Subkey %d is:\n%s" %(i, roundKeys[i]))
	
	#DES 1st round
	inputBlock = permute(binText, IP_TABLE)
	print("Initial permutation result:\n%s" % (inputBlock))
	L0 = inputBlock[:32] #splitting
	R0 = inputBlock[32:]
	output = cycle(L0, R0, roundKeys)
	fobj = open("binarytext.bin", 'wb')
	fobj.write(output.encode())
	fobj.close()
		
if __name__ == '__main__':
	main()
