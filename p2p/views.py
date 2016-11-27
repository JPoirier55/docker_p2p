"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""

from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from models import File, SplitFile
from management import syncdb
import search_methods
import file_methods
import os
from django.views.decorators.csrf import csrf_exempt

from scripts import client


def index(request):
    """
    Main page to upload documents
    :param request: wsgi request
    :return: render upload page
    """
    syncdb.sync_files()
    return render(request, 'upload.html')


def local_files(request):
    """
    Lists files on the system/container locally
    in whatever directory is preset - default is /files/
    :param request: wsgi request
    :return: render local_files page with file list
    """
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
    """
    Page that shows all files on neighboring nodes.
    Does a depth first search across nodes with GET requests,
    combines all known files local to those systems, and
    flushes any files that are local to the system doing the
    initial calling.
    There is a set default maximum of 5 hops, which is calculated
    within the filelist API for each node.
    Neighboring nodes must be added to django admin database to
    allow any searching. See future work/improvements page on
    github at https://github.com/JPoirier55/docker_p2p/wiki/Future-work-and-improvements
    :param request: wsgi request
    :return: render results page with filelist and meta data
    """
    aggregate_list, filename, host, port = search_methods.search_neighbors(request)
    return render(request, 'results1.html', {'files': aggregate_list,
                                             'filename': filename,
                                             'host': host,
                                             'port': port})


def search_page(request):
    """
    Simple page to search for files by name,
    redirect within javascript
    :param request: wsgi request
    :return: render search page
    """
    return render(request, 'search_page.html')


def search_neighbor(request):
    """
    Deprecated method that previously searched nodes and
    allowed for downloading the files searched for directly
    to the machine that was loading the page
    :param request: wsgi request
    :return: response with file object
    """
    response = search_methods.search_neighbor_single(request)
    return response


@csrf_exempt
def upload_page(request):
    """
    Main home page that allows for uploading
    documents to the node/system
    :param request: wsgi request
    :return: render upload page
    """
    return render(request, 'upload.html')


def test_page(request):
    """
    TESTING downloads
    :param request:
    :return:
    """
    ip = '172.17.0.3'
    file = 'test.txt'
    return render(request, "test.html", {'file': file})


# ---------------API SECTION-------------------------

def test_api(request):
    """
    TESTING tcp connection between nodes
    :param request:
    :return:
    """
    ip = '172.17.0.1'
    client.client_send(ip, '65000', 'test.txt')

    return HttpResponseRedirect("/test")


def download_split_tcp(request):
    """
    Method for splitting file across different connected
    nodes. Purpose is to allow a master node which can be accessed
    by the hosting system, to upload and download files that are
    split up, and encrypted with different keys for each piece.
    :param request: wsgi request
    :return: redirect
    """
    filename = request.GET.get('filename', 'test')
    try:
        fileobj = SplitFile.objects.get(name=filename)
        file1 = '/files/first_'+filename
        file2 = '/files/second_'+filename
        client.client_send(fileobj.node1, fileobj.port1, file1)
        client.client_send(fileobj.node2, fileobj.port2, file2)
        filenames = [file1, file2]
        with open('/files/'+filename, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

        for fname in filenames:
            os.remove(fname)

        added_files, removed_files = syncdb.sync_files()
        return render(request, 'sync_results.html', {'added_files': added_files,
                                                     'removed_files': removed_files})
    except:
        return HttpResponse('No such file')


def download_file_tcp(request):
    """
    Deprecated method for downloading files through
    tcp socket connection. File that is searched for on
    neighboring node is running a tcp socket server,
    and when file is clicked on in /search_results,
    this method kicks off client connection to that server.
    Handshake is established, then client sends filename to
    server, and server sends back the filedata and filename.
    :param request: wsgi request
    :return: redirect back to search results
    """
    added_files, removed_files = file_methods.download_single_file(request)
    return render(request, 'sync_results.html', {'added_files': added_files,
                                                 'removed_files': removed_files})


def sync_files(request):
    """
    Method to manually sync any files to the database.
    Can add files to /files/ directory and hit sync and
    it will update database. Can also remove files from
    directory and sync will update it.
    :param request: wsgi request
    :return: render sync results page with files added and removed
    """
    added_files, removed_files = syncdb.sync_files()
    return render(request, 'sync_results.html', {'added_files': added_files,
                                                 'removed_files': removed_files})


def download_file(request):
    """
    Deprecated API method to download file directly
    from page
    :param request: wsgi request
    :return: response with file
    """
    response = file_methods.download_file_http(request)
    return response


def filelist_api(request):
    """
    Search API for nodes that are getting queried for search.
    Continues the depth first traversal of all neighboring
    nodes until the maximum hop limit has been reached.
    :param request:
    :return:
    """
    json_response = search_methods.http_dfs_api(request)
    return HttpResponse(json.dumps(json_response))


@csrf_exempt
def upload_file(request):
    """
    Api method to allow for uploading files to the
    system through the upload page
    :param request: wsgi request
    :return: OK response
    """
    file_methods.upload_file(request)
    return HttpResponse("file uploaded")

