"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""


from models import Neighbors, File
import requests
import socket
import json
from django.http import HttpResponse, HttpResponseRedirect


def search_neighbors(request):
    """
    Depth first search for files across neighboring nodes
    :param request: wsgi request
    :return: list of files and meta data
    """
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
            response = requests.get(
                'http://{0}:{1}/api/v1/filelist?filename={2}&hop={3}'.format(neighbor.ip_address, neighbor.port,
                                                                             filename, hop_number), timeout=5)
            response = json.loads(response.text)
            for file in response:
                if filename in file['name']:
                    if file not in aggregate_list:
                        if (file['host'], file['port']) != (host, port) and file['host'] != host_local:
                            aggregate_list.append(file)
        except requests.exceptions.RequestException as e:
            print "Error: Cannot access {0}:{1} -- {2}".format(neighbor.ip_address, neighbor.port, e)
            continue
    return aggregate_list, filename, host, port


def http_dfs_api(request):
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
                response = requests.get(
                    'http://{0}:{1}/api/v1/filelist?filename={2}&hop={3}'.format(neighbor.ip_address,
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

    return json_response


def search_neighbor_single(request):
    neighbors = Neighbors.objects.all()
    filename = request.GET.get('filename')
    if filename is None:
        # TODO tell user to enter a file
        return HttpResponseRedirect('/')

    response = ''
    for neighbor in neighbors:
        response = requests.get(
            'http://{0}:{1}/api/v1/file?filename={2}'.format(neighbor.ip_address, neighbor.port, filename))
        if response.text != 'None':
            response = HttpResponse(response.content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    return response