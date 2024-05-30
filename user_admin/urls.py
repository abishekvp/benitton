from django.urls import path
from . import views
from app.views import delete_account

urlpatterns = [
    path('', views.index, name='user-admin'),
    path('home', views.index, name='user-admin-home'),
    
    # products routes
    path('create-product', views.create_product, name='admin-create-product'),
    path('edit-product/<str:id>/', views.edit_product, name='admin-edit-product'),
    path('delete-product/<str:id>/', views.delete_product, name='admin-delete-product'),
    
    path('view-products', views.view_products, name='admin-view-products'),
    path('trending-products', views.trending_products, name='admin-trending-product'),
    path('gallery-products', views.gallery_products, name='admin-gallery-products'),
    path('products/<str:category>', views.products, name='admin-products'),
    path('product-detail/<str:id>/', views.product_detail, name='admin-product-detail'),
    
    # requests
    path('enquiries', views.enquiries, name='admin-enquiry'),
    path('enquiry-form/<str:id>/', views.enquiry_form, name='admin-enquiry-form'),
    path('delete-enquiry/<str:id>/', views.delete_enquiry, name='admin-delete-enquiry'),
    path('plumber-requests', views.plumber_requests, name='admin-plumber-requests'),
    path('plumber-request/<str:id>/', views.plumber_request, name='admin-plumber-request'),
    path('delete-request/<str:id>/', views.delete_plumber_request, name='admin-delete-request'),

    # category
    path('main-category', views.main_category, name='admin-main-category'),
    path('main-category/<str:name>/', views.main_category, name='admin-main-category'),
    path('sub-category/<str:name>/', views.sub_category, name='admin-sub-category'),
    path('create-main-category', views.create_main_category, name='create-main-category'),
    path('create-sub-category', views.create_sub_category, name='create-sub-category'),
    path('edit-main-category/<str:name>/', views.edit_main_category, name='admin-edit-main-category'),
    path('edit-sub-category/<str:name>/', views.edit_sub_category, name='admin-edit-sub-category'),
    path('delete-main-category/<str:name>/', views.delete_main_category, name='admin-delete-main-category'),
    path('delete-sub-category/<str:name>/', views.delete_sub_category, name='admin-delete-sub-category'),

    # coient routes
    path('clients', views.clients, name='clients'),
    path('approve-user/<str:email>/', views.approve_user, name='approve-user'),
    path('revoke-user/<str:email>/', views.revoke_user, name='revoke-user'),
    path('remove-user/<str:email>/', views.remove_user, name='remove-user'),

    # accounts route 
    path('profile', views.profile, name='user-admin-profile'),
    path('edit-profile', views.edit_profile, name='user-admin-edit-profile'),
    path('delete-account', delete_account, name='delete-account'),
    
    # test
    path('test', views.test, name='test'),
]