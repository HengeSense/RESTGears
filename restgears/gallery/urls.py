from django.conf.urls.defaults import *
from django.views.generic import list_detail
from gallery.views import GalleryOverviewView,  GalleryListView, PostPhotoUploadView, PhotoVoteView,PhotoView,  PhotoUploadView, PhotoListView, PhotoUpdateRanks
from gallery.models import Gallery, Photo
from djangorestframework.mixins import ListModelMixin
#from djangorestframework.resources import ModelResource
from base.resources import AuthModelResource
from djangorestframework.views import View, ListModelView, InstanceModelView
from django.forms import ModelForm
from base.utils import reverse
from django.views.decorators.cache import cache_page, never_cache
from base.views import ImageServeView


class GalleryResource(AuthModelResource):
    model = Gallery
    fields = ('id','name', 
              'created_on', 
              'upload_url',
              'photos_url',
              'photos_by_views_url',
              'photos_by_votes_url',
              'photos_by_uploaded_url',
              'my_photos_url',
              'my_photos_by_views_url',
              'my_photos_by_votes_url',
              'my_photos_by_uploaded_url',
              )
    
    def upload_url(self, instance):
        return reverse('photo-upload', kwargs={'pk':instance.pk,})
    def photos_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'ordering':'votes'})
    def photos_by_views_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'ordering':'views'})
    def photos_by_votes_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'ordering':'votes'})
    def photos_by_uploaded_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,})
    def my_photos_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'user':'me'})
    def my_photos_by_views_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'user':'me', 'ordering':'views'})
    def my_photos_by_votes_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'user':'me', 'ordering':'votes'})
    def my_photos_by_uploaded_url(self, instance):
        return reverse('photo-list', kwargs={'gallery':instance.pk,'user':'me'})        

class PhotoUploadForm(ModelForm):
    class Meta:
        fields = ('image',)
        model = Photo

class PhotoResource(AuthModelResource):
    model = Photo
    form = PhotoUploadForm
    include = ()
    fields = ('id','uploaded_on','views','nickname','user_id','image_url','rank', 'thumb_image_url','votes','delete_url','vote_url','gallery_url','can_vote', 'can_delete', 'url', 'lastvote_on')
    def can_delete(self, instance):
        return instance.can_delete(self.current_user)

    def can_vote(self, instance):
        return instance.can_vote(self.current_user)
    
    def delete_url(self, instance):
        return reverse('photo-instance', kwargs={'pk':instance.pk,})

    def vote_url(self, instance):
        return reverse('photo-vote', kwargs={'pk':instance.pk,})
    
    def image_url(self, instance):
        return reverse('serve-photo', kwargs={'pk':instance.pk,})

    def gallery_url(self, instance):
        return reverse('gallery-instance', kwargs={'pk':instance.gallery_id,})

    def url(self, instance):
        return reverse('photo-instance', kwargs={'pk':instance.pk,}) 

urlpatterns = patterns ('',
    #url(r'^$', GalleryOverviewView.as_view(), name ='gallery-overview'),
    url(r'^$', ListModelView.as_view(resource=GalleryResource), name='gallery-index'),
    #url(r'^uploads$', PhotoListView.as_view(resource=PhotoResource), name='photos-current-user'),
    url(r'^(?P<gallery>\w+)/photos$', never_cache(PhotoListView.as_view(resource=PhotoResource)), name='photo-list'),
    url(r'^(?P<gallery>\w+)/photos-by-(?P<ordering>\w+)$', never_cache(PhotoListView.as_view(resource=PhotoResource)), name='photo-list'),
    url(r'^(?P<gallery>\w+)/photos-by-(?P<ordering>\w+)/(?P<user>\w+)$', never_cache(PhotoListView.as_view(resource=PhotoResource)), name='photo-list'),
    url(r'^(?P<gallery>\w+)/photos/(?P<user>\w+)$', never_cache(PhotoListView.as_view(resource=PhotoResource)), name='photo-list'),
    url(r'^(?P<pk>\w+)$', GalleryListView.as_view(resource=GalleryResource), name='gallery-instance'),

    #upload urls
    url(r'^(?P<pk>\w+)/upload$', never_cache(PhotoUploadView.as_view()), name='photo-upload'),
    url(r'^(?P<pk>\w+)/(?P<user_id>\w+)/postupload$', never_cache(PostPhotoUploadView.as_view(resource=PhotoResource)), name='photo-upload-user'),

    #photo
    url(r'^photo/(?P<pk>\w+)$', never_cache(PhotoView.as_view(resource=PhotoResource)), name='photo-instance'),

    #actions
    url(r'^vote/(?P<pk>\w+)$', never_cache(PhotoVoteView.as_view(resource=PhotoResource)), name='photo-vote'),
    #url(r'^delete-(?P<pk>\w+)$', PhotoDeleteView.as_view(resource=PhotoResource), name='photo-delete'),

    #serving
    url(r'^image/(?P<pk>\w+)$', ImageServeView.as_view(container=Photo, image_field='image_url'), name='serve-photo'),
    #url(r'^image/(?P<pk>\w+)$', ImageServeView.as_view(container=Photo), name='serve-photo'),
)
