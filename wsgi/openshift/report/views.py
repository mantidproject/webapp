from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader

# Create your views here.


def index(request):
    return render(request, 'index.html')


def host(request, md5):
    if md5 is None:
        return render(request, 'host_list.html')
    else:
        context = {'host': md5}
        return render(request, 'host.html', context)


def user(request, md5):
    if md5 is None:
        return render(request, 'user_list.html')
    else:
        context = {'uid': md5}
        return render(request, 'user.html', context)
