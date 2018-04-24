from s1_c1 import hex_to_binary, hex_alphabet, binary_to_decimal

hex_input = '1c0111001f010100061a024b53535009181c'
hex_xor_input = '686974207468652062756c6c277320657965'
expected_output = '746865206b696420646f6e277420706c6179'

def xor(bit1, bit2):
	return int(not(bit1 == bit2))

def bitwise_xor(bin_str1, bin_str2):
	str_res = ''
	for c1, c2 in zip(bin_str1, bin_str2):
		v1, v2 = int(c1), int(c2)
		str_res += str(xor(v1, v2))
	return str_res

def binary_to_hex(bin_str):
	bits_hex = 4
	start = 0
	end = bits_hex
	hex_res = ''
	while start < len(bin_str):
		chunk = bin_str[start:end]
		decimal = binary_to_decimal(chunk)
		hex_res += hex_alphabet[decimal]
		start += bits_hex
		end += bits_hex
	return hex_res


def hex_xor(hex_input, hex_xor_value):
	bin_input = hex_to_binary(hex_input)
	xor_input = hex_to_binary(hex_xor_value)
	return binary_to_hex(bitwise_xor(bin_input, xor_input))


assert (hex_xor(hex_input, hex_xor_input) == expected_output)

