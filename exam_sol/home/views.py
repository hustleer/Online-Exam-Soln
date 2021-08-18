import json
from django.core.paginator import Paginator
from itertools import chain , islice
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from django.contrib.auth import authenticate , login
from order.models import ShopCart , Wishlist
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from user.forms import SignUpForm
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage, FAQ , News , Banner
from mysite import settings
from product.models import Category, Product, Images,Brand, Comment, Variants , Color , Size
from user.models import UserProfile 


def index(request):
    request.session['discount'] = 0 
    if 'signin' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                request.session.set_expiry(30000000000)

                current_user = request.user
                messages.success(request , "Welcome! Login successful")
                return HttpResponseRedirect(url)
            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm()

    setting = Setting.objects.get(pk=1)
    banner = Banner.objects.all()
    products_latest = Product.objects.all().order_by('-id')[:8]  # last 4 products
    pages = False

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    wishlist = Wishlist.objects.filter(user_id = current_user.id)
    # products_slider = Product.objects.all().order_by('id')[:8]  #first 4 products
    products_all = Product.objects.all().order_by('?')[:12]  #first 4 products
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    category = Category.objects.all()
    cat = Category.objects.all().get_descendants(include_self=False)
    new_cat = []
    for rs in cat:
        if rs.level != 0 :
            new_cat.append(rs) 

    random.shuffle(new_cat)
    new_category = list(new_cat)
    new_category = new_category[:12]  
    products_picked = Category.objects.filter( level = 1 ).order_by('?')[:24]   #Random selected 4 products
    products_rated = Product.objects.all()  #Random selected 4 products
    products_rated =  sorted(products_rated, key=lambda product: -product.avaregereview() ) 
    products_rated =  products_rated[:12]
    request.session['discount']= 0 

    context={'setting':setting,
             'new_category':new_category,
             'wishlist':wishlist,
             'banner':banner,
             'shopcart':shopcart,
             'pages':pages,
            #  'category':category,
             'total':total,
             'form':form,
             'products_all': products_all,
             'products_picked': products_picked,
             'products_rated': products_rated,
             #'category':category
             }
    return render(request,'index.html',context)


def aboutus(request):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                request.session.set_expiry(30000000000)
                current_user = request.user
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)
    total = 0
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    banner = Banner.objects.all()
    context={'setting':setting ,'form':form ,'banner':banner  ,'total':total  ,'shopcart':shopcart }
    return render(request, 'about.html', context)

