import socket
import sys
import argparse

def client_send(ip, portnum, inputfile):
    """
    Client module that sends a file to the server depending on user inputs
    :param ip: incoming ip address from user args
    :param port: incomping port number from user args
    :param inputfile: file to be sent to server
    :return: None
    """

    """ Create socket with sock stream --> TCP"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind socket to args from user as IP, portnum tuple """
    server_address = (ip, int(portnum))

    print "Socket connecting on ", server_address
    sock.connect(server_address)

    try:

        """ Open file and read 256 bytes at a time, as well as filename """
        file = open(inputfile, 'rb')
        readfile = file.read(256)
        while readfile:
            sock.send(readfile)
            readfile = file.read(256)

        file.close()

    finally:
        sock.close()


def main():
    """
    Main access point for running from terminal commands
    Can use python client.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--serverip', help='use --serverip <serverip>', required=True)
    parser.add_argument('--serverport', help='use --serverport <serverport>', required=True)
    parser.add_argument('--inputfile', help='use --inputfile <filename>', required=False)

    args = parser.parse_args()

    client_send(args.serverip, args.serverport, args.inputfile)


if __name__ == '__main__':
    sys.exit(main())
