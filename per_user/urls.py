from django.urls import path
from . import views
from app.views import delete_account

urlpatterns = [
    path('', views.home, name='per_user'),
    path('home', views.home, name='per_user'),
    
    # products routes
    path('view-products', views.view_products, name='user-view-products'),
    path('products/<str:category>', views.products, name='user-products'),
    path('product-detail/<str:id>/', views.product_detail, name='user-product-detail'),
    path('main-category', views.main_category, name='user-main-category'),
    path('sub-category/<str:name>/', views.sub_category, name='user-sub-category'),
    
    # account routes
    path('profile', views.profile, name='per_user-profile'),
    path('edit-profile', views.edit_profile, name='per_user-edit-profile'),
    path('delete-account', delete_account),
]