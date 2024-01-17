from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .user_manager import UserProfileManager

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
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    
class ProfileInfo(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE , related_name= "profile")
    profile_pic = models.ImageField(upload_to='static/media/profile_pics', blank=True)
    location = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.email

    def get_followers(self):
        return self.followed_by.all()
    
    def get_followers_count(self):
        return self.followed_by.count()

    def get_followings_count(self):
        return self.follows.count()

    def get_posts_count(self):
        return self.user.post_set.count()

    def get_all_posts(self):
        return self.user.post_set.all()

    def get_all_posts_count(self):
        return self.user.post_set.count()
    
    def get_age(date_of_birth):
        today = date.today()
        birth_date = date_of_birth
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
