from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Author(models.Model):
    author_name = models.CharField(max_length=200)
    author_age = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.author_name
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)
    def __str__(self):
        return self.book_name
