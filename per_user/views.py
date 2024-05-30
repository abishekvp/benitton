from django.shortcuts import render, redirect
from django.contrib.auth import login
from app.models import AdminProduct as Product, ProductEnquiry as Enquiry, MainCategory, SubCategory, PlumberRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from app.views import get_role_name, remove_spcl_ch
import base64
import datetime
# Create your views here.

def is_user(user):
    if user.groups.filter(name='per_user').exists():
        return True

@user_passes_test(is_user)
def index(request):
    return render(request, 'per_user/index.html')

@user_passes_test(is_user)
def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']        
        try:
            if request.POST['plumber_visit']=='on':plumber_visit = True
        except:plumber_visit = False
        if 'product_image' in request.FILES:
            image = base64.b64encode(request.FILES['product_image'].read()).decode('utf-8')
        else:image = None
        
        PlumberRequest.objects.create(
            request_id=str(name+contact+address+str(datetime.datetime.now()).strip()).replace(' ','').replace(':','').replace('-','').replace('.',''),
            name=name,
            contact=contact,
            address=address,
            plumber_visit=plumber_visit,
            product_image=image
        )
      
    trendings_products_one = Product.objects.filter(trending=True)[:4]
    trendings_products_two = Product.objects.filter(trending=True)[4:]
    
    gallery_products = Product.objects.filter(gallery_view=True)
    
    product_one = Product.objects.filter(trending=True).first()
    if product_one!=None:
        features = product_one.pro_features.split('\n')
        for j in range(len(features)):
            features[j] = features[j].strip()
        product_one.pro_features = features
    
    product_two = Product.objects.filter(trending=True).last()
    if product_two!=None:        
        features = product_two.pro_features.split('\n')
        for j in range(len(features)):
            features[j] = features[j].strip()
        product_two.pro_features = features
    
    return render(request, 'per_user/home.html',{'gallery_products':gallery_products,'product_one':product_one,'product_two':product_two,'trending_products_one':trendings_products_one,'trending_products_two':trendings_products_two,'gallery_products':Product.objects.filter(gallery_view=True)})

@user_passes_test(is_user)
def view_products(request):
    return render(request, 'per_user/view-products.html',{'products':Product.objects.all(),'main_categories':MainCategory.objects.all()})

@user_passes_test(is_user)
def main_category(request):
    return render(request, 'per_user/main-category.html',{'trending_products':Product.objects.filter(trending=True)[:4],'main_categories':MainCategory.objects.all()})

@user_passes_test(is_user)
def sub_category(request,name):
    return render(request, 'per_user/sub-category.html',{
        'main_category':MainCategory.objects.filter(name=name).get(),
        'sub_categories':SubCategory.objects.filter(main_category=name),
        'related_products':Product.objects.filter(main_category=name)[:4],
    })

@user_passes_test(is_user)
def products(request,category):
    if request.user.is_authenticated and request.user.groups.filter(name='per_user').exists():
        products = []
        for i in Product.objects.filter(sub_category=str(category).lower()).all():
            products.append(i)
        if len(products)==0:
            for i in Product.objects.filter(main_category=str(category).lower()).all():
                products.append(i)
        return render(request, 'per_user/view-products.html', {'products': products,'main_categories':MainCategory.objects.all()})
    else:return redirect('signin')

@user_passes_test(is_user)
def product_detail(request,id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.groups.filter(name='per_user').exists():
                user_name = request.POST.get('user_name')
                user_contact = str(request.POST.get('user_contact')).strip()
                user_city = str(request.POST.get('user_city')).strip()
                user_state = str(request.POST.get('user_state')).strip()
                user_message = str(request.POST.get('user_message')).strip()
                enquiry = {
                    'request_id': remove_spcl_ch([datetime.datetime.now(),user_name,user_contact,user_city,user_state]),
                    'user_name': user_name,
                    'user_contact': user_contact,
                    'user_city': user_city,
                    'user_state': user_state,
                    'user_message': user_message,
                    'product_code':Product.objects.filter(product_id=id).get().pro_code,
                    'product_name':Product.objects.filter(product_id=id).get().pro_name,
                }
                Enquiry.objects.create(**enquiry)
                return redirect('user-product-detail',id)
            else:return redirect('auth_user')
        else:return redirect('signin')
    product = Product.objects.filter(product_id=id).get()
    features = product.pro_features.split('\n')
    for j in range(len(features)):
        features[j] = features[j].strip()
    product.pro_features = features
    return render(request, 'per_user/product-details.html',{'product': product})

@user_passes_test(is_user)
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'per_user/profile.html', {'user': request.user,"role":get_role_name(request)})
    else:
        return redirect('signin')

@user_passes_test(is_user)
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=request.user.email)
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        if password != '':
            user.set_password(password)
        user.save()
        login(request, user)
        return redirect("per_user-profile")
    return render(request, 'per_user/editprofile.html', {'user': request.user})

