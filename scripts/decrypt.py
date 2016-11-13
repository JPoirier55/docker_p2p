
"""
Author: Jake Poirier
Date: 1/25/2016
Class: ECE456
Assignment: Lab 1
"""


from cipher_utils import *
import argparse

SPACE = [0, 0, 1, 0, 0, 0, 0, 0]


def decrypt(raw_data, key):
    """
    Decrypts data from a file and writes it to another file
    :param raw_data: incoming data that has been read from a text file
    :param key: list of bits that correspond to the algorithms key
    :return: list of bits that have been decrypted
    """
    decrypted_bits = []
    byte_list = []
    bits = tobits(raw_data)
    blocks = split(bits, 16)

    for block in blocks:
        block_16 = BlockObject(block)

        if len(block_16.bit_string) == 16:
            split_bits = split(block_16.bit_string, 8)
            xor_bits = xor(split_bits[1], key)
            new_bytes = xor_bits + split_bits[0]
            byte_list.append(new_bytes)

        elif len(block_16.bit_string) == 8:
            block_8 = BlockObject(block_16.bit_string)
            xor_bits = xor(block_8.bit_string, key)
            new_bytes = xor_bits + SPACE
            byte_list.append(new_bytes)
        else:
            raise FormatError('There is an incorrect number of bits in packet #{0} '
                              'of object:{1} '.format(block_16.bit_string, block_16))
    for bytes in byte_list:
        decrypted_bits += bytes

    text_decrypted = frombits(decrypted_bits)
    return text_decrypted


def main():
    """
    Main access point for running from terminal commands
    Can use python decrypt.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', help='use --inputfile <filename>', required=True)
    parser.add_argument('--outputfile', help='use --outputfile <filename>', required=True)
    parser.add_argument('--keyfilename', help='use --keyfilename <filename>', required=True)

    args = parser.parse_args()

    key = read_key_file(args.keyfilename)
    iterations = len(key)

    key = read_key_file(args.keyfilename)
    input_message = read_file(args.inputfile)

    for iteration in reversed(range(iterations)):
        input_message = decrypt(input_message, key[iteration])
        write_file(args.outputfile, input_message)

if __name__ == '__main__':
    sys.exit(main())
