import math

input_hex = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
hex_alphabet = '0123456789abcdef'
bs4_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
expected_bs4 = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def hex_to_binary(hex_str):
    binray_str = ''
    for i, c in enumerate(hex_str.lower()):
        binray_str += decimal_to_binary(int(hex_alphabet.find(c)), 4)

    return binray_str

def decimal_to_binary(decimal, nbits):
    bin_str = ''
    reamining = decimal
    for i in range(nbits - 1, -1, -1):
        power = int(math.pow(2, i))
        if power <= reamining:
            bin_str += '1'
            reamining -= power
        else:
            bin_str += '0'
    return bin_str

def binary_to_decimal(bin_str):
    decimal = 0
    for (c, i) in zip(bin_str, range(len(bin_str) - 1, -1, -1)):
        if int(c):
            decimal += int(math.pow(2, i))
    return decimal


def binary_to_bs64(bin_str):
    """
    Assumes binary string is multiple of 8 (byte)
    """
    block_size = 24
    bits_bs64 = 6
    start = 0
    end = bits_bs64
    bs64_res = ''
    while end <= len(bin_str):
        chunk_size = 0
        padded = 0
        for i in range(block_size/bits_bs64):
            chunk = bin_str[start:end]
            chunk_size = len(chunk)
            zero_padding = ''
            if chunk_size < bits_bs64:
                n_padding = bits_bs64 - chunk_size
                zero_padding = '0'*n_padding
                chunk += zero_padding
                padded += 1
            
            start += bits_bs64
            end += bits_bs64
            last_iter = not (end <= len(bin_str))
            if last_iter and i > 1 and chunk == '0'*6:
                bs64_res += '='
            else:
                decimal = binary_to_decimal(chunk)
                bs64_res += bs4_alphabet[decimal]
            

    return bs64_res


def hex_to_bs64(hex_str):
    return binary_to_bs64(hex_to_binary(hex_str))



assert (hex_to_bs64(input_hex) == expected_bs4)









