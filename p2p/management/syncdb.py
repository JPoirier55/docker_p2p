import os

from p2p.models import File, Neighbors


def sync_files():
    file_dir = os.environ['P2P_FILE_DIR']
    for root, dirs, files in os.walk(file_dir):
        print root, dirs, files
        file = File.objects.get


