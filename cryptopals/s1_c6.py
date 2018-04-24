from s1_c3 import ascii_letter_to_hex, crack_xor_ecryption

from s1_c2 import binary_to_hex
from s1_c1 import hex_to_binary, bs4_alphabet, decimal_to_binary
import json
from collections import defaultdict

encrypted_file = 'cryptopals/s1_c6_data.txt'

def binary_hamm_distance(bin_str_1, bin_str_2):
	distance = 0
	for s1, s2 in zip(bin_str_1, bin_str_2):
		if s1 != s2:
			distance += 1
	return distance


def ascii_str_to_binary(ascii_str):
	bin_str = ''
	for c in ascii_str:
		bin_str += hex_to_binary(ascii_letter_to_hex(c))
	return bin_str


def base64_to_binary(bs64_str):
	bin_res = ''
	bits_bs64_char = 6
	for c in bs64_str:
		decimal = bs4_alphabet.find(c)
		if decimal:
			bin_res += decimal_to_binary(decimal, bits_bs64_char)
		else:
			bin_res += '0'*bits_bs64_char
	return bin_res


def base64_to_hex(bs64_str):
	return binary_to_hex(base64_to_binary(bs64_str))


'''
str1 = 'this is a test'
str2 = 'wokka wokka!!!'

assert(binary_hamm_distance(ascii_str_to_binary(str1), ascii_str_to_binary(str2)) == 37)

assert(base64_to_hex('HUIfTQsPAh9PE048GmllH0kcDk4TAQsHThsBFkU2AB4BSWQgVB0dQzNTTmVS') == '1d421f4d0b0f021f4f134e3c1a69651f491c0e4e13010b074e1b01164536001e01496420541d1d4333534e6552')
'''

def read_bs64_file(filename):
	with open(filename) as fp:
		return ''.join([l.strip() for l in fp.readlines()])

def norm_avg_hamm_dist(bin_str, key_size):
	avg_distance = 0.0
	blocks = []
	block_len = key_size*8
	start = 0
	end = block_len	
	while end < len(bin_str):
		blocks.append(bin_str[start:end])
		start += block_len
		end += block_len
	count = 0
	for i in range(len(blocks) - 1):
		avg_distance += float(binary_hamm_distance(blocks[i], blocks[i + 1]))/block_len
		count += 2 
	return avg_distance/count

def get_blocks(enc_hex_str, key_size):
	block_size = key_size*2
	start = 0
	end = block_size
	blocks = defaultdict(str)
	while start <= len(enc_hex_str):
		block = enc_hex_str[start:end]
		bs = 0
		be = 2
		i = 0
		while be <= len(block):
			blocks[i] += block[bs:be]
			bs += 2
			be += 2
			i += 1
		start += block_size
		end += block_size
	return blocks

def solve_blocks(blocks):
	final_key = ''
	final_ct = ''
	ct_dict = defaultdict(str)
	for block in blocks.values():
		# print('block =>', block)
		ct, key = crack_xor_ecryption(block, debug=False, check_words=False)
		
		if ct and key:
			# print('key => ', key)
			final_key += key
			for i, c in enumerate(ct):
				ct_dict[i] += c
		else:
			return None, None

	for i in sorted(ct_dict.keys()):
		final_ct += ct_dict[i]

	return final_key, final_ct

def crack_repeating_key_xor(raw_bin_enc):
	min_key_size = 2
	max_key_size = 100
	distances = {}
	for i in range(min_key_size, max_key_size, 1):
		distances[str(i)] = norm_avg_hamm_dist(raw_bin_enc, i)
	
	distances = sorted(distances.iteritems(), key=lambda (k,v): (v,k))
	# print(distances)
	hex_enc = binary_to_hex(raw_bin_enc)
	for dis in distances[:4]:
		key_size = int(dis[0])
		# print('Trying key_size = {}'.format(key_size))
		blocks = get_blocks(hex_enc, key_size)
		#print(blocks)
		final_key, final_ct = solve_blocks(blocks)
		if final_key and final_ct:
			# print('final_key', final_key)
			# print('final_ct', final_ct)
			return final_key, final_ct
			

	return None, None

	# print(json.dumps(distances[:5], indent=2))	

if __name__ == '__main__':
	raw_bs64 = read_bs64_file(encrypted_file)
	raw_bin_enc = base64_to_binary(raw_bs64)
	key, ct = crack_repeating_key_xor(raw_bin_enc)
	if key and ct:
		print('DECRYPTED')
		print('key: ', key)
		print('clear text: ', ct)
	else:
		print('Could not decrypt')


		
		
