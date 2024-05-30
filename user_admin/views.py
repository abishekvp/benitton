from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
from app.models import ProductEnquiry as Enquiry, AdminProduct as Product, MainCategory, SubCategory, PlumberRequest
import datetime
import base64
from app.views import get_role_name, remove_spcl_ch

def is_admin(request):
    if request.user.groups.filter(name='user_admin').exists():
        return True
    else:
        return False

def generate_product_id(code, name, series):
    import re
    id = str(
        str(datetime.datetime.now())+"-"+
        str(name).strip()+"-"+
        str(code).strip()+"-"+
        str(series).strip()
    )
    for j in id:
        if j.isalnum()==False and j!='-':
            id = id.replace(j,'-')
    id = re.sub(r'-+', '-', id)
    return id

def test(request):
    for i in Product.objects.all():
        pass
        
    return HttpResponse("Done")

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']        
        try:
            if request.POST['plumber_visit']=='on':plumber_visit = True
        except:plumber_visit = False
        if 'product_image' in request.FILES:
            image = base64.b64encode(request.FILES['product_image'].read()).decode('utf-8')
        else:image = ""
        id=str(str(datetime.datetime.now())+"-"+name+"-"+contact).strip()
        for i in id:
            if i.isalnum()==False and i!='-':
                id = id.replace(i,'-')
        PlumberRequest.objects.create(
            request_id=id,
            name=name,
            contact=contact,
            address=address,
            plumber_visit=plumber_visit,
            product_image=image
        )
    if is_admin(request):
          
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
        
        return render(request, 'user_admin/home.html',{'main_categories':MainCategory.objects.all(),'gallery_products':gallery_products,'product_one':product_one,'product_two':product_two,'trending_products_one':trendings_products_one,'trending_products_two':trendings_products_two[:4],'gallery_products':Product.objects.filter(gallery_view=True)})
    else:
        return redirect('auth_user')

def enquiries(request):
    if request.user.is_authenticated and is_admin(request):
        if is_admin(request):
            return render(request, 'user_admin/enquiries.html',{'enquiries':Enquiry.objects.all()})
        else:
            return redirect('auth_user')
    else:
        return redirect('signin')

def enquiry_form(request,id):
    if request.method == 'POST' and is_admin(request):
        if request.user.is_authenticated and is_admin(request):
            if request.user.groups.filter(name='user_admin').exists():
                note = request.POST['note']
                enquiry = Enquiry.objects.filter(request_id=id).get()
                enquiry.note = note
                enquiry.save()
                return redirect('admin-enquiry')
            else:return redirect('auth_user')
    return render(request, 'user_admin/enquiry-form.html',{'enquiry':Enquiry.objects.filter(request_id=id).get()})

def plumber_requests(request):
    if request.user.is_authenticated:
        if is_admin(request):
            return render(request, 'user_admin/plumber-requests.html',{'requests':PlumberRequest.objects.all()})
        else:
            return redirect('auth_user')
    else:
        return redirect('signin')
    
def plumber_request(request,id):
    if request.user.is_authenticated and is_admin(request):
        if request.method == 'POST':
            note = request.POST['note']
            req = PlumberRequest.objects.filter(request_id=id).get()
            req.note = note
            req.save()
            return redirect('admin-plumber-requests')
        return render(request, 'user_admin/plumber-request.html',{'request':PlumberRequest.objects.filter(request_id=id).get()})
    else:return redirect('auth_user')

def delete_plumber_request(request,id):
    PlumberRequest.objects.filter(request_id=id).delete()
    return redirect('admin-plumber-requests')

def delete_enquiry(request,id):
    Enquiry.objects.filter(request_id=id).delete()
    return redirect('admin-enquiry')

def dashboard(request):
    if request.user.is_authenticated and is_admin(request):
        if request.user.groups.filter(name='user_admin').exists():
            return render(request,'user_admin/index.html')
        else:return redirect('auth_user')
    else:return redirect('signin')

def create_main_category(request):
    import re
    if request.user.is_authenticated and is_admin(request):
        if request.method == 'POST' and is_admin(request):
            category_name = str(request.POST['category_name']).lower()
            category_descripiton = str(request.POST['category_name']).lower()
            category_image = base64.b64encode(request.FILES['category_image'].read()).decode('utf-8')
            cat_id = str(category_name).strip()+str(datetime.datetime.now())
            for j in cat_id:
                if j.isalnum()==False and j!='-':
                    cat_id = cat_id.replace(j,'-')
            
            cat_id = re.sub(r'-+', '-', cat_id)
            category = MainCategory(cat_id=cat_id,name=category_name, description=category_descripiton, image=category_image)
            category.save()
            return redirect('admin-view-products')
        else:
            return render(request, 'user_admin/create_main_category.html')
    else:
        return redirect('signin')

