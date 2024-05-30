from django.urls import path
from . import views
from app.views import delete_account

urlpatterns = [
    path('', views.home, name='plumber'),
    path('home', views.home, name='plumber'),
    
    # products routes
    path('view-products', views.view_products, name='plumber-view-products'),
    path('products/<str:category>', views.products, name='plumber-products'),
    path('product-detail/<str:id>/', views.product_detail, name='plumber-product-detail'),
    path('main-category', views.main_category, name='plumber-main-category'),
    path('sub-category/<str:name>/', views.sub_category, name='plumber-sub-category'),
    
    # account routes
    path('profile', views.profile, name='plumber-profile'),
    path('edit-profile', views.edit_profile, name='plumber-edit-profile'),
    path('delete-account', delete_account),
]