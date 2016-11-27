"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""


from models import File
from scripts import client
from management import syncdb
from django.http import HttpResponse, HttpResponseBadRequest
import logging


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
    Upload method to upload files to system
    :param request: wsgi request
    :return: None
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed')
    file = request.FILES['myfile']
    with open('/files/%s' % file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    added_files, removed_files = syncdb.sync_files()
