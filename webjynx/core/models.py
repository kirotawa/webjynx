from django.db import models


# Create your models here.
class Repositories(models.Model):
    name = models.CharField(max_length=200)
    path_name = models.CharField(max_length=255)


class PatchFile(models.Model):
    sha_commit = models.CharField(max_length=64)
    repository = models.ForeignKey('Repositories')
