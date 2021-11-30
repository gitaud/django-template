from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
	"""Manager for user profiles"""
	def create_user(self, email, name, password=None):
		"""Create a new user profile"""
		if not email:
			raise ValueError('User must supply an email')
		
		email = self.normalize_email(email)
		user = self.model(email=email, name=name)

		user.set_password(password)
		user.save(using=self._db)

		return user
	
	def create_company_staff(self, email, name, password):
		"""Create a new company user"""
		user = self.create_user(email, name, password)
		user.is_company_staff = True
	
	def create_superuser(self, email, name, password):
		"""Create a new superuser profile"""
		user = self.create_user(email, name, password)
		user.is_superuser = True
		user.is_staff = True
		user.is_company_staff = True

		user.save(using=self._db)

		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
	""" Database model for users in the system"""
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_company_staff = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']
	EMAIL_FIELD = 'email'

	def __str__(self):
		"""Returns the string representation of a user object """
		return self.email