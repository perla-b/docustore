from django.db import models

max_wlen = 200

class Topic(models.Model):
	name = models.CharField(max_length=max_wlen, primary_key=True)
	long_name = models.CharField(max_length=max_wlen)

class TaggableObject(models.Model):
	class Meta:
		abstract = True

class Folder(TaggableObject):
	name = models.CharField(max_length=max_wlen)

class Document(TaggableObject):
	name = models.CharField(max_length=max_wlen)
	file = models.FileField() # TODO: Set the location
	folder_key = models.ForeignKey(Folder, 
		on_delete=models.SET_NULL,
		null=True) # Is a folder necessary? 
