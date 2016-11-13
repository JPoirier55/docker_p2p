import socket
import sys
import datetime
import argparse


def check_for_file(filename):
    with open('filelist.txt', 'r') as f:
        for line in f:
            local_file_name = line.split(' ')[0]
            file_dir = line.split(' ')[1]
            if local_file_name == filename:
                return file_dir
            else:
                return None


def start_server(serverip, serverport):
    """
    This function starts the server on the designated port and ip address
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (serverip, int(serverport))
    print 'Starting server at: ', server_address[0], ':', server_address[1]
    sock.bind(server_address)

    message_buffer = []

    while True:
        print 'Waiting on message.....'
        # Max length of data is 400 to include the size of the time and ip for each message
        filename, address = sock.recvfrom(400)
        file_location = check_for_file(filename)
        if file_location is None:
            data = 'No file found'

        message = "[" + datetime.datetime.now().strftime("%H:%M:%S") + "] <" + address[0] + ">      " + data

        if len(message_buffer) == 5:
            del message_buffer[0]
            message_buffer.append(message)
        else:
            message_buffer.append(message)
        print message_buffer

        sending_message = ''
        for message in message_buffer:
            sending_message += message + "\n"

        if data:
            sent = sock.sendto(sending_message, address)
            print (sent, address)


def main():
    """
    Main access point for running from terminal commands
    Can use python server.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--serverip', help='use --serverip <serverip>', default='localhost', required=False)
    parser.add_argument('--serverport', help='use --serverport <serverport>', default=13572, required=False)

    args = parser.parse_args()

    start_server(args.serverip, args.serverport)

if __name__ == '__main__':
    sys.exit(main())
