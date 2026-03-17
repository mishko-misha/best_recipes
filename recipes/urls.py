from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:id>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:id>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:id>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]