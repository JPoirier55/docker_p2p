from django.shortcuts import render
import json
from django.http import HttpResponse
import requests
from models import File, Neighbors
import tarfile

# Create your views here.


def index(request):
    neighbors = Neighbors.objects.all()
    aggregate_list = {}
    for neighbor in neighbors:
        response = requests.get('http://{0}:{1}/api/v1/filelist'.format(neighbor.ip_address, neighbor.port))
        # filelist = json.loads(response.text)['files']
        aggregate_list[neighbor.hostname] = response.text

    # file = request.get('192.168.181.131:8001')

    return render(request, 'index.html', {'files': aggregate_list})


def filelist_api(request):
    filelist = File.objects.all()
    html = ''
    for file in filelist:
        html += file.__str__() + '<br>'
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