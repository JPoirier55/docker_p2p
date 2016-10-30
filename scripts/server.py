import socket
import argparse
import sys
import os

def create_server(ip, portnum):
    """
    Creates a TCP socket server at a given ip address and port number
    :param ip: incoming ip address from user args
    :param portnum: incoming port number from user args
    :return: None
    """

    """ Create socket with sock stream --> TCP"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind socket to args from user as IP, portnum tuple """
    server_address = (ip, int(portnum))

    print "Starting socket on "
    sock.bind(server_address)

    """ listen to any incoming connections from client """
    sock.listen(1)
    while True:
        print "Waiting for client connection...."
        connection, client_address = sock.accept()
        try:

            """ Receive file in only 256 byte chunks """

            header = ""
            while True:
                d = connection.recv(1)
                if d == '\n':
                    filename = header.split(" ")[1]
                    if os.path.isfile(filename):
                        file = open(filename, 'rb')

                        connection.sendall("FILE: {0} {1}\n".format(filename, os.stat(filename).st_size))
                        readfile = file.read(256)
                        while readfile:
                            connection.sendall(readfile)
                            readfile = file.read(256)

                        file.close()
                        break
                    else:
                        connection.sendall("FILE: {0} {1}\n".format(filename, 0))
                        connection.sendall("###File not found exception###")
                        break
                header += d


        finally:
            connection.close()



def main():
    """
    Main access point for running from terminal commands
    Can use python server.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--serverip', help='use --serverip <serverip>', required=True)
    parser.add_argument('--serverport', help='use --serverport <serverport>', required=True)

    args = parser.parse_args()

    create_server(args.serverip, args.serverport)


if __name__ == '__main__':
    sys.exit(main())
