asd = input("Enter your 12 bit EAN barcode number: ")
tin = [int(i) for i in asd]
odd = 0
even = 0
for k in range(1,12,2):
	odd += tin[k]
for j in range(0,12,2):
	even += tin[j]
checksum = odd*3 + even
checkdigit = checksum % 10
if checkdigit != 0:
	checkdigit = 10 - checkdigit

print(asd+str(checkdigit))
