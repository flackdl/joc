from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Recipe(models.Model):
    name = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructions = models.TextField()

    class Meta:
        indexes = [
            GinIndex(fields=['name', 'instructions']),
        ]

    def __str__(self):
        return self.name
