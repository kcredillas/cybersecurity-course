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

#KEY GENERATION TABLES
PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def textprocessing(text):
	#text = "Today is Tuesday"
	match = re.split("[^a-zA-Z0-9]", text)
	processed = ""
	for word in match:
		processed += word
	#print(processed)
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
	return [block[i-1] for i in table]
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

def main():	
	#Text preprocessing
	text = input("What text would you like to encrypt?\r\n")
	text = textprocessing(text)
	binText = ascii2bin(text)

	print("Data processing: ")

	countBytes = 0
	for x in binText:
		print(x)
		if countBytes == (len(binText)/2)-1:
			print('')
		countBytes += 1

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
	
	
	



	

	# permute()
	#print("Initial permute")
	#for block in binText:
		#block = int(block)
		#block = permute(block, IP_TABLE)
		
if __name__ == '__main__':
	main()
