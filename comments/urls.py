from django.urls import path, re_path
from comments import views
__app_name__ = "comments"
urlpatterns = [
    path('submit_comments/', views.submit_comments),
    path('own_comments/', views.own_comments),
]