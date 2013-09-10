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
	list_allowed_methods = ['get']
	detail_allowed_methods = ['get']
	resource_name = 'blogpost'
	comments = fields.ToManyField('BlogApp.api.resources.CommentResource', 'comment_set', related_name='comment', full=True, null=True)
	tags = fields.ToManyField('BlogApp.api.resources.TagResource', 'tags', related_name='tag', null=True)

	class Meta:
		queryset = BlogPost.objects.all()
		authorization= Authorization()
		filtering = {
	      'user': ALL_WITH_RELATIONS,
	      'title': ALL_WITH_RELATIONS,
	      'id': ALL_WITH_RELATIONS,
	      'tag': ALL_WITH_RELATIONS,
	    }

	def dehydrate(self, bundle):
	 	bundle.data['user'] = bundle.obj.user
	 	bundle.data['tags'] = []
	 	for tag in bundle.obj.tags.all():
	 		bundle.data['tags'].append(tag.name)
	 	return bundle

class PostDraftResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = PostDraft.objects.all()
		authorization= Authorization()
		filtering = {
	      'user': ALL_WITH_RELATIONS,
	      'title': ALL_WITH_RELATIONS,
	      'id': ALL_WITH_RELATIONS,
	      'tags': ALL_WITH_RELATIONS,
	      'published': ALL_WITH_RELATIONS,
	      'post': ALL_WITH_RELATIONS
	    }

class CommentResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	post = fields.ForeignKey(BlogPostResource, 'post')
	reply_to = fields.ForeignKey('self', 'reply_for', null=True)
	replies = fields.ToManyField('self', 'comment_reply', null=True, full=True)

	class Meta:
		queryset = Comment.objects.filter()
		authorization= Authorization()
		filtering = {
	      'user': ALL_WITH_RELATIONS,
	      'post': ALL_WITH_RELATIONS,
	    }

class TagResource(ModelResource):
	class Meta(object):
		queryset = Tag.objects.all()
		authorization= Authorization()
		filtering = {
			'name': ALL,
		}
