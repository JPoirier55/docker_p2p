import socket
import argparse
import sys


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
            print 'Connection from: ', client_address

            """ Read filename that is placed in the header of the file """

            file = open("picture.jpg", "wb")

            while True:

                """ Receive file in only 256 byte chunks """
                data = connection.recv(256)

                if data:
                    print "Receiving: ", data
                    file.write(data)

                else:
                    print "End of file, closing..."
                    file.close()
                    break

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
