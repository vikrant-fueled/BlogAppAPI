from django.contrib import admin
from BlogApp.models import UserProfile, BlogPost, BlogDraft

admin.site.register(UserProfile)
admin.site.register(BlogPost)
admin.site.register(BlogDraft)