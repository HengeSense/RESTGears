from django.contrib import admin
from restgears.gallery.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Photo, PhotoAdmin)
