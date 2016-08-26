from django.shortcuts import render
import json
from django.http import HttpResponse

# Create your views here.


def index(request):
    
    return render(request, 'index.html')


def filelist_api(request):
    filelist = {'files': ['test2.txt', 'test.txt', 'test3.txt']}
    return HttpResponse(json.dumps(filelist))