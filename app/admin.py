from django.contrib import admin
from app.models import Category, Recipe


class RecipeInlineAdmin(admin.TabularInline):
    model = Recipe
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (RecipeInlineAdmin,)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
