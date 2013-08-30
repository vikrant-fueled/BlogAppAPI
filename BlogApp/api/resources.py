from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie import fields

from BlogApp.models import *

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		excludes = ['email', 'is_staff', 'is_superuser', 'password']
		filtering = {
	      'username': ALL,
	    }

class BlogPostResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	comments = fields.ToManyField('BlogApp.api.resources.CommentResource', 'comment_set', related_name='comment', full=True)

	class Meta:
		queryset = BlogPost.objects.all()
		authorization= Authorization()
		filtering = {
	      'user': ALL_WITH_RELATIONS,
	      'title': ALL_WITH_RELATIONS,
	      'id': ALL_WITH_RELATIONS,
	    }

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	post = fields.ForeignKey(BlogPostResource, 'post')
	reply_to = fields.ForeignKey('self', 'reply_for', null=True)
	replies = fields.ToManyField('self', 'comment_reply', null=True)

	class Meta:
		queryset = Comment.objects.filter()
		authorization= Authorization()
		filtering = {
	      'user': ALL_WITH_RELATIONS,
	      'post': ALL_WITH_RELATIONS,
	    }