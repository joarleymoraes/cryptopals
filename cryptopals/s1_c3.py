from collections import defaultdict
import json
from string import ascii_letters, printable
from s1_c1 import decimal_to_binary, binary_to_decimal, hex_to_binary
from s1_c2 import binary_to_hex
import string

encrypted_hex_input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

top = 'ETAOINSHRDLU'
top_lower = top.lower()
top_english_letters =' ' + ''.join([u + l for u, l in zip(top, top_lower)])
# print('top_english_letters', top_english_letters)

ASCII = ''.join(chr(x) for x in range(128))

with open('cryptopals/top_3k_en_words.txt') as fp:
	words = fp.readlines()
words = [x.strip() for x in words] 


def hex_frequency(input_str):
	counter = defaultdict(int)
	for i in range(0, len(input_str), 2):
		counter[input_str[i:i+2]] += 1
	return counter

def ascii_letter_to_hex(l):
	return binary_to_hex(decimal_to_binary(ASCII.find(l), 8))

def hex_to_ascii_letter(hex_v):
	return ASCII[binary_to_decimal(hex_to_binary(hex_v))] 

def hex_to_ascii(hex_str):
	str_res = ''
	for i in range(0, len(hex_str), 2):
		hex_v = hex_str[i:i+2]
		str_res += hex_to_ascii_letter(hex_v)
	return str_res


def unxor(v1, r):
	if r:
		v2 = int(not v1)
	else:
		v2 = v1
	return v2


def inverse_bitwise_xor(bin_str1, bin_str_res):
	str_res = ''
	for c1, r in zip(bin_str1, bin_str_res):
		str_res += str(unxor(int(c1), int(r)))
	return str_res


def crack_key(top_letter, en_top_letter):
	bin_top_l = hex_to_binary(top_letter)
	bin_top_en = hex_to_binary(en_top_letter)
	bin_key = inverse_bitwise_xor(bin_top_en, bin_top_l)
	return binary_to_hex(bin_key)



def crack(top_letter, en_top_letter, encrypted_hex):
	decoding_key = ''
	p_key = crack_key(en_top_letter, top_letter)
	bin_key = hex_to_binary(p_key)
	# print('key: {}'.format(hex_to_ascii(p_key)))
	# print('key bin: {}'.format(bin_key))

	hex_clear_text = ''
	for i in range(0, len(encrypted_hex), 2):
		enc_hex = encrypted_hex[i:i+2]
		hex_clear_text += binary_to_hex(inverse_bitwise_xor(bin_key, hex_to_binary(enc_hex)))
	
	
	return hex_clear_text, p_key

def is_printable(str_value):
	for char in str_value:
		if char not in string.printable:
			return False
	return True

def crack_xor_ecryption(encrypted_input, debug=False, check_words=True):

	freq = hex_frequency(encrypted_input)


	i = 0
	cracked = False
	for l in top_english_letters:
		en_top_letter = l
		hex_en = ascii_letter_to_hex(en_top_letter)
		for top_res in sorted_freq:
			if cracked:
				return ct, key
			top_hex = top_res[0]
			hex_ct, hex_key = crack(top_hex, hex_en, encrypted_input)
			
			try:
				ct = hex_to_ascii(hex_ct)
			except IndexError:
				continue


			try:
				key = hex_to_ascii(hex_key)
			except IndexError:
				print('Hey! The key is non-ascii')
	
			if is_printable(ct):
				if check_words:
					for word in ct.split():
						if word in words:
							cracked = True
							break
				else:
					cracked = True

			if debug and cracked:
				print('Possible CLEAR TEXT: ' + ct)
				print('Tried {}  =>  {}'.format(en_top_letter, top_hex))
				print('Key: ' + key)
				print('Found after {} attempts'.format(i + 1))
				print('\n-------------')
				
			i += 1

	return None, None



if __name__ == '__main__':
	crack_xor_ecryption(encrypted_hex_input, True)


