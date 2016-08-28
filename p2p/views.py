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
    host, port = request.META['HTTP_HOST'].split(':')
    filelist = File.objects.all()
    json_response = []
    for file in filelist:
        json_response.append({'name': file.name,
                              'location': file.location,
                              'category': file.category,
                              'host': host,
                              'port': port})

    return HttpResponse(json.dumps(json_response))


def search_results(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        filename = ''
    aggregate_list = []
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/filelist'.format(neighbor.ip_address, neighbor.port))
        print response.text
        response = json.loads(response.text)
        print response
        for file in response:
            if filename in file['name']:
                aggregate_list.append(file)
    return render(request, 'results1.html', {'files': aggregate_list,
                                             'filename': filename})


def search_page(request):
    return render(request, 'search_page.html')


def search_neighbor(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        # TODO tell user to enter a file
        return HttpResponseRedirect('/')

    aggregate_list = {}
    response = ''
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/file?filename={2}'.format(neighbor.ip_address, neighbor.port, filename))
        if response.text != 'None':

            response = HttpResponse(response.content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    return response


def download_file(request):
    filename = request.GET.get('filename')
    files = File.objects.filter(name=filename)

    if files is not None or len(files) != 0:
        default = files[0]
        raw_text = open(default.location + default.name, 'rb').read()

        response = HttpResponse(raw_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(default.name)

        logging.debug("Response: {0}".format(response))
        return response
    else:
        return HttpResponse('None')
