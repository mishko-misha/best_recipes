from django.contrib import admin

from recipes.models import *

admin.site.register(Ingredients)
admin.site.register(Recipes)
admin.site.register(RecipeIngredients)
admin.site.register(Ratings)
admin.site.register(Bookmark)
