"""
registrationSystem URL Configuration

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
    path('temp/', views.temp, name='temp'),
    # TODO: Remove temp/ when there is a landing page after
    #   creating the full account.
    path('status/', views.status, name='status'),
    path('pay/', views.pay_page, name='pay_page'),
    path('change_status/', views.change_status, name='change_status'),
    # TODO add template for overview page later
    path('admin/', admin.site.urls),
    path('overview/', views.overview, name='overview'),
    path('login/', views.login_user, name='login'),
    path('confirm_email/<token>/', views.activate,  name='confirm_email'),
    path('payment/', views.test_payment, name="make_payment"),
    path(
        'create_account/<str:uid>', views.create_account, name='create_account'
    ),
    path(
        'set_to_won/<str:uid>', views.temp_set_to_won, name='set-status-won'
    ),
    # TODO: Remove set_to_won/ when there is functionality
    #   to change user's status to 'won'.
]
