from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class  Ingredients(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipes(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cooking_time = models.IntegerField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.description} - {self.cooking_time} - {self.author.username}"

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,related_name="ingredients")
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)

    class Meta:
        unique_together = (('recipe', 'ingredient'),)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient} - {self.amount}"


class Ratings(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,related_name="ratings")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'], name='unique_recipe_user_rating')]

    def __str__(self):
        return f"{self.recipe} - {self.user} - {self.rating}"