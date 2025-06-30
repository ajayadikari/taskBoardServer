from django.db import models
from user.models import UserModel

class BoardModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, null=False, blank=False)
    

    def __str__(self):
        return f'{self.id}'