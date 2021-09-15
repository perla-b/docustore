from django.db.models import QuerySet
from docstore.models import Folder, Document, Topic

def filter_by_topics(items, attrs):
    ''' Filters items QuerySet by topics if specified '''
    if 'topics' in attrs:
        topics = attrs['topics'].strip('"').split(',') # Remove spaces?
        items = items.filter(topics__in=topics)
    return items

def filter_by_name(items, attrs):
    ''' Filters items QuerySet by name if specified '''
    if 'name' in attrs:
        items = items.filter(name=attrs['name'].strip('"'))
    return items


def get_folder_by_name(attrs):
    ''' Returns folder with given name in attrs'''
    folder_name = attrs['folder']
    folder_matches = find_folders({'name' : folder_name})
    return folder_matches


def find_folders(attrs):
    ''' Returns folders with given attrs '''
    items = Folder.objects.all()
    items = filter_by_topics(items, attrs)
    items = filter_by_name(items, attrs)
    return items

def find_docs(attrs):
    ''' Returns documents with given attrs '''
    items = Document.objects.all()

    # Check if folder is specified, if so limit search to its documents
    if 'folder' in attrs:
        folders = get_folder_by_name(attrs)
        if len(folders) == 0:
            return QuerySet({})
        else:
            folder = folders[0]
            items = items.filter(folder_key=folder.pk)

    # Filter by name and list of topics
    items = filter_by_name(items, attrs)
    items = filter_by_topics(items, attrs)

def find_topics(attrs):
    ''' Returns topics with given attrs '''
    items = Topic.objects.all()

    # Search for name value in short form descriptors
    items = filter_by_name(items, attrs)

    # Search for desc substring in long form descriptors
    if 'desc' in attrs:
        items = items.filter(long_name__contains=attrs['desc'])
    return items