def create_sub_category(request):
    import re
    if request.user.is_authenticated and is_admin(request):
        if request.method == 'POST' and is_admin(request):
            main_category = request.POST['main_category']
            category = str(request.POST['category_name']).lower()
            category_description = str(request.POST['category_description']).lower()
            category_image = base64.b64encode(request.FILES['category_image'].read()).decode('utf-8')
            cat_id = str(category).strip()+str(datetime.datetime.now())
            for j in cat_id:
                if j.isalnum()==False and j!='-':
                    cat_id = cat_id.replace(j,'-')
            
            cat_id = re.sub(r'-+', '-', cat_id)
            category = SubCategory(cat_id=cat_id, main_category=main_category ,name=category, description=category_description, image=category_image)
            category.save()
            return redirect('admin-main-category')
        else:
            return render(request, 'user_admin/create_sub_category.html',{'main_categories':MainCategory.objects.all()})
    else:
        return redirect('signin')

def edit_main_category(request,name):
    if request.method == 'POST':
        category = MainCategory.objects.get(name=name)
        name = request.POST['name']
        description = request.POST['description']
        if 'image' in request.FILES:category.image = base64.b64encode(request.FILES['image'].read()).decode('utf-8')
        else:category.image = MainCategory.objects.get(name=name).image
        category.name = name
        category.description = description
        category.save()
        return redirect('/user-admin/main-category')
    return render(request, 'user_admin/edit-main-category.html',{'category':MainCategory.objects.get(name=name)})

def edit_sub_category(request,name):
    if request.method == 'POST':
        category = SubCategory.objects.get(name=name)
        # category.name = request.POST['name']
        category.main_category = MainCategory.objects.get(name=request.POST['main_category'])
        category.description = request.POST['description']

        if 'image' in request.FILES:category.image = base64.b64encode(request.FILES['image'].read()).decode('utf-8')
        else:category.image = SubCategory.objects.get(name=name).image
        category.save()
        
        SubCategory.objects.get(name=name).name = request.POST['name']
        
        return redirect('/user-admin/main-category')
    return render(request, 'user_admin/edit-sub-category.html',{'category':SubCategory.objects.get(name=name), 'main_categories':MainCategory.objects.all()})

def delete_main_category(request,name):
    MainCategory.objects.filter(name=name).delete()
    return redirect('/user-admin/main-category')

def delete_sub_category(request,name):
    SubCategory.objects.filter(name=name).delete()
    return redirect('/user-admin/main-category')

def main_category(request):
    trending_products = Product.objects.filter(trending=True)[:4]
    return render(request, 'user_admin/main-category.html',{'trending_products':trending_products,'main_categories':MainCategory.objects.all()})

def sub_category(request,name):
    return render(request, 'user_admin/sub-category.html',{
        'main_category':MainCategory.objects.filter(name=name).get(),
        'sub_categories':SubCategory.objects.filter(main_category=name),
        'related_products':Product.objects.filter(main_category=name)[:4],
    })

def trending_products(request):
    trending_products = Product.objects.filter(trending=True)
    return render(request, 'user_admin/viewproducts.html',{'products':trending_products})

def gallery_products(request):
    gallery_products = Product.objects.filter(gallery_view=True)
    return render(request, 'user_admin/viewproducts.html',{'products':gallery_products})

def create_product(request):
    if request.user.is_authenticated and is_admin(request):
        if request.method == 'POST' and is_admin(request) and request.user.groups.filter(name='user_admin').exists():
            name = request.POST['pro_name']
            price = request.POST['pro_price']
            pro_price_per_user = request.POST['pro_price_per_user']
            pro_price_plumber = request.POST['pro_price_plumber']
            pro_price_prime = request.POST['pro_price_prime']
            description = request.POST['pro_description']
            code = request.POST['pro_code']
            series = request.POST['pro_series']
            features = request.POST['pro_features']
            main_category = request.POST['pro_main_category']
            sub_category = request.POST['pro_sub_category']
            try:
                if request.POST['pro_trending']=='on':trending = True
            except:trending = False
            try:
                if request.POST['pro_gallery_view']=='on':gallery_view = True
            except:gallery_view = False
                
            img = base64.b64encode(request.FILES['pro_image'].read()).decode('utf-8')            

            product = Product(
                product_id=generate_product_id(code=code,name=name,series=series),
                pro_code=code,
                pro_name=name,
                pro_price=price,
                pro_price_per_user=pro_price_per_user,
                pro_price_plumber=pro_price_plumber,
                pro_price_prime=pro_price_prime,
                pro_description=description,
                pro_image=img,
                pro_series = series,
                pro_features=features,
                main_category=main_category,
                sub_category=sub_category,
                trending=trending,
                gallery_view=gallery_view,
            )
            product.save()
            return redirect('admin-view-products')
        else:
            return render(request, 'user_admin/createproduct.html',{'main_categories':MainCategory.objects.all(),'sub_categories':SubCategory.objects.all()})
    else:
        return redirect('signin')

