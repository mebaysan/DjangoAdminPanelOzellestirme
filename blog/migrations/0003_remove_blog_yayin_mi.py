# Generated by Django 3.0.5 on 2020-04-24 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200425_0235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='yayin_mi',
        ),
    ]