def contactus(request):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                request.session.set_expiry(30000000000)
                current_user = request.user
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm(request.POST or None)
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    banner = Banner.objects.all()

    if request.method == 'POST': # check post
        formz = ContactForm(request.POST)
        if formz.is_valid():
            data = ContactMessage() #create relation with model
            data.name = formz.cleaned_data['name'] # get form input data
            data.email = formz.cleaned_data['email']
            data.subject = formz.cleaned_data['subject']
            data.message = formz.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    category = Category.objects.all()
    formz = ContactForm
    current_user = request.user
    setting = Setting.objects.get(pk = 1 )
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    wishlist = Wishlist.objects.filter(user_id = current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    context={'setting':setting,'formz':formz ,'banner':banner ,'total':total ,'wishlist':wishlist ,'shopcart':shopcart ,'form':form ,'category':category  }
    return render(request, 'contactus.html', context)




def category_products(request , id , slug , color_data , price_data , brand_data , rate_data ):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                request.session.set_expiry(30000000000)
                current_user = request.user
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm()
    catid = id
    catt = Category.objects.get(id = catid)
    is_leaf = catt.level
    catidd = []
    products = Product.objects.none()
    if is_leaf == 0: 
        childs = catt.get_descendants()
        for rs in childs:
            temp = Product.objects.filter(category_id = rs.id)
            products = list(chain(products , temp))
            catidd.append(rs.id)
    else:
        catidd.append(catid)
        products = Product.objects.filter(category_id = catid)

    catdata = Category.objects.get(id = catid) 
    for catid in catidd:
        request.session['sel_size'] = 0

        price_datas = int(price_data)
        form = SignUpForm()
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        current_user = request.user
        sizes = Size.objects.all()
        shopcart = ShopCart.objects.filter(user_id = current_user.id )

        total = 0
        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity

        #color filter
        products1 = Product.objects.none()
        
        if color_data == 0:
            col_latest = Variants.objects.all() 
            for rs in col_latest:
                temp = Product.objects.filter(id=rs.product_id,status="True" )
                products1 = list(chain(products1 , temp))
        else:
            col_latest = Variants.objects.filter( color_id = color_data  )
            for rs in col_latest:
                temp = Product.objects.filter(id=rs.product.id  ,status="True")
                products1 = list(chain(products1 , temp))
        products = set(products1).intersection(set(products))


        #size filter    
        
        selected_size = []
        if 'size_array' in request.POST:
            sel_size = request.POST.getlist('size')
            request.session['sel_size'] = sel_size
        
            if sel_size:
                for i in sel_size:
                    selected_size.append(int(i)) 
            else :
                selected_size.append(0)  
        else :
            sel_size = request.session.get('sel_size')

            if sel_size:
                for i in sel_size:
                    selected_size.append(int(i)) 
            else :
                selected_size.append(0) 

        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if selected_size[0] == 0 :
            col_latest = Variants.objects.all() 
            for rs in col_latest:
                temp = Product.objects.filter(id=rs.product_id,status="True" )
                products1 = list(chain(products1 , temp))
        else:
            for size_datas in selected_size:
                col_latest = Variants.objects.filter( size_id = size_datas)
                for rs in col_latest:
                    temp = Product.objects.filter(id=rs.product.id  ,status="True")
                    products1 = list(chain(products1 , temp))

        products = set(products).intersection(set(products1))


        #brand filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if brand_data == 0:
            products1 = Product.objects.filter(status="True") 
        else:
            products1 = Product.objects.filter( brand_id = brand_data)

        products = set(products1).intersection(set(products))
        #rating  filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if rate_data == 0:
            products1 = Product.objects.filter(status="True") 
        else:
            products11 = Product.objects.filter( status="True") 
            for rs in products11:
                if rs.avaregereview() >= rate_data:
                    temp = Product.objects.filter(id = rs.id)
                    products1 = list(chain(temp , products1))


        products = set(products1).intersection(set(products)) 
        #price  filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if price_data == 0:
            products1 = Product.objects.filter(status="True") 
        else:
            products11 = Product.objects.filter( status="True") 
            for rs in products11:
                if rs.price <= price_data:
                    temp = Product.objects.filter(id = rs.id)
                    products1 = list(chain(temp , products1))


        products = set(products1).intersection(set(products))
        # productz = Product.objects.none()
        # for product in products:
        #     temp = Product.objects.filter(id = product.id)
        #     productz = productz.union(temp)
        # products = productz.objects.all().order_by('id')
    sort_value = ""
    if 'sortby' in request.POST:
        sort_by = request.POST.get('sortby')
        sort_value = sort_by
        if sort_by == 'latest':
            products =  sorted(products, key=lambda product: -product.id )  
        if sort_by == 'rating':
            products =  sorted(products, key=lambda product: -product.countreview() )  

        if sort_by == 'bestrating':
            products =  sorted(products, key=lambda product: -product.avaregereview() )  
        if sort_by == 'increasing':
            products =  sorted(products, key=lambda product: product.price )  
        if sort_by == 'decreasing':
            products =  sorted(products, key=lambda product: -product.price )  
        if sort_by == 'date':
            products =  sorted(products, key=lambda product: product.create_at )  

    #selected_price
    catidd = []
    product_list = Product.objects.none()
    if is_leaf == 0: 
        childs = catt.get_descendants()
        for rs in childs:
            temp = Product.objects.filter(category_id = rs.id)
            product_list = list(chain(product_list , temp))
            catidd.append(rs.id)
    else:
        catidd.append(catid)
        product_list = Product.objects.filter(category_id = catid)
    # product_list = Product.objects.filter(category_id = catid)
    min_price = 1000000
    max_price = 0 
    for rs in product_list : 
        if rs.variant == 'None':
            if rs.price > max_price:
                max_price = rs.price
            if rs.price < min_price:
                min_price = rs.price
        else:
            variants = Variants.objects.filter(product_id = rs.id)
            for rss in variants:
                if rss.price > max_price:
                    max_price = rss.price
                if rss.price < min_price:
                    min_price = rss.price
    price1 = int(min_price)
    price2 = int((max_price - min_price)/5) * 1 + int(min_price)
    price3 = int((max_price - min_price)/5) * 2 + int(min_price)
    price4 = int((max_price - min_price)/5) * 3 + int(min_price)
    price5 = int((max_price - min_price)/5) * 4 + int(min_price)
    price6 = int(max_price)

        
    #selected color 
    res = Color.objects.none()
    productz = Product.objects.filter(category_id = catid)
    for  productz in products:
        variants = Variants.objects.filter(product_id = productz.id)
        for vs in variants:
            if vs.color:
                temp = vs.color.id
                temp_color = Color.objects.filter(id = temp)
                res = list(chain(res , temp_color)) 
    colorz = [] 
    for i in res: 
        if i not in colorz: 
            colorz.append(i)

    #selected rate 
    rating = [5,4,3,2,0] 


    #selected size 
    res = Size.objects.none()
    productz = Product.objects.filter(category_id = catid)
    for  product in productz:
        variants = Variants.objects.filter(product_id = product.id)
        if variants[0].size is not None:
            for vs in variants:
                temp = vs.size.id
                temp_size = Size.objects.filter(id = temp)
                res = list(chain(res , temp_size))
    sizes = [] 
    for i in res: 
        if i not in sizes: 
            sizes.append(i)
    #selected brand
    brands = Brand.objects.filter(category_id = catid)

        
    paginator = Paginator(list(products)  , 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    pages =  False
    context = {'products': products,
                'color_data':color_data,
                'price_datas':price_datas,
                'price1':price1,
                'price2':price2,
                'price3':price3,
                'is_leaf':is_leaf,
                'price4':price4,
                'price5':price5,
                'price6':price6,
                'sort_value':sort_value,
                'form':form,

                'slug':slug,
                'rating':rating,
                'setting':setting,
                'total':total,
                'selected_size':selected_size,
                'brand_data':brand_data,
                'rate_data':rate_data,
                'catid':catid,
                'catidd':catidd,
                'brands':brands,
                'sizes':sizes,
                'catdata':catdata,
                'colorz':colorz,
                'category': category
                }
    return render(request , 'category_products.html' , context)      






def search(request , id , query , color_data , price_data , brand_data , rate_data ):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                request.session.set_expiry(30000000000)
                current_user = request.user
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm()
    color_data = color_data 
    brand_data = brand_data 
    rate_data = rate_data
    price_data = price_data
    if 'search' in request.POST:
        formz = SearchForm(request.POST)
        if formz.is_valid():
            request.session['sel_size'] = 0

            query = formz.cleaned_data['query'] # get form input data
            request.session['query'] = query
            catid = formz.cleaned_data['catid']
            request.session['catid'] = catid
            if catid==0:
                products=Product.objects.filter(keywords__icontains=query  )  #SELECT * FROM product WHERE title LIKE '%query%'
            #selected_price
                product_list = Product.objects.filter(keywords__icontains=query )
                min_price = 1000000
                max_price = 0 
                for rs in product_list : 
                    if rs.variant == 'None':
                        if rs.price > max_price:
                            max_price = rs.price
                        if rs.price < min_price:
                            min_price = rs.price
                    else:
                        variants = Variants.objects.filter(product_id = rs.id)
                        for rss in variants:
                            if rss.price > max_price:
                                max_price = rss.price
                            if rss.price < min_price:
                                min_price = rss.price
                price1 = int(min_price)
                price2 = int((max_price - min_price)/5) * 1 + int(min_price)
                price3 = int((max_price - min_price)/5) * 2 + int(min_price)
                price4 = int((max_price - min_price)/5) * 3 + int(min_price)
                price5 = int((max_price - min_price)/5) * 4 + int(min_price)
                price6 = int(max_price)
            
                    
            #selected color 
                res = Color.objects.none()
                productz = Product.objects.filter(keywords__icontains=query )
                for  productz in products:
                    variants = Variants.objects.filter(product_id = productz.id)
                    for vs in variants:
                        if vs.color:
                            temp = vs.color.id
                            temp_color = Color.objects.filter(id = temp)
                            res = list(chain(res , temp_color)) 
                colorz = [] 
                for i in res: 
                    if i not in colorz: 
                        colorz.append(i)

            #selected rate 
                rating = [5,4,3,2,0] 


            #selected size 
                res = Size.objects.none()
                productz = Product.objects.filter(keywords__icontains=query )
                for  product in productz:
                    variants = Variants.objects.filter(product_id = product.id)
                    if variants[0].size is not None:
                        for vs in variants:
                            temp = vs.size.id
                            temp_size = Size.objects.filter(id = temp)
                            res = list(chain(res , temp_size))
                sizes = [] 
                for i in res: 
                    if i not in sizes: 
                        sizes.append(i)
                sizes = list( dict.fromkeys(sizes) ) 

            #selected brand
                brands = Brand.objects.none()
                for rs in products:
                    temp = Brand.objects.filter( id = rs.brand.id)
                    brands = list(chain(brands , temp ))
                brands = list( dict.fromkeys(brands) )

                category = Category.objects.all()
                setting = Setting.objects.get(pk=1)
                current_user = request.user
                shopcart = ShopCart.objects.filter(user_id  = current_user.id)
                total = 0
                for rs in shopcart:
                    if rs.product.variant == 'None':
                        total += rs.product.price * rs.quantity
                    else:
                        total += rs.variant.price * rs.quantity
                pages =  False
                price_datas = 0 
                paginator = Paginator(list(products)  , 12)
                page = request.GET.get('page')
                products = paginator.get_page(page)    
                brand_data = 0 
                color_data = 0 
                rate_data  = 0 
                context = { 'products': products,
                            'rate_data':rate_data,
                            'pages':pages,
                            'price_data':price_data,
                            'color_data':color_data,
                            'brand_data':brand_data,
                            'price1':price1,
                            'price2':price2,
                            'price3':price3,
                            'price4':price4,
                            'price5':price5,
                            'price6':price6,
                            'form':form,

                            'query':query,
                            'catid':catid,
                            'rating':rating,
                            'setting':setting,
                            'total':total,
                            'catid':catid,
                            'brands':brands,
                            'sizes':sizes,
                            'colorz':colorz,
                            'category': category,
                            }
                return render(request, 'search_products.html', context)
            else:
                products = Product.objects.filter(keywords__icontains=query ,category_id=catid)

            #selected_price
                product_list = Product.objects.filter(keywords__icontains=query ,category_id=catid)
                min_price = 1000000
                max_price = 0 
                for rs in product_list : 
                    if rs.variant == 'None':
                        if rs.price > max_price:
                            max_price = rs.price
                        if rs.price < min_price:
                            min_price = rs.price
                    else:
                        variants = Variants.objects.filter(product_id = rs.id)
                        for rss in variants:
                            if rss.price > max_price:
                                max_price = rss.price
                            if rss.price < min_price:
                                min_price = rss.price
                price1 = int(min_price)
                price2 = int((max_price - min_price)/5) * 1 + int(min_price)
                price3 = int((max_price - min_price)/5) * 2 + int(min_price)
                price4 = int((max_price - min_price)/5) * 3 + int(min_price)
                price5 = int((max_price - min_price)/5) * 4 + int(min_price)
                price6 = int(max_price)
            
                    
            #selected color 
                res = Color.objects.none()
                productz = Product.objects.filter(keywords__icontains=query ,category_id=catid)
                for  productz in products:
                    variants = Variants.objects.filter(product_id = productz.id)
                    for vs in variants:
                        if vs.color:
                            temp = vs.color.id
                            temp_color = Color.objects.filter(id = temp)
                            res = list(chain(res , temp_color)) 
                colorz = [] 
                for i in res: 
                    if i not in colorz: 
                        colorz.append(i)

            #selected rate 
                rating = [5,4,3,2,0] 


            #selected size 
                res = Size.objects.none()
                productz = Product.objects.filter(keywords__icontains=query ,category_id=catid)
                for  product in productz:
                    variants = Variants.objects.filter(product_id = product.id)
                    if variants[0].size is not None:
                        for vs in variants:
                            temp = vs.size.id
                            temp_size = Size.objects.filter(id = temp)
                            res = list(chain(res , temp_size))
                sizes = [] 
                for i in res: 
                    if i not in sizes: 
                        sizes.append(i)
                sizes = list( dict.fromkeys(sizes) ) 

            #selected brand
                brands = Brand.objects.none()
                for rs in products:
                    temp = Brand.objects.filter( id = rs.brand.id)
                    brands = list(chain(brands , temp ))
                brands = list( dict.fromkeys(brands) )


                category = Category.objects.all()
                setting = Setting.objects.get(pk=1)
                current_user = request.user
                shopcart = ShopCart.objects.filter(user_id  = current_user.id)
                total = 0
                for rs in shopcart:
                    if rs.product.variant == 'None':
                        total += rs.product.price * rs.quantity
                    else:
                        total += rs.variant.price * rs.quantity
                pages =  False
                price_datas = 0 


                paginator = Paginator(list(products)  , 12)
                page = request.GET.get('page')
                products = paginator.get_page(page)             
                brand_data = 0 
                color_data = 0 
                rate_data  = 0 
                context = { 'products': products,
                            'rate_data':rate_data,
                            'pages':pages,
                            'price_data':price_data,
                            'color_data':color_data,
                            'brand_data':brand_data,
                            'price1':price1,
                            'price2':price2,
                            'price3':price3,
                            'price4':price4,
                            'price5':price5,
                            'price6':price6,
                            'form':form,

                            'query':query,
                            'catid':catid,
                            'rating':rating,
                            'setting':setting,
                            'total':total,
                            'catid':catid,
                            'brands':brands,
                            'sizes':sizes,
                            'colorz':colorz,
                            'category': category,
                            }
                return render(request, 'search_products.html', context)
        return HttpResponseRedirect('/')
    else:
        query = request.session.get('query')
        id = request.session.get('catid')

        products1 = Product.objects.none()
        products = Product.objects.all()
        if id == 0:
            products = Product.objects.filter(keywords__icontains=query )
        else:
            products = Product.objects.filter(keywords__icontains=query ,category_id=id)
            
        if color_data == 0:
            col_latest = Variants.objects.all() 
            for rs in col_latest:
                if id == 0 :
                    temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query  )
                    products1 = list(chain(products1 , temp))
                else:
                    temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query ,category_id=id )
                    products1 = list(chain(products1 , temp))

        else:
            col_latest = Variants.objects.filter( color_id = color_data  )
            for rs in col_latest:
                if id == 0 :
                    temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query  )
                    products1 = list(chain(products1 , temp))
                else:
                    temp = Product.objects.filter(id=rs.product_id,status="True" ,keywords__icontains=query ,category_id=id )
                    products1 = list(chain(products1 , temp))

        products = set(products1).intersection(set(products))


            #size filter    
        
        selected_size = []
        if 'size_array' in request.POST:
            sel_size = request.POST.getlist('size')
            request.session['sel_size'] = sel_size
       
            if sel_size:
                for i in sel_size:
                    selected_size.append(int(i)) 
            else :
                selected_size.append(0)  
        else :
            sel_size = request.session.get('sel_size')

            if sel_size:
                for i in sel_size:
                    selected_size.append(int(i)) 
            else :
                selected_size.append(0)  
 

        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if selected_size[0] == 0 :
            col_latest = Variants.objects.all() 
            for rs in col_latest:
                if id == 0 :
                    temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query  )
                    products1 = list(chain(products1 , temp))
                else:
                    temp = Product.objects.filter(id=rs.product_id,status="True" ,keywords__icontains=query ,category_id=id )
                    products1 = list(chain(products1 , temp))

        else:
            for size_datas in selected_size:
                col_latest = Variants.objects.filter( size_id = size_datas)
                for rs in col_latest:
                    if id == 0 :
                        temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query  )
                        products1 = list(chain(products1 , temp))
                    else:
                        temp = Product.objects.filter(id=rs.product_id,status="True" , keywords__icontains=query ,category_id=id )
                        products1 = list(chain(products1 , temp))


        products = set(products).intersection(set(products1))


            #brand filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if brand_data == 0:
            if id == 0 :
                products1 = Product.objects.filter(status="True" ,keywords__icontains=query )
            else:
                products1 = Product.objects.filter(status="True" ,keywords__icontains=query ,category_id=id )
        else:
            if id == 0 :
                products1 = Product.objects.filter(brand_id=brand_data,status="True" ,keywords__icontains=query  )
            else:
                products1 = Product.objects.filter(brand_id=brand_data,status="True" , keywords__icontains=query ,category_id=id )

        products = set(products1).intersection(set(products))
        #rating  filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if rate_data == 0:
            products1 = Product.objects.filter(status="True") 
        else:
            products11 = Product.objects.filter( status="True") 
            for rs in products11:
                if rs.avaregereview() >= rate_data:
                    temp = Product.objects.filter(id = rs.id)
                    products1 = list(chain(temp , products1))


        products = set(products1).intersection(set(products)) 
        #price  filter
        products1 = Product.objects.none()
        # products = Product.objects.filter(category_id = catid)
        if price_data == 0:
            products1 = Product.objects.filter(status="True") 
        else:
            products11 = Product.objects.filter( status="True") 
            for rs in products11:
                if rs.price <= price_data:
                    temp = Product.objects.filter(id = rs.id)
                    products1 = list(chain(temp , products1))


        products = set(products1).intersection(set(products))
        # productz = Product.objects.none()
        # for product in products:
        #     temp = Product.objects.filter(id = product.id)
        #     productz = productz.union(temp)
        # products = productz.objects.all().order_by('id')
        sort_value = ""
        if 'sortby' in request.POST:
            sort_by = request.POST.get('sortby')
            sort_value = sort_by
            if sort_by == 'latest':
                products =  sorted(products, key=lambda product: -product.id )  
            if sort_by == 'rating':
                products =  sorted(products, key=lambda product: -product.countreview() )  

            if sort_by == 'bestrating':
                products =  sorted(products, key=lambda product: -product.avaregereview() )  
            if sort_by == 'increasing':
                products =  sorted(products, key=lambda product: product.price )  
            if sort_by == 'decreasing':
                products =  sorted(products, key=lambda product: -product.price )  
            if sort_by == 'date':
                products =  sorted(products, key=lambda product: product.create_at )  

        #selected_price
        product_list = Product.objects.all()
        if id == 0 :
            product_list = Product.objects.filter(status="True" , keywords__icontains=query  )
        else:
            product_list = Product.objects.filter(status="True" ,keywords__icontains=query ,category_id=id )

        min_price = 1000000
        max_price = 0 
        for rs in product_list : 
            if rs.variant == 'None':
                if rs.price > max_price:
                    max_price = rs.price
                if rs.price < min_price:
                    min_price = rs.price
            else:
                variants = Variants.objects.filter(product_id = rs.id)
                for rss in variants:
                    if rss.price > max_price:
                        max_price = rss.price
                    if rss.price < min_price:
                        min_price = rss.price
        price1 = int(min_price)
        price2 = int((max_price - min_price)/5) * 1 + int(min_price)
        price3 = int((max_price - min_price)/5) * 2 + int(min_price)
        price4 = int((max_price - min_price)/5) * 3 + int(min_price)
        price5 = int((max_price - min_price)/5) * 4 + int(min_price)
        price6 = int(max_price)

            
        #selected color 
        res = Color.objects.none()
        productz = Product.objects.all()
        if id == 0 :
            productz = Product.objects.filter(status="True" , keywords__icontains=query  )
        else:
            productz = Product.objects.filter(status="True" ,keywords__icontains=query ,category_id=id )
        for  productz in products:
            variants = Variants.objects.filter(product_id = productz.id)
            for vs in variants:
                if vs.color:
                    temp = vs.color.id
                    temp_color = Color.objects.filter(id = temp)
                    res = list(chain(res , temp_color)) 
        colorz = [] 
        for i in res: 
            if i not in colorz: 
                colorz.append(i)

        #selected rate 
        rating = [5,4,3,2,0] 


        #selected size 
        res = Size.objects.none()
        if id == 0 :
            productz = Product.objects.filter(status="True" ,keywords__icontains=query )
        else:
            productz = Product.objects.filter(status="True" ,keywords__icontains=query ,category_id=id )
        for  product in productz:
            variants = Variants.objects.filter(product_id = product.id)
            if variants[0].size is not None:
                for vs in variants:
                    temp = vs.size.id
                    temp_size = Size.objects.filter(id = temp)
                    res = list(chain(res , temp_size))
        sizes = [] 
        for i in res: 
            if i not in sizes: 
                sizes.append(i)
        #selected brand
        brands = Brand.objects.none()
        temp_products = Product.objects.none()
        if id == 0 :
            temp_products = Product.objects.filter(status="True" , keywords__icontains=query )
        else:
            temp_products = Product.objects.filter(status="True" , keywords__icontains=query ,category_id=id)
        for rs in temp_products:
            temp = Brand.objects.filter( id = rs.brand.id)
            brands = list(chain(brands , temp ))
        brands = list( dict.fromkeys(brands))
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity

        pages =  False    
        paginator = Paginator(list(products)  , 12)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        setting = Setting.objects.get(pk = 1)
        pages =  False
        catid = id
        category = Category.objects.all()
        context = { 'products': products,
                    'price1':price1,
                    'price2':price2,
                    'pages':pages,
                    'price3':price3,
                    'price4':price4,
                    'price5':price5,
                    'price6':price6,
                    'sort_value':sort_value,
                    'color_data':color_data,
                    'price_data':price_data,
                    'brand_data':brand_data,
                    'selected_size':selected_size,
                    'form':form,

                    'query':query,
                    'rating':rating,
                    'setting':setting,
                    'total':total,
                    'rate_data':rate_data,
                    'catid':catid,
                    'brands':brands,
                    'sizes':sizes,
                    'colorz':colorz,
                    'category': category,
                    }
        return render(request , 'search_products.html' , context)      

    return HttpResponseRedirect('/')

