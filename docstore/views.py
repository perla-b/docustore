from django.core.exceptions import BadRequest
from requests.api import options
from django.http.response import Http404, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.http import HttpResponse, FileResponse
from docstore import model_search

import json
import docstore_create
from docstore.maps import dtypes

search_func_map = {
    'folders' : model_search.find_folders,
    'docs' : model_search.find_docs,
    'topics' : model_search.find_topics,
}

def search(request):
    '''
        Helper function for list_view finds
        items from query
    '''
    items = []
    dtype = None
    if request.GET:
        options = {k : request.GET[k].strip('"') for k in request.GET}
        dtype = options.get('data_type')
        if dtypes.contains(dtype):
            items = search_func_map[dtype](options)
    return items

def list_view(request):
    ''' Lists data objects from a query '''
    # Get host URL
    url = request.get_host()

    # Find items matching request and map to JSON string
    items = search(request)
    dicts = [item.to_dict(url) for item in items]
    data = json.dumps(dicts, indent=4)

    return HttpResponse(data, content_type='json')

def extract_request_info(request):
    # Get host URL and load object info
    url = request.get_host()
    opts = json.loads(request.body)
    dtype = opts.get('data_type')
    return url, opts, dtype

def format_response(obj, url, error_msg=None):
    ''' 
        Formats JSON-type response if model object is found
    '''
    if obj is not None:
        data = json.dumps(obj.to_dict(url), indent=4)
        response = HttpResponse(data, content_type='json')
    else:
        response = HttpResponseBadRequest(error_msg)
    return response

def create(request):
    ''' Lists data objects from a query '''
    if request.method == 'POST':
        # Load request info
        url, opts, dtype = extract_request_info(request)

        # Try to create object w/ given attrs
        obj = None
        if dtypes.contains(dtype):
            obj = docstore_create.create_item(dtype, opts)
        return format_response(obj, url)
    else:
        return HttpResponseBadRequest()

def update(request):
    if request.method == 'PUT':
        # Load request information
        url, opts, dtype = extract_request_info(request)

        # Try to find object that matches request and update it
        obj = None
        if dtypes.contains(dtype):
            obj = docstore_create.update_item(dtype, opts)

        # 404 if no object is updated
        if obj is None:
            return Http404()
        return format_response(obj, url)
    else:
        return HttpResponseBadRequest()

def delete(request):
    if request.method == 'DELETE':
        # Extract request info
        url, opts, dtype = extract_request_info(request)

        if dtypes.contains(dtype):
            # Try to find and delete object
            found = docstore_create.delete_item(dtype, opts)

            # 404 if no object is found
            if not found:
                return Http404()
            else:
                return HttpResponse('Succesfully deleted.')
    else:
        return HttpResponseBadRequest()