# Generated by Django 3.0.5 on 2020-04-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20200426_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategori',
            name='ad',
            field=models.CharField(max_length=100, verbose_name='Kategorinin Adı'),
        ),
    ]
