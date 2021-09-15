from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from docstore.models import Folder, Document, Topic
from django.core import serializers
from docstore import model_search

datatypes = ['folder', 'doc', 'topic']
    
def search(request):
    items = []
    if request.GET:
        options = request.GET
        dtype = options.get('data_type')
        if dtype == 'folders':
            items = model_search.find_folders(options)
        elif dtype == 'docs':
            items = model_search.find_docs(options)
        elif dtype == 'topics':
            items = model_search.find_topics(options)
    return items

def serialize(items):
    data = serializers.serialize('xml', items, fields=('name','size'))

def list(request):
    items = search(request)
    return HttpResponse(str([e.name for e in items]))

def download(request):
    pass


def update(request):
    pass