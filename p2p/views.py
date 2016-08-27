from django.shortcuts import render
import json
from django.http import HttpResponse
import requests
from models import File, Neighbors
from wsgiref.util import FileWrapper
import tarfile


# Create your views here.


def index(request):
    ip_adds = ['192.168.181.131:8000', '192.168.181.131:8001', '192.168.181.131:8002']
    aggregate_list = {}
    for ip in ip_adds:
        response = requests.get('http://{0}/api/v1/filelist'.format(ip))
        filelist = json.loads(response.text)['files']
        aggregate_list[ip] = filelist

    return render(request, 'index.html', {'files': aggregate_list})


def filelist_api(request):
    filelist = File.objects.all()
    html = ''
    for file in filelist:
        html += file.__str__()
    return HttpResponse(html)


def download_file(request):
    filename = request.GET.get('filename')
    files = File.objects.filter(name=filename)
    print files
    if files:
        default = files[0]
        response = HttpResponse(content_type='application/x-gzip')
        print response
        response['Content-Disposition'] = 'attachment; filename=myfile.tar.gz'
        tarred = tarfile.open(fileobj=response, mode='w:gz')
        tarred.add(default.location)
        tarred.close()
        return response
        # return
    else:
        return HttpResponse('no')


    # html = 'successful'
    # response = HttpResponse(html, content_type='text/plain')
    # response['Content-Disposition'] = 'attachment; filename="test.txt"'
    # return response
