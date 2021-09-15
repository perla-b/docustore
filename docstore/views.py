from django.http import response
from django.http.response import HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.http import HttpResponse, FileResponse
from docstore import model_search

import zipfile
import tempfile

import json
import os

datatypes = ['folder', 'doc', 'topic']

def search(request):
    items = []
    dtype = None
    if request.GET:
        options = request.GET
        dtype = options.get('data_type')
        if dtype == 'folders':
            items = model_search.find_folders(options)
        elif dtype == 'docs':
            items = model_search.find_docs(options)
        elif dtype == 'topics':
            items = model_search.find_topics(options)
    return (items, dtype)

def list(request):
    # Get host URL
    url = request.get_host()

    # Find items matching request and map to JSON string
    items, dtype = search(request)
    dicts = [item.to_dict(url) for item in items]
    data = json.dumps(dicts, indent=4)
    return HttpResponse(data, content_type='json')

def create(request):
    pass

def update(request):
    pass