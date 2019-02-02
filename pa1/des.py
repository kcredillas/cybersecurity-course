import re

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

def main():	
	text = input("What text would you like to encrypt?\r\n")
	text = textprocessing(text)
	binText = ascii2bin(text)
	for x in binText:
		print(x)

if __name__ == '__main__':
	main()
