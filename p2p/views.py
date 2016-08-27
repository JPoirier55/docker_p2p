from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
import requests
from models import File, Neighbors
import tarfile
import logging
import os

# Create your views here.


def index(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        filename = ''
    aggregate_list = {}
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/filelist'.format(neighbor.ip_address, neighbor.port))
        aggregate_list[neighbor.hostname] = response.text

    return render(request, 'index.html', {'files': aggregate_list,
                                          'filename': filename})


def filelist_api(request):
    filelist = File.objects.all()
    html = ''
    for file in filelist:
        html += file.__str__() + '<br>'
    return HttpResponse(html)


def search_neighbor(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        # TODO tell user to enter a file
        return HttpResponseRedirect('/')

    aggregate_list = {}
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/file?filename={2}'.format(neighbor.ip_address, neighbor.port, filename))

        response = HttpResponse(response.content, content_type='application/x-gzip')

        return response

    return render(request, 'index.html', {'files': aggregate_list,
                                          'filename': filename})


def download_file(request):
    filename = request.GET.get('filename')
    files = File.objects.filter(name=filename)
    print files
    print filename
    if files:
        default = files[0]
        dir = os.getcwd()
        print dir
        raw_text = open(dir + '/p2p/static/files/' + default.name, 'r').read()

        response = HttpResponse(raw_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

        logging.debug("Response: {0}".format(response))
        return response
    else:
        return HttpResponseRedirect('/?filename={0}'.format(filename))
