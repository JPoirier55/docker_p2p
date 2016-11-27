"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""


import socket
import sys
import argparse
import os


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

        sock.send("FILE: {0}\n".format(inputfile))

        header = ""
        while True:
            d = sock.recv(1)
            if d == '\n':
                break
            header += d

        filename = header.split(" ")[1]
        cleanfilename = filename.split("/")[-1]
        filesize = int(header.split(" ")[2])

        file = open(filename, "wb+")

        while True:
            """ Receive file in only 256 byte chunks """
            data = sock.recv(256)
            if '###File not found exception###' in data:
                print 'file not found'
                file.close()
                break

            elif data:
                print "Receiving: ", data
                file.write(data)

            else:
                print "End of file, closing..."
                file.close()
                break

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
