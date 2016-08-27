from django.shortcuts import render
import json
from django.http import HttpResponse
import requests
from models import File

# Create your views here.


def index(request):
    ip_adds = [ '192.168.181.131:8001', '192.168.181.131:8002']
    aggregate_list = {}
    for ip in ip_adds:
        response = requests.get('http://{0}/api/v1/filelist'.format(ip))
        # filelist = json.loads(response.text)['files']
        aggregate_list[ip] = response.text
    file = request.get('192.168.181.131:8001')

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