from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from common.forms import RecipeForm, IngredientForm
from recipes.models import Recipes, Ingredients


class RecipeListView(View):
    template_name = "recipes_list.html"
    form_class = RecipeForm

    def get(self, request):
        list_form = self.form_class()
        recipes = Recipes.objects.all()
        return render(request, self.template_name, context={"form": list_form, "recipes": recipes}, )


class RecipeDetailView(View):
    template_name = "recipe_detail.html"
    form_class = RecipeForm

    def get(self, request, recipe_id):
        list_form = self.form_class()
        recipe = Recipes.objects.get(id=recipe_id)
        return render(request, self.template_name, context={"form": list_form, "recipe": recipe}, )


@method_decorator(login_required, name='dispatch')
class RecipeCreateView(View):
    template_name = "recipe_create.html"
    form_class = RecipeForm

    def get(self, request):
        create_form = self.form_class()
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
    form_class = IngredientForm
    
    def get(self, request):
        ingredient_form = self.form_class()
        return render(request, self.template_name, context={"ingredient": ingredient_form}, )

    def post(self, request):
        ingredient_form = self.form_class(request.POST)
        if ingredient_form.is_valid():
            ingredient = Ingredients.objects.create(**ingredient_form.cleaned_data)
            ingredient.save()
        return render(request, self.template_name, context={"ingredient": ingredient_form}, )

class RecipeUpdateView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe update {id}")


class RecipeDeleteView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe delete {id}")
