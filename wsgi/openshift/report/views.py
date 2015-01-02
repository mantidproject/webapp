from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

# Create your views here.

def is_md5(value):

    if len(value) != 32:
        return False

    for i in "0123456789abcdef":
      value = value.replace(i, "")
    return (len(value) == 0)

def index(request):
    return HttpResponse("Hello, world. You're at the report index.")

def host(request, md5):
    if is_md5(md5):
        return HttpResponse("Hello, world. You're at the host report.")
    else:
        return HttpResponseBadRequest("'%s' is not consistent with md5" % md5)

def uid(request, md5):
    if is_md5(md5):
        return HttpResponse("Hello, world. You're at the uid report.")
    else:
        return HttpResponseBadRequest("'%s' is not consistent with md5" % md5)
