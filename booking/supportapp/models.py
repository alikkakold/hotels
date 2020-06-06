from django.db import models

# Create your models here.
from authapp.models import User


class Problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.CharField(max_length=1000)
    page = models.CharField(max_length=1000)

    def __str__(self):
        return self.problem