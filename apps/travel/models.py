from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def validateReg(self, request):
        errors = []
        if len(request.POST['username']) < 1:
            errors.append('Username can not be empty')
        try:
            user = User.objects.get(username = request.POST['username'])
            errors.append('This username is already being used')
        except ObjectDoesNotExist:
            pass
        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateRegPass(self, request):
        errors = []
        if len(request.POST['password']) < 1:
            errors.append('Password can not be empty')
        elif len(request.POST['password']) < 8:
            errors.append('Password should be more than 7 characters')
        elif not PASS_REGEX.match(request.POST['password']):
            errors.append('Password should contain at least one apper case letter and one number')
        if request.POST['password'] != request.POST['repeat']:
            errors.append('Password repeat did not match the password')
        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateLogin(self, request):
        from bcrypt import hashpw, gensalt
        errors = []
        try:
	        user = self.get(username=request.POST['username'])
	        password = user.pw_hash.encode()
	        loginpass = request.POST['password'].encode()
	        if hashpw(loginpass, password) == password:
	            return (True, user)
	        else:
	            errors.append("Sorry, no password match. Please try again.")
	            return (False, errors)
        except ObjectDoesNotExist:
            pass
        errors.append("Sorry, no username found. Please try again.")
        return (False, errors)

class TravelManager(models.Manager):
    def validateAddTravel(self, request):
        errors = []
        if len(request.POST['destination']) < 1:
            errors.append('Destination can not be empty')
        if len(request.POST['plan']) < 1:
            errors.append('Description can not be empty')
        if len(request.POST['start']) < 1:
            errors.append('Travel Date can not be empty')
        if len(request.POST['end']) < 1:
            errors.append('Travel Date To can not be empty')
        if request.POST['end'] < request.POST['start']:
            errors.append('Travel Date To can not be earlier than Travel Date From')
        if len(errors) > 0:
            return (False, errors)
        return (True, errors)




class User(models.Model):
      username = models.CharField(max_length=45)
      pw_hash = models.CharField(max_length=255)
      user_image = models.ImageField(upload_to='user/', default = 'user/anonym.jpg', null=True, blank=True)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = models.Manager()
      manager = UserManager()

      def __unicode__(self):
          return u"%s" % (self.username)

class Travel(models.Model):
      destination = models.CharField(max_length=255)
      plan = models.TextField(max_length=500)
      start = models.DateField()
      end = models.DateField()
      past = models.BooleanField(default = True)
      travel_image = models.ImageField(upload_to='travel/', default = 'travel/no.jpg', null=True, blank=True)
      user_id = models.ForeignKey(User, related_name='travel_create')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      objects = models.Manager()
      manager = TravelManager()

      def __unicode__(self):
          return u"%s" % (self.destination)

class Join(models.Model):
      travel_id = models.ForeignKey(Travel, related_name='join_travel')
      user_id = models.ForeignKey(User, related_name='join_user')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
