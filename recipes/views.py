from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from common.forms import RecipeForm, RecipeIngredientsForm
from recipes.models import Recipes, Ingredients, RecipeIngredients


class RecipeListView(View):
    template_name = "recipes_list.html"

    def get(self, request):
        query = request.GET.get('name', '')

        recipes = Recipes.objects.all()

        if query:
            recipe_name = Recipes.objects.filter(title__icontains=query)
            ingredient_name = Recipes.objects.filter(
                ingredients__ingredient__name__icontains=query
            )

            recipes = (recipe_name | ingredient_name).distinct()

        return render(
            request,
            self.template_name,
            {
                "recipes": recipes,
                "query": query
            }
        )

class RecipeDetailView(View):
    template_name = "recipe_detail.html"

    def get(self, request, recipe_id):
        list_form = RecipeForm()
        recipe = Recipes.objects.get(id=recipe_id)
        return render(request, self.template_name, context={"form": list_form, "recipe": recipe}, )

@method_decorator(login_required, name='dispatch')
class RecipeCreateView(View):
    template_name = "recipe_create.html"
    recipe_class = RecipeForm
    recipe_ingredient_form = RecipeIngredientsForm

    def get(self, request):
        create_form = self.recipe_class()
        ingredient_form = self.recipe_ingredient_form()
        return render(request, self.template_name, context={"form": create_form, "ingredient_form": ingredient_form}, )

    def post(self, request):
        create_form = self.recipe_class(request.POST)
        ingredient_form = self.recipe_ingredient_form(request.POST)
        if create_form.is_valid():
            recipe = Recipes.objects.create(author=request.user, **create_form.cleaned_data)

            # Save all ingredients sent as ingredient_name[] / ingredient_amount[]
            names = request.POST.getlist('ingredient_name[]')
            amounts = request.POST.getlist('ingredient_amount[]')
            for name, amount in zip(names, amounts):
                name = name.strip()
                amount = amount.strip()
                if name:
                    ingredient, _ = Ingredients.objects.get_or_create(name=name)
                    RecipeIngredients.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount,
                    )

            return redirect('recipe_detail', recipe_id=recipe.id)

        return render(request, self.template_name, context={"form": create_form, "ingredient_form": ingredient_form}, )


@method_decorator(login_required, name='dispatch')
class RecipeUpdateView(View):
    template_name = "recipe_edit.html"
    recipe_class = RecipeForm
    recipe_ingredient_form = RecipeIngredientsForm

    def get(self, request, recipe_id):
        recipe = Recipes.objects.get(id=recipe_id)
        update_form = self.recipe_class(instance=recipe)
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe).select_related("ingredient").order_by("id")

        ingredient_rows = [
            {
                "ingredient_name": recipe_ingredients.ingredient.name,
                "ingredient_amount": recipe_ingredients.amount
            }
            for recipe_ingredients in recipe_ingredients
        ]

        ingredient_form = self.recipe_ingredient_form()

        return render(
            request,
            self.template_name,
            context={"form": update_form, "recipe": recipe, "ingredient_form": ingredient_form,
                     "recipe_ingredients": recipe_ingredients, "ingredient_rows": ingredient_rows}, )

    def post(self, request, recipe_id):
        recipe = Recipes.objects.get(id=recipe_id)
        update_form = self.recipe_class(request.POST, instance=recipe)

        if update_form.is_valid():
            recipe = update_form.save()

            names = request.POST.getlist('ingredient_name[]')
            amounts = request.POST.getlist('ingredient_amount[]')

            # use clears fields as name, amount and when click save, it will delete ingredients
            RecipeIngredients.objects.filter(recipe=recipe).delete()

            for name, amount in zip(names, amounts):
                name = name.strip()
                amount = amount.strip()
                if name and amount:
                    ingredient, _ = Ingredients.objects.get_or_create(name=name)
                    RecipeIngredients.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount
                    )

            return redirect('recipe_detail', recipe_id=recipe.id)

        # Collect all  ingredients which related to recipe
        recipe_ingredients = (
            RecipeIngredients.objects
            .filter(recipe=recipe)
            .select_related("ingredient")
            .order_by("id")
        )

        ingredient_rows = [
            {
                "ingredient_name": ri.ingredient.name,
                "ingredient_amount": ri.amount
            }
            for ri in recipe_ingredients
        ]

        return render(
            request,
            self.template_name,
            context={
                "form": update_form,
                "recipe": recipe,
                "recipe_ingredients": recipe_ingredients,
                "ingredient_rows": ingredient_rows
            },
        )


@method_decorator(login_required, name='dispatch')
class RecipeDeleteView(View):
    def get(self, request, recipe_id):
        recipe = Recipes.objects.get(id=recipe_id)
        return render(request, "recipe_delete", {"recipe": recipe})

    def post(self, request, recipe_id):
        recipe = Recipes.objects.get(id=recipe_id)

        RecipeIngredients.objects.filter(recipe=recipe).delete()

        recipe.delete()

        return redirect('recipes_list')
