from django.shortcuts import render
import json
from django.http import HttpResponse
import requests

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
    filelist = {'files': ['test2.txt', 'test.txt', 'test3.txt']}
    return HttpResponse(json.dumps(filelist))
