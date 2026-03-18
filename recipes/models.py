from django.db import models

class  Ingredients(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Recipes(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cooking_time = models.IntegerField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.description} - {self.cooking_time} - {self.author.username}"

    def __repr__(self):
        return f"{self.title} - {self.description} - {self.cooking_time} - {self.author.username}"

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,related_name="ingredients")
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient} - {self.amount}"

    def __repr__(self):
        return f"{self.recipe} - {self.ingredient} - {self.amount}"