from django.db import models
from django.contrib.auth.models import User

def user_unicode_edit(self):
    return '%s %s' % (self.first_name, self.last_name)

def user_save_edit(self, *args, **kwargs):
	#do something
	super(User, self).save(*args, **kwargs)

User.__unicode__ = user_unicode_edit
User.save = user_save_edit

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	post_count = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s' % self.user

class BlogPost(models.Model):
	user = models.ForeignKey(User, null=False)
	title = models.CharField(max_length=200, null=False)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField(null=False)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s by %s' % (self.title, self.user)

class PostDraft(models.Model):
	user = models.ForeignKey(User, null=False)
	post = models.ForeignKey(BlogPost)
	title = models.CharField(max_length=200, null=False)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField(null=False)
	published = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s by %s - [Draft date: %s]' % (self.title, self.post.user, self.created)

	def save(self, *args, **kwargs):
		if self.pk is None:
			if hasattr(self, 'post'):
				super(PostDraft, self).save(*args, **kwargs) # Call the "real" save() method.
			else:
				new_post = BlogPost(user=self.user, title=self.title, body=self.body)
				new_post.save()
				self.post = new_post
				super(PostDraft, self).save(*args, **kwargs) # Call the "real" save() method.
		else:
			return 'You are not allowed to overwrite a draft. Please create a new one'

	def publish(self):
		post = self.post
		post.title = self.title
		post.body = self.body
		self.published = True
		post.save()
		return 'Draft has been succesfully published as %s' % (post.title)

class Comment(models.Model):
	user = models.ForeignKey(User, null=False)
	body = models.TextField(null=False)
	post = models.ForeignKey(BlogPost, null=False)
	reply_for = models.ForeignKey('self', null=True, related_name='comment_reply')
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		if(self.reply_for):
			return 'Reply to comment #%s on post " %s "' % (self.reply_for.pk, self.post)
		else:
			return 'Comment #%s on post " %s "' % (self.pk, self.post.title)

