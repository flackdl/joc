from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Recipe(models.Model):
    name = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
