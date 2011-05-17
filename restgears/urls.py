from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'restgears.views.home', name='home'),
    url(r'^news/', include('news.urls'), name='news'),
    url(r'^gallery/', include('gallery.urls'), name='gallery'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
                       
    (r'^$', direct_to_template, {'template': 'news/index.html'}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
