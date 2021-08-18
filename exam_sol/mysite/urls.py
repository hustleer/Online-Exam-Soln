"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import home
from home import views
from order import views as OrderViews
from user import views as UserViews
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_('admin/'), admin.site.urls),
    path('', views.index, name='home'),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls'), name='user'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),


    path(_('about/'), views.aboutus, name='aboutus'),
    path(_('search_for_banner/<int:id>/'), views.search_for_banner, name='search_for_banner'),
    path(_('contact/'), views.contactus, name='contactus'),
    # path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),  
    path('category/<int:id>/<slug:slug>/<int:color_data>/<int:price_data>/<int:brand_data>/<int:rate_data>/', views.category_products, name='category_products'),
    path('search/<int:id>/<str:query>/<int:color_data>/<int:price_data>/<int:brand_data>/<int:rate_data>/', views.search, name='search'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),  
    path('wishlist/', OrderViews.wishlist, name='wishlist'),   
    path('login/', UserViews.login_form, name='login'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('signup/', UserViews.signup_form, name='signup'),
    path('faq/', views.faq, name='faq'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('ajaxtest/', views.ajaxtest, name='ajaxtest'),
    path('ajaxtestdelete/', views.ajaxtestdelete, name='ajaxtestdelete'),
    path('ajaxcartdelete1/', views.ajaxcartdelete1, name='ajaxcartdelete1'), 
    path('ajaxlistdelete/', views.ajaxlistdelete, name='ajaxlistdelete'),
    path('ajaxcartupdate/', views.ajaxcartupdate, name='ajaxcartupdate'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
