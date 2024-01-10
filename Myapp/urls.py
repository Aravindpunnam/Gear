from django.urls import path
from . import views


urlpatterns=[
    path('',views.store, name='store'),
    path('cart',views.cart, name='cart'),
    path('checkout',views.checkout, name='checkout'),
    path('login',views.login1, name='login'),
    path('logout',views.logout, name='logout'),
    path('register',views.register, name='register'),
    path('update_item/',views.updateItem, name='update_item'),
    path('product_detail/<int:product_id>/',views.product_detail, name='product_detail'),
    path('processorder/', views.processOrder, name='processorder'),
    path('myorders', views.completed_orders, name='processorder'),
    path('search/', views.search_view, name='search'),


    path('photography/', views.category_view, {'category': 'Photography'}, name='photography'),
    path('paintings/', views.category_view, {'category': 'Painting'}, name='paintings'),
    path('drawing/', views.category_view, {'category': 'Drawing'}, name='drawing'),
    path('sculpture/', views.category_view, {'category': 'Sculpture'}, name='sculpture'),
    path('mixed-media/', views.category_view, {'category': 'Mixed Media'}, name='mixed_media'),
]