"""registrationSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path(
        'create_account/<str:uid>', views.create_account, name='create_account'
    ),
    path('temp/', views.temp, name='temp'),
    path('status/', views.status, name='status'),
    path('change_status/', views.change_status, name='change_status'),
    path('raft_info/', views.raft_info, name='raft_info'),
    path('admin/', admin.site.urls),
    path('confirm_email/<token>/', views.activate,  name='confirm_email'),
]
