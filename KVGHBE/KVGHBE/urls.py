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
    path('user/crypto_in/', views.crypto_in, name='crypto_in'),
    path('user/crypto_out/', views.crypto_out, name='crypto_out'),
    path('hotel/create/', views.hotel_create, name='hotel_create'),
    path('hotel/read/<int:req_id>/', views.hotel_read, name='hotel_read'),
    path('hotel/delete/', views.hotel_delete, name='hotel_delete'),
    path('hotel/update/', views.hotel_update, name='hotel_update'),
    # path('room_type/create/', views.room_type_create, name='room_type_create'),
    # path('room_type/read/<int:req_id>/', views.room_type_read, name='room_type_read'),
    # path('room_type/delete/', views.room_type_delete, name='room_type_delete'),
    # path('room_type/update/', views.room_type_update, name='room_type_update'),
    # path('room/create/', views.room_create, name='room_create'),
    # path('room/read/<int:req_id>/', views.room_read, name='room_read'),
    # path('room/delete/', views.room_delete, name='room_delete'),
    # path('room/update/', views.room_update, name='room_update'),
    # path('user_role/create/', views.user_role_create, name='user_role_create'),
    # path('user_role/read/<int:req_id>/', views.user_role_read, name='user_role_read'),
    # path('user_role/delete/', views.user_role_delete, name='user_role_delete'),
    # path('user_role/update/', views.user_role_update, name='user_role_update'),
    # path('user/create/', views.user_create, name='user_create'),
    # path('user/read/<int:req_id>/', views.user_read, name='user_read'),
    # path('user/delete/', views.user_delete, name='user_delete'),
    # path('user/update/', views.user_update, name='user_update'),
    # path('customer/create/', views.customer_create, name='customer_create'),
    # path('customer/read/<int:req_id>/', views.customer_read, name='customer_read'),
    # path('customer/delete/', views.customer_delete, name='customer_delete'),
    # path('customer/update/', views.customer_update, name='customer_update'),
    # path('reservation/create/', views.reservation_create, name='reservation_create'),
    # path('reservation/read/<int:req_id>/', views.reservation_read, name='reservation_read'),
    # path('reservation/delete/', views.reservation_delete, name='reservation_delete'),
    # path('reservation/update/', views.reservation_update, name='reservation_update'),
]
