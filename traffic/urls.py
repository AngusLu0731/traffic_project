"""traffic_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from traffic import views
app_name = "tra"
urlpatterns = [
    path('index/', views.index),
    path('enroll/', views.enroll),
    path('feedback/', views.feedback),
    path('member/',views.member),
    path('member_fix/',views.member_fix),
    path('edit/',views.edit),
    path('search/',views.search),
    path('gps/',views.gps,name='gps'),
    path('gps/map',views.gps),
    path('welcome/',views.welcome),
    path('',views.welcome),
    
]


