from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from BlogApp.models import *

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		excludes = ['email', 'is_staff', 'is_superuser', 'password']

class BlogPostResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = BlogPost.objects.all()
		authorization= Authorization()

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	post = fields.ForeignKey(BlogPostResource, 'post')

	class Meta:
		queryset = Comment.objects.all()
		authorization= Authorization()