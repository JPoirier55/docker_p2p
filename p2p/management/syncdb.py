import os

from p2p.models import File


def sync_files():
    added_files = []
    removed_files = []
    file_dir = os.environ['P2P_FILE_DIR']
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            try:
                File.objects.get(name=file)
            except:
                print 'Creating new file: ', file
                File.objects.create_file(file, root)
                added_files.append(file)
                continue
        for file in File.objects.all():
            if file.name not in files:
                print 'Deleting file: ', file.name
                removed_files.append(file.name)
                file.delete()

