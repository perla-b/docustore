from django.db import models

max_wlen = 200

class Topic(models.Model):
	name = models.CharField(max_length=max_wlen, primary_key=True)
	long_name = models.CharField(max_length=max_wlen)
	def to_tuple(self):
		return (self.name, self.long_name)
	
	def __str__(self):
		return self.name

class TaggableObject(models.Model):
	topics = models.ManyToManyField(Topic)
	class Meta:
		abstract = True

class Folder(TaggableObject):
	name = models.CharField(max_length=max_wlen)

	def __str__(self):
		return self.name

class Document(TaggableObject):
	name = models.CharField(max_length=max_wlen)
	file = models.FileField() # TODO: Set the location
	folder_key = models.ForeignKey(Folder, on_delete=models.SET_NULL, 
		null=True) # Is a folder necessary? 
	
	def __str__(self):
		return (self.name)