from django.conf.urls.defaults import *
from django.views.generic import list_detail
from gallery.views import GalleryOverviewView,  GalleryListView, PhotoVoteView,PhotoView, download_handler, PhotoDeleteView, PhotoUploadView
from gallery.models import Gallery, Photo
from djangorestframework.mixins import ListModelMixin
from djangorestframework.resources import ModelResource
from djangorestframework.views import View, ListModelView, InstanceModelView
from django.forms import ModelForm

class GalleryIndexResource(ModelResource):
    model = Gallery
    fields = ('id','name', 'url' )
    def url(self, instance):
        return instance.url

class GalleryListResource(ModelResource):
    model = Gallery
    fields = ('id','name', 'created_on', 'upload_url',  ('photos',('id','uploaded_on',('user',('username',)), 'image_url', 'votes','url')),)


class PhotoUploadForm(ModelForm):
    class Meta:
        fields = ('image',)
        model = Photo

class PhotoResource(ModelResource):
    model = Photo
    form = PhotoUploadForm
    include = ()
    base_fields = ('id','uploaded_on',('user',('username',)), 'image_url', 'votes',)
    vote_field = ('vote_url',)
    delete_field = ('delete_url',)
    def url(self, instance):
        if hasattr(instance, 'url'):
            return instance.url


urlpatterns = patterns ('',
    url(r'^$', GalleryOverviewView.as_view(), name ='gallery-overview'),
    url(r'^index$', ListModelView.as_view(resource=GalleryIndexResource), name='gallery-index'),
    url(r'^(?P<pk>\w+)$', GalleryListView.as_view(resource=GalleryListResource), name='gallery-instance'),
    url(r'^upload-(?P<pk>\w+)$', PhotoUploadView.as_view(resource=PhotoResource), name='photo-upload'),
    url(r'^upload-(?P<pk>\w+)-(?P<user_id>\w+)$', PhotoUploadView.as_view(resource=PhotoResource), name='photo-upload-user'),
    url(r'^photo-(?P<pk>\w+)$', PhotoView.as_view(resource=PhotoResource), name='photo-instance'),
    url(r'^vote-(?P<pk>\w+)$', PhotoVoteView.as_view(resource=PhotoResource), name='photo-vote'),
    url(r'^delete-(?P<pk>\w+)$', PhotoDeleteView.as_view(resource=PhotoResource), name='photo-delete'),
    url(r'^image/(?P<pk>\w+)$', download_handler, name='gallery-image'),
)
