# Generated by Django 3.1.3 on 2021-01-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsApp', '0002_semrush'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[(0, 'Male'), (1, 'Female')], default='M', max_length=10)),
                ('dob', models.DateField(blank=True, null=True)),
                ('address', models.TextField(default='Address')),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
            ],
        ),
    ]
