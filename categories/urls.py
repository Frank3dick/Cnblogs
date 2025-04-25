from django.urls import path, re_path
from categories import views

__app_name__ = "categories"

urlpatterns = [
    path('create_categories/', views.create_categories),
    re_path('dif_categories-(\\d+)/', views.into_dif_group, name='dif_categories'),
    re_path('dif_categories/', views.dif_categories),
]