def edit_product(request,id):
    if request.user.is_authenticated and is_admin(request):
        if request.method == 'POST' and is_admin(request):
            product = Product.objects.get(product_id=id)
            
            product.pro_name = request.POST['pro_name']
            product.pro_code = request.POST['pro_code']
            product.pro_series = request.POST['pro_series']
            product.pro_price = request.POST['pro_price']
            product.pro_price_per_user = request.POST['pro_price_per_user']
            product.pro_price_prime = request.POST['pro_price_prime']
            product.pro_price_plumber = request.POST['pro_price_plumber']
            product.pro_description = request.POST['pro_description']
            product.pro_features = request.POST['pro_features']
            product.main_category = request.POST['pro_main_category']
            product.sub_category = request.POST['pro_sub_category']
            try:
                if request.POST['pro_trending']=='on':product.trending = True
            except:product.trending = False
            try:
                if request.POST['pro_gallery_view']=='on':product.gallery_view = True
            except:product.gallery_view = False
                
            if 'pro_image' in request.FILES:product.pro_image = base64.b64encode(request.FILES['pro_image'].read()).decode('utf-8')
            else:product.pro_image = Product.objects.get(product_id=id).pro_image
            product.gallery_view = False
            product.trending = False
            product.save()
            return redirect('admin-product-detail',id)
        
        product = Product.objects.get(product_id=id)
        return render(request, 'user_admin/editproduct.html',{
            'product': product,
            'main_categories':MainCategory.objects.all(),
            'sub_categories':SubCategory.objects.all(),
            'tren':product.trending
        })
    else:
        return redirect('signin')

def delete_product(request,id):
    if request.user.is_authenticated and is_admin(request):
        product = Product.objects.filter(product_id=id).delete()
        return redirect('admin-view-products')
    else:
        return redirect('signin')

def products(request,category):
    if request.user.is_authenticated and is_admin(request):
        products = []
        for i in Product.objects.filter(sub_category=str(category).lower()).all():
            products.append(i)
        if len(products)==0:
            for i in Product.objects.filter(main_category=str(category).lower()).all():
                products.append(i)
          
        return render(request, 'user_admin/viewproducts.html', {'products': products,'main_categories':MainCategory.objects.all()})
    else:
        return redirect('signin')

def product_detail(request,id):
    if request.method == 'POST' and is_admin(request):
        if request.user.is_authenticated and is_admin(request):
            if request.user.groups.filter(name='user_admin').exists():
                user_name = request.POST.get('user_name')
                user_contact = str(request.POST.get('user_contact')).strip()
                user_city = str(request.POST.get('user_city')).strip()
                user_state = str(request.POST.get('user_state')).strip()
                user_message = str(request.POST.get('user_message')).strip()
                enquiry = {
                    'request_id': remove_spcl_ch([datetime.datetime.now(),user_name,user_contact,user_city,user_state]),
                    'user_name': user_name,
                    'user_contact': user_contact,
                    'product_name':Product.objects.filter(product_id=id).get().pro_name,
                    'product_code':Product.objects.filter(product_id=id).get().pro_code,
                    'user_city': user_city,
                    'user_state': user_state,
                    'user_message': user_message,
                }
                Enquiry.objects.create(**enquiry)
                return redirect('admin-product-detail',id)
            else:return redirect('auth_user')
        else:return redirect('signin')
    product = Product.objects.filter(product_id=id).get()
    features = product.pro_features.split('\n')
    for j in range(len(features)):
        features[j] = features[j].strip()
    product.pro_features = features
    return render(request, 'user_admin/product-details.html',{'product': product})

def view_products(request):
    if request.user.is_authenticated and is_admin(request):
        products = Product.objects.all()
        return render(request, 'user_admin/viewproducts.html', {'products': products,'main_categories':MainCategory.objects.all()})
    else:
        return redirect('signin')

def clients(request):
    if request.user.is_authenticated and is_admin(request):
        inactive_clients = {}
        for i in User.objects.all():
            if i.is_active==False and i.is_superuser==False and i.is_staff==False:
                inactive_clients[i] = i
        
        active_clients = {}
        for i in User.objects.all():
            if i.is_active==True and i.is_superuser==False and i.is_staff==False:
                active_clients[i] = i
        
        return render(request, 'user_admin/clients.html',{'inactive_clients': inactive_clients, 'active_clients': active_clients})
    else:
        return redirect('signin')

def approve_user(request,email):
    if request.user.is_authenticated and is_admin(request):
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return redirect('clients')
    else:
        return redirect('signin')

def revoke_user(request,email):
    if request.user.is_authenticated and is_admin(request):
        user = User.objects.get(email=email)
        user.is_active = False
        user.save()
        return redirect('clients')
    else:
        return redirect('signin')

def remove_user(request,email):
    if request.user.is_authenticated and is_admin(request):
        user = User.objects.get(email=email)
        user.delete()
        return redirect('clients')
    else:
        return redirect('signin')

def profile(request):
    if request.user.is_authenticated and is_admin(request):
        return render(request, 'user_admin/profile.html', {'user': request.user,'role':get_role_name(request)})
    else:
        return redirect('signin')

def edit_profile(request):
    if request.method == 'POST' and is_admin(request):
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
        return render(request, 'user_admin/editprofile.html', {'message':'Profile Updated Successfully','user': request.user})
    return render(request, 'user_admin/editprofile.html', {'user': request.user})
