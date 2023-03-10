"""basketball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from core import views
from authentication.loginView import Login
from authentication.logoutView import LogoutApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', Login.as_view()),
    path('logout/', LogoutApi.as_view()),
    path('health/', views.health, name='health'),
    path('score_board/', views.score_board, name='scoreboard'),
    path('coach/<int:user_id>', views.coach, name='coach'),
    path('player_score/<int:user_id>/', views.player_score, name='player_score'),
    path('all_team_details/<int:user_id>/', views.all_team_details, name='team_details'),
    path('login_details/<int:user_id>/', views.login_details, name='login_details')
]
