from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import requests
from models import File, Neighbors, SplitFile
import logging
from management import syncdb
import socket
from django.views.decorators.csrf import csrf_exempt

from scripts import client


def index(request):
    syncdb.sync_files()
    return render(request, 'upload.html')


def local_files(request):
    json_response = []
    filelist = File.objects.all()
    for file in filelist:
        json_response.append({'name': file.name,
                              'location': file.location,
                              'category': file.category,
                              'host': 'localhost',
                              })

    return render(request, 'local_files.html', {'files': json_response})


def search_results(request):
    neighbors = Neighbors.objects.all()
    host, port = request.META['HTTP_HOST'].split(':')
    filename = request.GET.get('filename')
    hop_number = int(request.GET.get('hop', '0'))
    host_local = socket.gethostbyname(socket.gethostname())
    if filename is None:
        filename = ''
    aggregate_list = []
    for neighbor in neighbors:
        try:
            response = requests.get('http://{0}:{1}/api/v1/filelist?filename={2}&hop={3}'.format(neighbor.ip_address, neighbor.port, filename, hop_number), timeout=5)
            response = json.loads(response.text)
            for file in response:
                if filename in file['name']:
                    if file not in aggregate_list:
                        if (file['host'], file['port']) != (host, port) and file['host'] != host_local:
                            aggregate_list.append(file)
        except requests.exceptions.RequestException as e:
            print "Error: Cannot access {0}:{1} -- {2}".format(neighbor.ip_address, neighbor.port, e)
            continue

    return render(request, 'results1.html', {'files': aggregate_list,
                                             'filename': filename,
                                             'host': host,
                                             'port': port})


def search_page(request):
    return render(request, 'search_page.html')


def search_neighbor(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        # TODO tell user to enter a file
        return HttpResponseRedirect('/')

    response = ''
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/file?filename={2}'.format(neighbor.ip_address, neighbor.port, filename))
        if response.text != 'None':

            response = HttpResponse(response.content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    return response


@csrf_exempt
def upload_page(request):
    return render(request, 'upload.html')


def test_page(request):
    ip = '172.17.0.3'
    file = 'test.txt'
    return render(request, "test.html", {'file': file})


# ---------------API SECTION-------------------------

def test_api(request):

    ip = '172.17.0.1'
    client.client_send(ip, '65000', 'test.txt')

    return HttpResponseRedirect("/test")


def download_split_tcp(request):
    filename = request.GET.get('filename', 'test')
    try:
        fileobj = SplitFile.objects.get(name=filename)
        client.client_send(fileobj.node1, fileobj.port1, '/files/split1.txt')
        client.client_send(fileobj.node2, fileobj.port2, '/files/split2.txt')

        return HttpResponseRedirect('/')
    except:
        return HttpResponse('No such file')


def download_file_tcp(request):
    filename = request.GET.get('filename')
    ip = request.GET.get('ip')
    port = request.GET.get('port')

    client.client_send(ip, port, filename)
    added_files, removed_files = syncdb.sync_files()
    print added_files
    print removed_files
    return HttpResponseRedirect('/search_results')


def sync_files(request):
    added_files, removed_files = syncdb.sync_files()
    return render(request, 'sync_results.html', {'added_files': added_files,
                                                 'removed_files': removed_files})


def download_file(request):
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


def filelist_api(request):
    host, port = request.META['HTTP_HOST'].split(':')
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    hop_number = int(request.GET.get('hop'))
    hop_number += 1
    filelist = File.objects.all()
    json_response = []
    for file in filelist:
        json_response.append({'name': file.name,
                              'location': file.location,
                              'category': file.category,
                              'host': host,
                              'port': port})
    if filename is None:
        filename = ''
    if len(neighbors) != 0 and hop_number < 5:
        for neighbor in neighbors:
            try:
                response = requests.get('http://{0}:{1}/api/v1/filelist?filename={2}&hop={3}'.format(neighbor.ip_address,
                                                                                                     neighbor.port,
                                                                                                     filename,
                                                                                                     hop_number), timeout=5)
                response = json.loads(response.text)
                for response_file in response:
                    if filename in response_file['name']:
                        json_response.append({'name': response_file['name'],
                                              'location': response_file['location'],
                                              'category': response_file['category'],
                                              'host': response_file['host'],
                                              'port': response_file['port']})
            except requests.exceptions.RequestException as e:
                print "Error: Cannot access {0}:{1} -- {2}".format(neighbor.ip_address, neighbor.port, e)
                continue

    return HttpResponse(json.dumps(json_response))


@csrf_exempt
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed')
    file = request.FILES['myfile']
    with open('/files/%s' % file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    added_files, removed_files = syncdb.sync_files()
    return HttpResponse("file uploaded")

