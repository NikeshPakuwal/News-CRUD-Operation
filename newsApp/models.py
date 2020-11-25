from django.db import models

# Create your models here.
class newsDetails(models.Model):
    newsTitle = models.CharField(max_length=100)
    newsCategory = models.CharField(max_length=30)
    newsDescription = models.CharField(max_length=200)
    newsChannel = models.CharField(max_length=50)
