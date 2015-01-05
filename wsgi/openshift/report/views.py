from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader

# Create your views here.

def is_md5(value):

    if len(value) != 32:
        return False

    for i in "0123456789abcdef":
      value = value.replace(i, "")
    return (len(value) == 0)

def index(request):
    return render(request, 'index.html')

def host(request, md5):
    if md5 is None:
        return render(request, 'host_list.html')
    if is_md5(md5):
        context={'host':md5}
        return render(request, 'host.html', context)
    else:
        return HttpResponseBadRequest("'%s' is not consistent with md5" % md5)

def user(request, md5):
    if md5 is None:
        return render(request, 'user_list.html')
    if is_md5(md5):
        context={'uid':md5}
        return render(request, 'user.html', context)
    else:
        return HttpResponseBadRequest("'%s' is not consistent with md5" % md5)
