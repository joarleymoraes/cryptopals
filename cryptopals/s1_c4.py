from s1_c3 import crack_xor_ecryption


with open('cryptopals/s1_c4_data.txt') as fp:
	inputs = fp.readlines()

for i in inputs:
	ct, key = crack_xor_ecryption(i.strip())
	if ct:
		print('{} ==> {}, {}'.format(i, ct, key))
		break