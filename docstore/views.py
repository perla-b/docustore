from django.http import response
from django.http.response import HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.db.models import QuerySet
from docstore.models import Folder, Document, Topic
from django.core import serializers
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

def write_files_to_zip(zfile, files, dirname=''):
    ''' Writes Document files to given zipfile under given directory'''
    for f in files:
        local_path = f.file.path
        zip_path = os.path.join(dirname, f.file.name)
        zfile.write(local_path, arcname=zip_path)

def create_zipfile():
    fd = tempfile.TemporaryFile(mode='w+b')
    zfile = zipfile.ZipFile(fd, mode='w')
    return fd, zfile

def create_zip_response(fd, zfile):
    # Close zip file and reset buffer's position
    zfile.close()
    fd.seek(0)

    # Create HTTP response with zip file as attachment
    response = HttpResponse(fd)
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment; filename=download.zip'
    return response

def write_folders(items):
    # Create zip file and temporary buffer
    fd, zfile = create_zipfile()

    # Write documents in each folder
    for folder in items:
        name = folder.name
        docs = folder.get_documents()
        write_files_to_zip(zfile, docs, dirname=name)

    return create_zip_response(fd, zfile)

def write_documents(items):
    # Create zip file and temporary buffer
    fd, zfile = create_zipfile()

    # Write files to top level of archive
    write_files_to_zip(zfile, items)

    return create_zip_response(fd, zfile)

def list(request):
    # Get host URL
    url = request.get_host()

    # Find items matching request and map to JSON string
    items, dtype = search(request)
    dicts = [item.to_dict(url) for item in items]
    data = json.dumps(dicts, indent=4)
    return HttpResponse(data, content_type='json')

def download(request):
    items, dtype = search(request)

    if dtype is None or len(items) == 0:
        return HttpResponse('No matching data', status=204)

    if dtype == 'folders':
        response = write_folders(items)
    elif dtype == 'docs':
        response = write_documents(items)
    else:
        response = HttpResponseBadRequest()

    return response

def create(request):
    pass

def update(request):
    pass