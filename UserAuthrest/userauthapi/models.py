from django.contrib.auth.models import User
from django.db import models

# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#   username = None
#   email = models.EmailField('email address', unique=True)
#   first_name = models.CharField(
#     'First Name', max_length=255, blank=True, null=False)
#   last_name = models.CharField(
#     'Last Name', max_length=255, blank=True,null=False)
#   USERNAME_FIELD = 'email'
#   # EMAIL_FIELD = 'email'
#   REQUIRED_FIELDS =[]
#   objects = UserManager()

#   # def __str__(self):
#   #   return f"{self.email} {self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(
        'First Name', max_length=255, blank=True, null=False)
    last_name = models.CharField(
        'Last Name', max_length=255, blank=True, null=False)

    class meta:
        model = User
        fields = '__all__'
