from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Repositories(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    path_name = models.CharField(max_length=255)


class PatchFile(models.Model):
    sha_commit = models.CharField(max_length=64)
    repository = models.ForeignKey('Repositories')
