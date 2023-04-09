"""
URL configuration for KVGHBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from KVGH_API import views

urlpatterns = [
    path('hotel/create/', views.hotel_create, name='hotel_create'),
    path('hotel/read/<int:req_id>/', views.hotel_read, name='hotel_read'),
    path('hotel/delete/', views.hotel_delete, name='hotel_delete'),
    path('hotel/update/', views.hotel_update, name='hotel_update'),
]
