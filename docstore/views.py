from django.http.response import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from docstore.models import Folder, Document, Topic
from django.core import serializers

datatypes = ['folder', 'doc', 'topic']

def filter_by_topics(items, attrs):
    if 'topics' in attrs:
        topics = attrs['topics'].strip('"').split(',') # Remove spaces?
        items = items.filter(topics__in=topics)
    return items

def filter_by_name(items, attrs):
    if 'name' in attrs:
        items = items.filter(name=attrs['name'].strip('"'))
    return items

def find_folder_by_name(attrs):
    folder_name = attrs['folder']
    folder_matches = find_folders({'name' : folder_name})
    return folder_matches

def find_folders(attrs):
    items = Folder.objects.all()
    items = filter_by_topics(items, attrs)
    items = filter_by_name(items, attrs)
    return items

def find_docs(attrs):
    items = Document.objects.all()

    if 'folder' in attrs:
        folders = find_folder_by_name(attrs)
        if len(folders) == 0:
            return QuerySet({})
        else:
            folder = folders[0]
            items = items.filter(folder_key=folder.pk)

    items = filter_by_name(items, attrs)
    items = filter_by_topics(items, attrs)

def find_topics(attrs):
    if 'folder' in attrs:
        folders = find_folder_by_name(attrs)
        if len(folders) == 0:
            return QuerySet({})
        else:
            folder = folders[0]
            items = folder.topics.objects.all()
    else:
        items = Topic.objects.all()

    items = filter_by_name(items, attrs)

    if 'desc' in attrs:
        items = items.filter(long_name__contains=attrs['desc'])
    return items
    
def search(request):
    items = []
    if request.GET:
        options = request.GET
        dtype = options.get('data_type')
        if dtype == 'folders':
            items = find_folders(options)
        elif dtype == 'docs':
            items = find_docs(options)
        elif dtype == 'topics':
            items = find_topics(options)
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