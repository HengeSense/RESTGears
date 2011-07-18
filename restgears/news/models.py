from django.db import models
from django.conf import settings
from base.utils import reverse

from base.models import BaseModel
from news.views import download_handler

class Entry(BaseModel):
    teaser = models.TextField(max_length=500, help_text='This text is displayed in the news overview list a well as in top of every news entry (Text only)');
    content = models.TextField(max_length=4000, help_text='This text is the main content for the news entry (supports HTML).');
    class Meta:
        verbose_name_plural = 'News Entries';
        ordering = ['-publish_on','-created_on']
  
class Image(models.Model):
    description = models.TextField(max_length=500, help_text='Will be displayed under the image', blank=True);
    newsentry = models.ForeignKey(Entry, related_name='images');
    image = models.ImageField(upload_to='uploads/news', help_text='Select an image that is already resized for the iphone');
    orderindex = models.IntegerField(default=100, help_text='Image will be ordererd according to its Order Index')
    
    def get_absolute_url(self):
        return reverse('news-image', kwargs={'pk':self.pk,}) 
    url = property(get_absolute_url)

    def preview_image(self):
        return u'<img src="%s" alt="%s" height="100"/>'%(self.url, self.description)
    
    preview_image.allow_tags = True

    class Meta:
        verbose_name_plural = 'News Images';
        ordering = ['orderindex',]
