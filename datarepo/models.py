from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id) + '-' + str(self.name)

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = 'products'