def search_for_banner(request , id):
    ban = Banner.objects.get(id = id )
    request.session['query'] = ban.search_keywords
    return HttpResponseRedirect('/search/0/a/0/0/0/0') 



def search_id(request , id , query , color_data , price_data , brand_data , rate_data ):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            data = News()
            data.email =  request.POST['newsemail']
            data.save()
            messages.success(request , "Email added to Newsletter")
            return HttpResponseRedirect(url)
    products1 = Product.objects.none()
    products = Product.objects.all()
    if id == 0:
        products = Product.objects.filter(title__icontains=slug)
    else:
        products = Product.objects.filter(title__icontains=query,category_id=id)
        
    if color_data == 0:
        col_latest = Variants.objects.all() 
        for rs in col_latest:
            if id == 0 :
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug )
                products1 = list(chain(products1 , temp))
            else:
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug,category_id=id )
                products1 = list(chain(products1 , temp))

    else:
        col_latest = Variants.objects.filter( color_id = color_data  )
        for rs in col_latest:
            if id == 0 :
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug )
                products1 = list(chain(products1 , temp))
            else:
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug,category_id=id )
                products1 = list(chain(products1 , temp))

    products = set(products1).intersection(set(products))


    #size filter    

    selected_size = []
    if 'size_array' in request.POST:
        sel_size = request.POST.getlist('size')
        request.session['sel_size'] = sel_size
    
        if sel_size:
            for i in sel_size:
                selected_size.append(int(i)) 
        else :
            selected_size.append(0)  
    else :
        sel_size = request.session.get('sel_size')

        if sel_size:
            for i in sel_size:
                selected_size.append(int(i)) 
        else :
            selected_size.append(0)  

    products1 = Product.objects.none()
    # products = Product.objects.filter(category_id = catid)
    if selected_size[0] == 0 :
        col_latest = Variants.objects.all() 
        for rs in col_latest:
            if id == 0 :
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug )
                products1 = list(chain(products1 , temp))
            else:
                temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug,category_id=id )
                products1 = list(chain(products1 , temp))

    else:
        for size_datas in selected_size:
            col_latest = Variants.objects.filter( size_id = size_datas)
            for rs in col_latest:
                if id == 0 :
                    temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug )
                    products1 = list(chain(products1 , temp))
                else:
                    temp = Product.objects.filter(id=rs.product_id,status="True" , title__icontains=slug,category_id=id )
                    products1 = list(chain(products1 , temp))


    products = set(products).intersection(set(products1))


    #brand filter
    products1 = Product.objects.none()
    # products = Product.objects.filter(category_id = catid)
    if brand_data == 0:
        if id == 0 :
            products1 = Product.objects.filter(status="True" , title__icontains=slug )
        else:
            products1 = Product.objects.filter(status="True" , title__icontains=slug,category_id=id )
    else:
        products1 = Product.objects.filter(brand_id=brand_data,status="True" , title__icontains=slug,category_id=id )
    products = set(products1).intersection(set(products))
    #rating  filter
    products1 = Product.objects.none()
    # products = Product.objects.filter(category_id = catid)
    if rate_data == 0:
        products1 = Product.objects.filter(status="True") 
    else:
        products11 = Product.objects.filter( status="True") 
        for rs in products11:
            if rs.avaregereview() >= rate_data:
                temp = Product.objects.filter(id = rs.id)
                products1 = list(chain(temp , products1))


    products = set(products1).intersection(set(products)) 
    #price  filter
    products1 = Product.objects.none()
    # products = Product.objects.filter(category_id = catid)
    if price_data == 0:
        products1 = Product.objects.filter(status="True") 
    else:
        products11 = Product.objects.filter( status="True") 
        for rs in products11:
            if rs.price <= price_data:
                temp = Product.objects.filter(id = rs.id)
                products1 = list(chain(temp , products1))


    products = set(products1).intersection(set(products))
    # productz = Product.objects.none()
    # for product in products:
    #     temp = Product.objects.filter(id = product.id)
    #     productz = productz.union(temp)
    # products = productz.objects.all().order_by('id')
    sort_value = ""
    if 'sortby' in request.POST:
        sort_by = request.POST.get('sortby')
        sort_value = sort_by
        if sort_by == 'latest':
            products =  sorted(products, key=lambda product: -product.id )  
        if sort_by == 'rating':
            products =  sorted(products, key=lambda product: -product.countreview() )  

        if sort_by == 'bestrating':
            products =  sorted(products, key=lambda product: -product.avaregereview() )  
        if sort_by == 'increasing':
            products =  sorted(products, key=lambda product: product.price )  
        if sort_by == 'decreasing':
            products =  sorted(products, key=lambda product: -product.price )  
        if sort_by == 'date':
            products =  sorted(products, key=lambda product: product.create_at )  

    #selected_price
    product_list = Product.objects.all()
    if id == 0 :
        product_list = Product.objects.filter(status="True" , title__icontains=slug )
    else:
        product_list = Product.objects.filter(status="True" , title__icontains=slug,category_id=id )

    min_price = 1000000
    max_price = 0 
    for rs in product_list : 
        if rs.variant == 'None':
            if rs.price > max_price:
                max_price = rs.price
            if rs.price < min_price:
                min_price = rs.price
        else:
            variants = Variants.objects.filter(product_id = rs.id)
            for rss in variants:
                if rss.price > max_price:
                    max_price = rss.price
                if rss.price < min_price:
                    min_price = rss.price
    price1 = int(min_price)
    price2 = int((max_price - min_price)/5) * 1 + int(min_price)
    price3 = int((max_price - min_price)/5) * 2 + int(min_price)
    price4 = int((max_price - min_price)/5) * 3 + int(min_price)
    price5 = int((max_price - min_price)/5) * 4 + int(min_price)
    price6 = int(max_price)

        
    #selected color 
    res = Color.objects.none()
    productz = Product.objects.all()
    if id == 0 :
        productz = Product.objects.filter(status="True" , title__icontains=slug )
    else:
        productz = Product.objects.filter(status="True" , title__icontains=slug,category_id=id )
    for  productz in products:
        variants = Variants.objects.filter(product_id = productz.id)
        for vs in variants:
            if vs.color:
                temp = vs.color.id
                temp_color = Color.objects.filter(id = temp)
                res = list(chain(res , temp_color)) 
    colorz = [] 
    for i in res: 
        if i not in colorz: 
            colorz.append(i)

    #selected rate 
    rating = [5,4,3,2,0] 


    #selected size 
    res = Size.objects.none()
    if id == 0 :
        productz = Product.objects.filter(status="True" , title__icontains=slug )
    else:
        productz = Product.objects.filter(status="True" , title__icontains=slug,category_id=id )
    for  product in productz:
        variants = Variants.objects.filter(product_id = product.id)
        if variants[0].size is not None:
            for vs in variants:
                temp = vs.size.id
                temp_size = Size.objects.filter(id = temp)
                res = list(chain(res , temp_size))
    sizes = [] 
    for i in res: 
        if i not in sizes: 
            sizes.append(i)
    #selected brand
    brands = Brand.objects.none()
    for rs in products:
        temp = Brand.objects.filter( id = rs.brand.id)
        brands = list(chain(brands , temp ))
    brands = list( dict.fromkeys(brands))
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    pages =  False    
    paginator = Paginator(list(products)  , 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    setting = Setting.objects.get(pk = 1)
    pages =  False
    catid = id
    category = Category.objects.all()
    context = {'products': products,
                'price1':price1,
                'price2':price2,
                'price3':price3,
                'price4':price4,
                'price5':price5,
                'price6':price6,
                'sort_value':sort_value,

                'slug':slug,
                'rating':rating,
                'setting':setting,
                'total':total,
                'rate_data':rate_data,
                'catid':catid,
                'brands':brands,
                'sizes':sizes,
                'colorz':colorz,
                'category': category,
                }
    return render(request , 'search_products.html' , context)      





def search_auto(request):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            data = News()
            data.email =  request.POST['newsemail']
            data.save()
            messages.success(request , "Email added to Newsletter")
            return HttpResponseRedirect(url)
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title 
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def product_detail(request,id,slug):
    url = request.META.get('HTTP_REFERER')
    if 'news' in request.POST:
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                
                request.session.set_expiry(30000000000)
                current_user = request.user
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm()
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START


    category = Category.objects.all()

    product = Product.objects.get(pk=id)


    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end

    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')[:5]
    product_picked = Product.objects.filter(category_id = Product.objects.get(id = id).category.id ).order_by('?')[:4]
    current_user = request.user
    setting = Setting.objects.get(pk = 1 )
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    wishlist = Wishlist.objects.filter(user_id = current_user.id)


    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    banner = Banner.objects.all()
    context = {'product': product,'banner': banner,'setting': setting,'product_picked': product_picked,'category': category,
               'images': images, 'total': total,'form': form, 'comments': comments,'shopcart': shopcart,
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        product_picked = Product.objects.filter(category_id = Product.objects.get(id = id).category.id )[:4]
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity
        banner = Banner.objects.all()
        context.update({'sizes': sizes, 'banner': banner,'setting': setting,'colors': colors, 'wishlist': wishlist,'product_picked': product_picked,
                        'variant': variant,'url': url ,'form': form ,'total': total ,'query': query ,'shopcart': shopcart
                        })
    return render(request,'product_detail.html',context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxtest(request):
    data = {}
    current_user = request.user

    if request.POST.get('action') == 'post':
        productid = request.POST.get('productid')
        variantid = request.POST.get('variantid')
        quantity = request.POST.get('quantity')
        checkinproduct = ShopCart.objects.filter(product_id=productid) # Check product in shopcart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid)  # Check product in shopcart

        control = 0

        if checkinproduct and checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart
        if control==1: # Update  shopcart
            data = ShopCart.objects.filter(product_id= productid   , variant_id = variantid).first()
            data.quantity += int(quantity)
            data.save()  # save data
        else : # Inser to Shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = productid
            data.variant_id = variantid
            data.quantity = quantity
            data.save()
        # messages.success(request, "Product added to Shopcart edited")

        current_user = request.user
        user = current_user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity  
        context = { 
            'shopcart': shopcart,
            'total': total,
            'user': user,
   
        }
        data = {'rendered_table': render_to_string('ajatest.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def ajaxtestdelete(request):
    data = {}
    current_user = request.user

    if request.POST.get('action') == 'post':
        shopproductid = request.POST.get('cartproduct')
        ShopCart.objects.filter(id=shopproductid , user_id = current_user.id).delete()
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        user = current_user
        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity  
        context = { 
            'shopcart': shopcart,
            'total': total,
            'user': user,
   
        }
        data = {'rendered_table': render_to_string('ajatest.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxcartdelete1(request):
    data = {}
    current_user = request.user

    if request.POST.get('action') == 'post':
        shopproductid = request.POST.get('cartproduct')
        ShopCart.objects.filter(id=shopproductid , user_id = current_user.id).delete()
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        user = current_user

        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity  
        context = { 
            'shopcart': shopcart,
            'total': total,
            'user': user,
   
        }
        data = {'rendered_table': render_to_string('cartajax.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data) 



def ajaxcartupdate(request):
    data = {}
    current_user = request.user

    if request.POST.get('action') == 'post':
        shopproductid = request.POST.get('cartitemid')
        quantity = request.POST.get('quantity')
        s = ShopCart.objects.get(id=shopproductid , user_id = current_user.id)
        s.quantity = quantity
        s.save()
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        user = current_user

        for rs in shopcart:
            if rs.product.variant == 'None':
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity  
        context = { 
            'shopcart': shopcart, 
            'total': total,
            'user': user,
            "_token": "{{ csrf_token() }}",
   
        }
        data = {'rendered_table': render_to_string('cartajax.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data) 




def ajaxlistdelete(request):
    data = {}
    current_user = request.user

    if request.POST.get('action') == 'post':
        shopproductid = request.POST.get('listproduct')
        Wishlist.objects.filter(id=shopproductid  , user_id = current_user.id).delete()
        wishlist = Wishlist.objects.filter(user_id = current_user.id)
        user = current_user
        context = { 
            'wishlist': wishlist,
            'user': user,

    
        }
        data = {'rendered_table': render_to_string('ajaxwishlist.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def faq(request):
    if 'news' in request.POST:
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            all_emails = News.objects.all()
            flag = 0
            for rs in all_emails:
                if rs.email == request.POST['newsemail']:
                    flag = 1
        
               
            if flag == 1:
                messages.success(request , "Email already exists in Newsletter")
                return HttpResponseRedirect(url)
            else:
                data = News()
                data.email =  request.POST['newsemail']
                data.save()
                messages.success(request , "Email added to Newsletter")
                return HttpResponseRedirect(url)
                    
    if 'signin' in request.POST:

        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            username  = request.POST['username']
            password  = request.POST['password']
            user = authenticate(request , username = username , password = password)

            if user is not None:
                login(request , user)
                current_user = request.user
                request.session.set_expiry(30000000000)
                messages.success(request , "Welcome! Login successful")

                return HttpResponseRedirect(url)

            else:
                messages.warning(request , "Login error ! Please check username and password")
                return HttpResponseRedirect(url)


    # signup
    url = request.META.get('HTTP_REFERER')
    form = SignUpForm(request.POST or None)
    url = request.META.get('HTTP_REFERER')
    if 'signup' in request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            user_data = User.objects.get(id = current_user.id)
            user_data.email = form.cleaned_data.get('username')
            user_data.save()              # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="/images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect(url)


    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    setting = Setting.objects.get(pk = 1 )
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    wishlist = Wishlist.objects.filter(user_id = current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'category': category,
        'setting': setting,
        'form': form,
        'wishlist': wishlist,
        'shopcart': shopcart,
        'total': total,
        'faq': faq,
    }
    return render(request, 'faq.html', context)



