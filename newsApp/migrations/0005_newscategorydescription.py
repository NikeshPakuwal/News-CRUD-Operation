# Generated by Django 3.1.3 on 2020-12-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsApp', '0004_auto_20201208_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='newsCategoryDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsCategoryTitle', models.CharField(max_length=98)),
            ],
        ),
    ]
