from django.shortcuts import render
import json
from django.http import HttpResponse
import requests
from models import File, Neighbors

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
    html = 'successful'
    response = HttpResponse(html, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="test.txt"'
    return response