from django_filters import rest_framework as filters
from app.models import Category, Recipe


class CategoryFilter(filters.ModelChoiceFilter):

    def _child_categories(self, category: Category):
        # recursively generate category children
        result = [category]
        children = Category.objects.filter(parent=category)
        for child in children:
            result.extend(self._child_categories(child))
        return result

    def filter(self, qs, category):
        if category:
            # recursively return recipes from all child categories
            children = self._child_categories(category)
            qs = qs.filter(category__in=children)
        return qs


class RecipeFilterSet(filters.FilterSet):
    # overridden to include all category children
    category = CategoryFilter(field_name='category', queryset=Category.objects.all())

    class Meta:
        model = Recipe
        fields = ['name', 'category']
