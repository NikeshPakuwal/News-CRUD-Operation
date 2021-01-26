from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=99)

    def __str__(self):
        return self.title

class newsDetails(models.Model):
    newsTitle = models.CharField(max_length=100)
    newsCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    newsDescription = RichTextField(blank=True, null=True)
    newsChannel = models.CharField(max_length=50)

class todoList(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now,blank=True)

class webScraping(models.Model):
    url = models.TextField(default="https://hollywoodmask.com/lgbtiq/tim-dillon-gay.html")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Semrush(models.Model):
    objects = None
    Item = None
    country = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    seed_keyword = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    volume = models.IntegerField(max_length=255, blank=True, null=True)
    keyword_difficulty = models.CharField(max_length=255, blank=True, null=True)
    ccp = models.CharField(max_length=255, blank=True, null=True)
    competitive_density = models.CharField(max_length=255, blank=True, null=True)
    number_of_results = models.CharField(max_length=255, blank=True, null=True)
    serp_Features = models.TextField(blank=True, null=True)
    trend = models.CharField(max_length=255, blank=True, null=True)
    click_potential = models.CharField(max_length=255, blank=True, null=True)
    competitors = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.country+" "+self.seed_keyword

class SerpDataLink(models.Model):
    keyword_id = models.ForeignKey(Semrush, on_delete=models.CASCADE, related_name='serp_semrush')
    links = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.keyword_id) + '|' + str(self.links)

    def get_absolute_url(self):
        return reverse('list_serpview')

class Employee(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender_male = 0
    gender_female = 1
    gender_choices = [(gender_male, 'Male'), (gender_female, 'Female')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    dob = models.DateField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

