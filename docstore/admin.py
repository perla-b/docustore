from django.contrib import admin

from docstore.models import Folder, Document, Topic

class FolderAdmin(admin.ModelAdmin):
    fields = ['name','topics']

class DocumentAdmin(admin.ModelAdmin):
    fields = ['name', 'file', 'folder_key', 'topics']

class TopicAdmin(admin.ModelAdmin):
    fields = ['name', 'long_name']

admin.site.register(Folder, FolderAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Topic, TopicAdmin)