from django.http import HttpResponse
from django.views import View


class RecipeListView(View):
    def get(self, request):
        return HttpResponse("Recipe list")

class RecipeCreateView(View):
    def get(self, request):
        return HttpResponse("Recipe create")

class RecipeDetailView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe detail {id}")

class RecipeUpdateView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe update {id}")

class RecipeDeleteView(View):
    def get(self, request, id):
        return HttpResponse(f"Recipe delete {id}")
