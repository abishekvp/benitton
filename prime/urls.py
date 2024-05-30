from django.urls import path
from . import views
from app.views import delete_account

urlpatterns = [
    path('', views.home, name='prime'),
    path('home', views.home, name='prime'),
    
    # products routes
    path('view-products', views.view_products, name='prime-view-products'),
    path('products/<str:category>', views.products, name='prime-products'),
    path('product-detail/<str:id>/', views.product_detail, name='prime-product-detail'),
    path('main-category', views.main_category, name='prime-main-category'),
    path('sub-category/<str:name>/', views.sub_category, name='prime-sub-category'),
    
    # account routes
    path('profile', views.profile, name='prime-profile'),
    path('edit-profile', views.edit_profile, name='prime-edit-profile'),
    path('delete-account', delete_account),
]
