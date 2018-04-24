from s1_c3 import ascii_letter_to_hex
from s1_c2 import hex_xor

input_text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

passphrase = 'ICE'

exp_output = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'


def ascii_xor_encrypt(clear_txt, passphrase):
	enc_res_hex = ''
	for i, c in enumerate(clear_txt):
		len_pass = len(passphrase)
		key_c = passphrase[i%len_pass]
		enc_res_hex += hex_xor(ascii_letter_to_hex(c), ascii_letter_to_hex(key_c))
	return enc_res_hex



assert(ascii_xor_encrypt(input_text, passphrase) == exp_output)




