from django.test import TestCase
from docstore.models import Folder, Topic, Document
from django.urls import reverse

class QueryTest(TestCase):
    def test(self):
        # Find all herb-related documents
        docs = Document.objects.all()
        herbs = docs.filter(topics__in=['herbs'])
        herb_keys = [herb.name for herb in herbs]
        assert(set(herb_keys) == set(['Basil', 'Oregano']))

        # Find all herb-related docs in the "Dry Goods" folder
        folders = Folder.objects.all()
        folder_name = 'Dry Goods'
        folder_key = folders.filter(name=folder_name)[0].pk
        folder_docs = docs.filter(folder_key=folder_key)
        herbs_in_folder = folder_docs.filter(topics__in=['herbs'])
        herb_keys = [herb.name for herb in herbs_in_folder]
        assert((set(herb_keys)) == set(['Oregano']))

        # Find all folders with legumes or herbs in tag
        legume_folders = folders.filter(topics__in=['legumes', 'herbs']).distinct()
        folder_keys = [folder.name for folder in legume_folders]
        assert (set(folder_keys) == set(['Dry Goods', 'Produce', 'Canned foods']))

        # Find all folders with meat in tag (None)
        starch_folders = folders.filter(topics__in=['mear'])
        assert (len(starch_folders) == 0)
