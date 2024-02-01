"""Vehicle_health URL Configuration

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
from App_vehicle import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',views.Home),
    path('',views.Home),
    path('Sign_in/',views.Sign_in,name='signin'),
    path('Sign_up/',views.Sign_up),
    path('Dashboard/',views.Dashboard),
    path('Sign_in/Add_Entry/vid=<int:vid>',views.Add_Entry,name='add_entry'),
    path('Sign_in/All_Entry/vid=<int:vid>',views.All_Entry,name='all_entry'),
    path('Result/vid=<int:vid>',views.Result,name='reports'),
    path("delete_entry/<int:vnos>",views.delete_entry),
   
]
