from django.urls import path

from . import views

urlpatterns = [
    path('recipes/', views.RecipeListView.as_view(), name='recipes_list'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:recipe_id>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:recipe_id>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:recipe_id>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]
