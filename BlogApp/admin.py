from django.contrib import admin
from BlogApp.models import UserProfile, BlogPost, PostDraft, Comment

admin.site.register(UserProfile)
admin.site.register(BlogPost)
admin.site.register(PostDraft)
admin.site.register(Comment)