from django.db import models
from django.contrib.auth.models import User

def user_unicode_edit(self):
    return '%s %s' % (self.first_name, self.last_name)

def user_save_edit(self, *args, **kwargs):
	self.set_password(self.password)
	super(User, self).save(*args, **kwargs)

User.__unicode__ = user_unicode_edit
User.save = user_save_edit

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	post_count = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s' % self.user

class BlogPost(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=200, null=False)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField(null=False)
	published = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s by %s [ Published? : %s ]' % (self.title, self.user, self.published)

class BlogDraft(models.Model):
	user = models.ForeignKey(User, null=False)
	post = models.ForeignKey(BlogPost)
	title = models.CharField(max_length=200, null=False)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField(null=False)

	def __unicode__(self):
		return '%s by %s - [Draft date: %s]' % (self.title, self.post.user, self.created)

	def save(self, *args, **kwargs):
		if hasattr(self, 'post'):
			super(BlogDraft, self).save(*args, **kwargs) # Call the "real" save() method.
		else:
			new_post = BlogPost(user=self.user, title=self.title, body=self.body, published=False)
			new_post.save()
			self.post = new_post
			super(BlogDraft, self).save(*args, **kwargs) # Call the "real" save() method.

class Comment(models.Model):
	user = models.ForeignKey(User, null=False)
	body = models.TextField(null=False)
	post = models.ForeignKey(BlogPost, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Comment #%s on post " %s "' % (self.pk, self.post.title)

class Reply(models.Model):
	user = models.ForeignKey(User, null=False)
	body = models.TextField(null=False)
	comment = models.ForeignKey(Comment, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Reply #%s on comment #%s' % (self.pk, self.comment.pk)

