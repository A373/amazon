# Generated by Django 3.1.7 on 2021-03-24 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0002_auto_20210318_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
