# Generated by Django 3.0.5 on 2020-04-26 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200426_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100)),
                ('yayin_mi', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoriler',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(related_name='bloglar', to='blog.Kategori'),
        ),
    ]
