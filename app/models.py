from django.db import models
from django.contrib.auth.models import Group

# Group.objects.create(name='super-admin')
# Group.objects.create(name='user_admin')
# Group.objects.create(name='per_user')
# Group.objects.create(name='plumber')
# Group.objects.create(name='prime')

class AdminProduct(models.Model):
    product_id = models.CharField(max_length=128,primary_key=True)
    pro_code = models.CharField(max_length=128)
    pro_name = models.CharField(max_length=128)
    main_category = models.CharField(max_length=32,default="")
    sub_category = models.CharField(max_length=32,default="")
    pro_series = models.CharField(max_length=64,default="",null=True)
    pro_description = models.TextField()
    pro_image = models.TextField()
    pro_features = models.TextField(default="")
    pro_price = models.IntegerField()
    pro_price_per_user = models.IntegerField()
    pro_price_plumber = models.IntegerField()
    pro_price_prime = models.IntegerField()
    trending = models.BooleanField(default=0)
    gallery_view = models.BooleanField(default=0)

class ProductEnquiry(models.Model):
    request_id = models.CharField(max_length=128,primary_key=True)
    user_name = models.CharField(max_length=32)
    user_contact = models.CharField(max_length=32)
    user_city = models.CharField(max_length=32)
    user_state = models.CharField(max_length=32)
    user_message = models.TextField()
    product_code = models.CharField(max_length=32)
    product_name = models.CharField(max_length=32)
    recieved_on = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=128, default="")

class MainCategory(models.Model):
    cat_id = models.CharField(max_length=128,default="")
    name = models.CharField(max_length=64,primary_key=True)
    description = models.TextField(default="")
    image = models.TextField(default="")

class SubCategory(models.Model):
    cat_id = models.CharField(max_length=128,default="")
    main_category = models.CharField(max_length=64)
    name = models.CharField(max_length=64,primary_key=True)
    description = models.TextField(default="")
    image = models.TextField(default="")

class PlumberRequest(models.Model):
    request_id = models.CharField(max_length=64,primary_key=True)
    name = models.CharField(max_length=32)
    contact = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    recieved_on = models.DateTimeField(auto_now_add=True)
    plumber_visit = models.BooleanField(default=0)
    product_image = models.TextField(default="")
    recieved_on = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=128, default="")
