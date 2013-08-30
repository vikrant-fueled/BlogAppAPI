from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from BlogApp.api.resources import *

admin.autodiscover()

api_v1 = Api(api_name='v1')
api_v1.register(UserResource())
api_v1.register(BlogPostResource())
api_v1.register(CommentResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_v1.urls)),
)
