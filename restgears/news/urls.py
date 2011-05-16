from django.conf.urls.defaults import *
from django.views.generic import list_detail
from news.models import Entry
from news.handlers import EntryHandler
from base import views as baseviews
from piston.resource import Resource

news_info = {
        "queryset" : Entry.objects.all(),
}

entry_handler = Resource(EntryHandler)


urlpatterns = patterns ('',
                        (r'^$', list_detail.object_list, news_info, 'news-index'),
                        url(r'^api$', entry_handler, { 'emitter_format': 'json' }),
)
