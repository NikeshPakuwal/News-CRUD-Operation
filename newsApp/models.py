from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=99)

    def __str__(self):
        return self.title

class newsDetails(models.Model):
    newsTitle = models.CharField(max_length=100)
    newsCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    newsDescription = models.TextField()
    newsChannel = models.CharField(max_length=50)