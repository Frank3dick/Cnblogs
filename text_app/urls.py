from django.urls import path, re_path
from text_app import views

__app_name__ = "text_app"
urlpatterns = [
    path('clean_login/', views.clean_login),
    path('own_articles/', views.own_articles),
    path('header_ex/', views.header_ex),
    path('create_articles/', views.create_articles),
    re_path('detail-(\\d+)-(\\d+)/', views.detail),
    path('own_articles/', views.own_articles),
    re_path('delete-(\\d+)/', views.delete_article),
    re_path('alter_article-(\\d+)-(\\d+)/', views.alter_article),
]