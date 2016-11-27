"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""


from models import File, FileNodes, SplitFile
from scripts import client
from scripts.dev import client2
from management import syncdb
from django.http import HttpResponse, HttpResponseBadRequest
import logging
import os


def download_single_file(request):
    """
    Calls tcp client connection to the
    requested host and port for downloading
    a specific file
    :param request: wsgi request
    :return: files added and removed from sync method
    """
    filename = request.GET.get('filename')
    ip = request.GET.get('ip')
    port = request.GET.get('port')

    client.client_send(ip, port, filename)
    added_files, removed_files = syncdb.sync_files()

    return added_files, removed_files


def download_file_http(request):
    """
    Deprecated method to download files through
    http
    :param request: wsgi request
    :return: response with file
    """
    filename = request.GET.get('filename')
    try:
        fileobj = File.objects.get(name=filename)
    except:
        return HttpResponse('No such file')

    raw_text = open(fileobj.location + fileobj.name, 'rb').read()

    response = HttpResponse(raw_text, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fileobj.name)

    # TODO make it so files are downloaded to the /files/ dir in linux

    logging.debug("Response: {0}".format(response))
    return response


def upload_file(request):
    """
    Upload method to upload files to system, intakes
    a file and splits it up into two pieces, then sends each
    piece to each of the filenodes that are on the system as
    :param request: wsgi request
    :return: None
    """
    filenodes = FileNodes.objects.get(id=1)
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed')
    request_file = request.FILES['myfile']
    with open('/files/%s' % request_file.name, 'wb+') as dest:
        for chunk in request_file.chunks():
            dest.write(chunk)
    size = os.path.getsize('/files/'+request_file.name)
    with open('/files/%s' % request_file.name) as source:
        filenames = ['/files/' + 'first_' + request_file.name, '/files/' + 'second_' + request_file.name]
        with open(filenames[0], 'wb') as dest:
            for data in source.readlines(size/2):
                dest.write(data)
        with open(filenames[1], 'wb') as dest:
            for data in source.readlines(size/2):
                dest.write(data)

    client2.client_send(filenodes.ip_address1, filenodes.port1, filenames[0])
    client2.client_send(filenodes.ip_address2, filenodes.port2, filenames[1])
    for file in filenames:
        os.remove(file)
    added_files, removed_files = syncdb.sync_files()
    split_file = SplitFile()
    split_file.name = request_file.name
    split_file.node1 = filenodes.ip_address1
    split_file.node2 = filenodes.ip_address2
    split_file.port1 = filenodes.port1
    split_file.port2 = filenodes.port2
    split_file.save()
    print added_files
    print removed_files
