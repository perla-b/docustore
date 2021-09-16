from django.db import models
from django.conf import settings
import urllib.parse
from django.core.exceptions import ValidationError

max_wlen = 200

class Topic(models.Model):
	name = models.CharField(max_length=max_wlen, primary_key=True)
	desc = models.CharField(max_length=max_wlen)
	
	def __str__(self):
		return self.name

	def to_dict(self, url=''):
		''' Returns dictionary representation of Topic '''
		values = {
			'key' : self.name,
			'desc' : self.desc
		}
		return values

class TaggableObject(models.Model):
	''' Base class for Folder and Document since both have topics lists'''
	topics = models.ManyToManyField(Topic)
	class Meta:
		abstract = True

	def get_topics_list(self):
		''' Returns the list of topics as dict objects '''
		topics = self.topics.all()
		return [topic.to_dict() for topic in topics]

class Folder(TaggableObject):
	name = models.CharField(max_length=max_wlen, primary_key=True)
	def __str__(self):
		return self.name

	def to_dict(self, url=''):
		''' Returns dictionary representation of Folder'''
		values = {}
		values['data_type'] = 'folder'
		values['name'] = self.name
		values['key'] = self.pk
		values['topics'] = self.get_topics_list()

		# Get list of documents corresponding to this folder
		docs = self.get_documents()
		values['items'] = [d.to_dict(url) for d in docs]

		return values

	def get_documents(self):
		''' Returns QuerySet of documents in this folder'''
		docs = Document.objects.all()
		docs = docs.filter(folder_key=self.pk)
		return docs

class Document(TaggableObject):
	name = models.CharField(max_length=max_wlen)
	file = models.FileField(settings.MEDIA_ROOT)
	folder_key = models.ForeignKey(Folder, on_delete=models.CASCADE)

	def __str__(self):
		return (self.name)

	def to_dict(self, url):
		''' Returns dictionary representation of Document'''
		values = {}
		values['data_type'] = 'doc'
		values['name'] = self.name
		values['filename'] = self.file.name
		values['key'] = self.pk
		values['folder'] = self.folder_key.name
		values['folder_key'] = self.folder_key.pk
		values['topics'] = self.get_topics_list()
		values['file_url'] = ''.join([url, self.file.url])

		return values
	
	def clean(self):
		name = self.name
		folder = self.folder_key
		dupl_files = Document.objects.all().filter(folder_key=folder, name=name)
		if len(dupl_files) > 0:
			if dupl_files[0] != self:
				raise ValidationError('Cannot have duplicate document names in same folder')
