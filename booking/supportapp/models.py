from django.db import models

# Create your models here.
from authapp.models import User


class Problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    problem = models.CharField(max_length=1000)
    page = models.CharField(max_length=1000)

    def __str__(self):
        return self.problem


class RequestException(models.Model):
    page = models.CharField(max_length=200)
    exception_text = models.CharField(max_length=1000)
    status_code = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.exception_text