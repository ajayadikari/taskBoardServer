from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class UserModel(AbstractUser):
    pass
    objects = UserManager()

