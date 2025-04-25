from django.urls import path, re_path
from accounts import views
__app_name__ = "accounts"

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.login),
    path('register/', views.register),
    path('check_code/', views.check_code),
    path('editor/', views.editor),
    path('test_redirect/', views.test_redirect),
    path('change_head/', views.change_head),
]