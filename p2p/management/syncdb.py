import os

from p2p.models import File, FileManager, Neighbors


def sync_files():
    synced_files = []
    file_dir = os.environ['P2P_FILE_DIR']
    for root, dirs, files in os.walk(file_dir):
        print root, dirs, files
        for file in files:
            try:
                File.objects.get(name=file)
            except:
                print 'Creating new file: ', file
                File.objects.create_file(file, root)
                synced_files.append(file)
                continue
    return synced_files



