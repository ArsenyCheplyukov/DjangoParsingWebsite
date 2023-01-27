from django.contrib import admin
from .models import *

# class RequestDataAdmin(admin.ModelAdmin):
#     list_display = ('request_text', 'slug', 'time_create', 'is_published')
#     list_display_links = ('id', 'title')
#     search_fields = ('title', 'content')
#     list_editable = ('is_published',)
#     list_filter = ('is_published', 'time_create')
#     prepopulated_fields = {"slug": ("title",)}

# class ImageDataAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#     prepopulated_fields = {"slug": ("name",)}

# class ModelDataAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#     prepopulated_fields = {"slug": ("name",)}


# admin.site.register(RequestData, RequestDataAdmin)
# admin.site.register(ImageData, ImageDataAdmin)

admin.site.register(RequestData)
admin.site.register(ImageData)
admin.site.register(ModelData)
