from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .user_manager import UserProfileManager
# Create your models here.
class UserProfile(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} + {self.last_name}"

    def get_short_name(self):
        return self.first_name
