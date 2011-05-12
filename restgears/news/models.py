from django.db import models
from datetime import datetime

class BaseModel(models.Model):
    name = models.CharField(max_length=200, help_text='Choose a name that describes this document')
    #type = models.CharField(max_length=100, blank=True, help_text='Use type to better distinguish between documents')
    slug = models.SlugField(max_length=50, db_index=True)
    publish_on = models.DateTimeField(blank=True, null=True, default=datetime.now)
    deleted_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category')

    def _is_published(self):
        return self.published_on < datetime.now()
    is_published = property(_is_published)

    def _is_deleted(self):
        return self.deleted_on < datetime.now()
    is_deleted = property(_is_deleted)

    def _is_active(self):
        return self.is_published() and not self.is_deleted()
    is_active = property(_is_active)

    def __unicode__(self):
        return self.name

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('documents.views.show', [str(self.id)])
    class Meta:
        abstract = True

class Entry(BaseModel):
    teaser = models.TextField(max_length=500, help_text='Insert text only');
    content = models.TextField(max_length=4000, help_text='Insert HTML here');

class Image(models.Model):
    description = models.TextField(max_length=500, help_text='Insert text only');
    newsentry = models.ForeignKey(Entry);
    image = models.FileField(upload_to='uploads/news');

class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Choose a name that describes this category', db_index=True, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(max_length=32, db_index=True)
    entry = models.ForeignKey(Entry, related_name='tags')

    def __unicode__(self):
        return self.name
