"""server URL Configuration

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
from django.urls import re_path
from . import views

app_name = "users"

urlpatterns = [
    # users
    re_path(r"^register[/]?$", views.RegisterView.as_view(), name="register"),
    re_path(
        r"^username/(?P<username>[a-zA-Z0-9_-]{5,20})/count[/]?$",
        views.UsernameCountView.as_view(),
        name="username_count",
    ),
    re_path(
        r"^mobiles/(?P<mobile>1[3-9]\d{9})/count[/]?$",
        views.MobileCountView.as_view(),
        name="mobile_count",
    ),
    re_path(
        r"^login[/]?$",
        views.LoginView.as_view(),
        name="login",
    ),
    re_path(
        r"^user[/]?$",
        views.UserInfoView.as_view(),
        name="user_info",
    ),
]
