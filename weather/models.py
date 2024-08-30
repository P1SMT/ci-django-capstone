from django.contrib.auth.models import User
from django.db import models

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.user.username}'
