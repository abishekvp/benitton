from django.urls import path
from . import views
from app.views import delete_account

urlpatterns = [
    path('', views.home, name='guser'),
    path('home', views.home, name='guser'),
    
    # products routes
    path('view-products', views.view_products, name='guser-view-products'),
    path('products/<str:category>', views.products, name='guser-products'),
    path('product-detail/<str:id>/', views.product_detail, name='guser-product-detail'),
    path('main-category', views.main_category, name='guser-main-category'),
    path('sub-category/<str:name>/', views.sub_category, name='guser-sub-category'),
    
    # account routes
    path('profile', views.profile, name='guser-profile'),
    path('edit-profile', views.edit_profile, name='guser-edit-profile'),
    path('delete-account', delete_account),
]
