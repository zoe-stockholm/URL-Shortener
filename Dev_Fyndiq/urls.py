from django.conf.urls import patterns, include, url
from django.contrib import admin
from shortener import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shorten_url/$', views.shorten_url),
    url(r'^(?P<key>\w+)/$', views.redirect),
)
