from django.urls import path
from KVGH_API import views


urlpatterns = [
    path('crypto/prime', views.crypto_prime, name='prime'),
    path('crypto/link', views.crypto_link, name='link'),
    path('authorize', views.authorize, name='authorize'),
    path('create/<str:element>', views.create, name='create'),
    path('read/<str:element>/<int:req_id>', views.read, name='read'),
    path('delete/<str:element>', views.delete, name='delete'),
    path('update/<str:element>', views.update, name='update'),
]
