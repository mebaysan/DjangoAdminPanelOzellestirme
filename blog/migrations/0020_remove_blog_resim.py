# Generated by Django 3.0.5 on 2020-05-01 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_blog_resim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='resim',
        ),
    ]