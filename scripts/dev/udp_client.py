import socket
import sys
import argparse
import time


def send_and_check(message, server_address, sock):
    """
    Takes in message and server address, ip and port, and checks sent status
    resends if the message is not blank, and the data returned is none
    :param message: message to be sent to server
    :param server_address: tuple of ip address and port number
    :param sock: instance of the socket we created in connect_to_server
    :return: data if there isn't a failure to receive data from server
    """
    sock.sendto(message, server_address)

    data, server = sock.recvfrom(4096)

    return data

def connect_to_server(serverip, serverport, inputfile, input):
    """
    Client socket connection to server through incoming parameters
    :param serverip: ip of the server destination
    :param serverport: port of the server destination
    :param inputfile: file with current message to be sent
    :return: None
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (serverip, int(serverport))

    message = ""
    if inputfile is not None:
        try:
            with open(inputfile, "r") as f:
                message = f.read()
        except Exception, e:
            sys.stderr("Cannot open file: ", e)
    else:
        message = input

    if len(message) > 250:
        sys.stderr("Input message is too large, must be < 250 chars")
        return None

    try:

        print "Message to be sent: ", message

        print "Waiting for received data from server...."

        print send_and_check(message, server_address, sock)

    finally:
        print "Data received: closing socket"
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
    while(1):
        if args.inputfile:
            connect_to_server(args.serverip, args.serverport, args.inputfile, None)
        else:
            input = raw_input("Enter a message to send")
            connect_to_server(args.serverip, args.serverport, None, input+" ")


if __name__ == '__main__':
    sys.exit(main())
