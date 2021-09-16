from docstore.maps import dtypes
from typing import FrozenSet

from docstore.models import Folder, Topic, Document
from docstore.maps import model_maps

def get_model_attrs(model):
    ''' Returns list of fields for a given model '''
    return [field.name for field in model._meta.get_fields()]

def clean_options(options, model):
    ''' Cleans up options used for initializing model '''
    # Get list of valid attrs for model
    attrs = get_model_attrs(model)

    # Extract special cases
    options = options.copy()
    special_cases = ['topics', 'key', 'folder']
    special_values = {k : options.get(k) for k in special_cases}

    # Remove any invalid or special case attributes
    option_keys = list(options.keys())
    for opt in option_keys:
        if (opt not in attrs) or (opt in special_values):
            del options[opt]

    # Set folder object if a match exists
    folder = special_values.get('folder')
    if folder is not None:
        folder = find_existing(Folder, folder)
        if folder is not None and 'folder_key' in attrs:
            options['folder_key'] = folder

    return options, special_values

def find_existing(model, key):
    ''' Attempts to find an existing object with the given
        key for the given model
    '''
    existing_obj = None
    if key is not None:
        objs = model.objects.all().filter(pk=key)
        if len(objs) > 0:
            existing_obj = objs[0]
    return existing_obj

def check_exists(model, obj, special_values):
    '''
        Checks if an object with attributes equal
        to 'obj' already exists

        Returns
            1 - Match exists and has the same attributes
            0 - Match exists but attrs are different
            -1 - No match exists
    '''
    # Get primary key and search for a match
    key_name = model._meta.pk.name
    name = special_values.get(key_name)
    existing_obj = find_existing(model, name)

    # Check if existing object has same attrs
    if existing_obj:
        return int(existing_obj.to_dict() == obj.to_dict)
    return -1
    
def create_object(model, options, interm_func=None):
    ''' Creates an object of type model with given attrs '''
    # Clean up options and initialize object
    options, special_values = clean_options(options, model)
    obj = model(**options)
    
    # Check if there isn't a conflicting existing object
    if check_exists(model, obj, special_values) != -1:
        return None

    # Attempt to validate object
    try:
        obj.clean()
        obj.save()
    except:
        return None

    # Set additional options that could not be initialized
    if interm_func:
        res = interm_func(obj, options, special_values)

        # Delete if additional options could not be set
        if res == False:
            obj.delete()
            return None

    return obj

def set_topics(obj, options, special_values):
    ''' Sets the topics list for a given object
    
        Returns True if all topics are valid
    '''
    # Check if there are any topics that can be created
    topic_infos = special_values.get('topics')
    if topic_infos is None or len(topic_infos) == 0:
        return True

    # Create new topics for each topic dict
    new_topics = []
    for t in topic_infos:
        # Create a new topic
        topic_obj = create_topic(t)
        new_topics.append(topic_obj)

        # Return False if a topic could not be created
        if topic_obj is None:
            return False

    # Clear previous topics list for object
    topics = obj.topics.all()
    for t in topics:
        obj.topics.remove(t)

    # Add in new topics list for object
    for topic in new_topics:
        obj.topics.add(topic)

    return True

def update_attrs(model, obj, options):
    ''' Updates attributes for a given object '''
    # Clean up attributes before setting them on object
    options, special_values = clean_options(options, model)
    for attr in options:
        setattr(obj, attr, options[attr])

    # Set topics for object if given
    val = set_topics(obj, options, special_values)
    if not val:
        return None

    # Return original object if successful
    return obj

def update_object(model, options):
    ''' Looks for and attempts to update attributes
        for an existing object
    '''
    # Look for object with given key
    key = options.get('key')
    obj = find_existing(model, key)
    if obj is None:
        return None

    # Set attributes for object and save
    res = update_attrs(model, obj, options)
    obj.save()

    return res

def create_topic(options):
    ''' Creates a topic'''
    return create_object(Topic, options)

def create_item(dtype, options):
    if dtype == 'topic':
        return create_topic(options)
    else:
        return create_object(model_maps[dtype], options, set_topics)

def update_item(dtype, options):
    ''' Updates attributes for a given item '''
    # Make sure that key is given
    key = options.get('key')
    if key is None:
        return None

    # Check that not trying to change key for object
    model = model_maps[dtype]
    key_name = model._meta.pk.name
    if key_name in options and options[key_name] != key:
        return None

    # Update other attributes
    if dtype == 'topic':
        return create_topic(options)
    else:
        return update_object(model_maps[dtype], options)

def delete_item(dtype, options):
    ''' Attemps to find and delete object of given data type with 
        given key and returns True if a match is found
    '''
    # Check if an existing object with key exists
    key = options.get('key')
    model = model_maps[dtype]
    obj = find_existing(model, key)
    found = (obj is not None)

    # Delete object if one is found
    if obj is not None:
        obj.delete()
    return found
