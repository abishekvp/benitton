from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('authenticating-user',views.auth_user,name="auth_user"),
    path('search',views.search,name="search"),
    path('delete-account',views.delete_account,name="delete-account"),
    path('enquiry',views.enquiry,name="enquiry"),
    path('error',views.error,name="error"),
]
