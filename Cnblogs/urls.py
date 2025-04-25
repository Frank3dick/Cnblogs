"""
URL configuration for Cnblogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path, include
from text_app import urls as text_app_urls
from comments import urls as comments_urls
from categories import urls as categories_urls
from accounts import urls as accounts_urls
from text_app import views as text_app_views

urlpatterns = [
    #    path("admin/", admin.site.urls),
    # path('', text_app_views.index),
    path('text_app/', include(text_app_urls)),
    path('comments/', include(comments_urls)),
    path('categories/', include(categories_urls)),
    path('accounts/', include(accounts_urls)),
    path('', text_app_views.home, name='home'),
]
