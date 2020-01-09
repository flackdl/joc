from rest_framework import viewsets
from app.api.filtersets import RecipeFilterSet
from app.api.serializers import CategorySerializer, RecipeSerializer
from app.models import Category, Recipe


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['parent', 'name']
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilterSet
    search_fields = ['@instructions']
