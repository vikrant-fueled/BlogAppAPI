from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization



class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		excludes = ['email', 'is_staff', 'is_superuser', 'password']
		
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()

		def obj_create(self, bundle, request=None, **kwargs):
			username, password = bundle.data['username'], bundle.data['password']
    		try:
        		bundle.obj = User.objects.create_user(username, '', password)
    		except IntegrityError:
        		raise BadRequest('That username already exists')
    		return bundle