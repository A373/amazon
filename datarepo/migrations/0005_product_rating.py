# Generated by Django 3.1.7 on 2021-03-29 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0004_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]