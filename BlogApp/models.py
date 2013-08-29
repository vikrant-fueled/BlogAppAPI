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


	
