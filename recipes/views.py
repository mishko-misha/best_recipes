from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from common.forms import RecipeForm, RecipeIngredientForm
from recipes.models import Recipes, Ingredients


class RecipeListView(View):
    template_name = "recipes_list.html"

    def get(self, request):
        list_form = RecipeForm()
        recipes = Recipes.objects.all()
        return render(request, self.template_name, context={"form": list_form, "recipes": recipes}, )


class RecipeDetailView(View):
    template_name = "recipe_detail.html"

    def get(self, request, recipe_id):
        list_form = RecipeForm()
        recipe = Recipes.objects.get(id=recipe_id)
        return render(request, self.template_name, context={"form": list_form, "recipe": recipe}, )


@method_decorator(login_required, name='dispatch')
class RecipeCreateView(View):
    template_name = "recipe_create.html"

    def get(self, request):
        create_form = RecipeForm()
        return render(request, self.template_name, context={"form": create_form}, )

    def post(self, request):
        create_form = self.form_class(request.POST)
        if create_form.is_valid():
            recipe = Recipes.objects.create(author=request.user, **create_form.cleaned_data)
            recipe.save()
        return render(request, self.template_name, context={"form": create_form}, )

@method_decorator(login_required, name='dispatch')
class RecipeCreateIngredientView(View):
    template_name = "recipe_create_ingredient.html"
    
    def get(self, request):
        ingredient_form = RecipeIngredientForm()
        return render(request, self.template_name, context={"ingredient_form": ingredient_form}, )

    def post(self, request):
        ingredient_form = self.form_class(request.POST)
        if ingredient_form.is_valid():
            ingredient = Ingredients.objects.create(**ingredient_form.cleaned_data)
            ingredient.save()
        return render(request, self.template_name, context={"ingredient_form": ingredient_form}, )

class RecipeUpdateView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe update {id}")


class RecipeDeleteView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe delete {id}")
