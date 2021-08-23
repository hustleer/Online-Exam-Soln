import json
from django.core.paginator import Paginator
from itertools import chain , islice
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from django.contrib.auth import authenticate , login
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from home.forms import SearchForm
from home.models import CustomUser , QuestionAnwers , Images
from django.http import HttpResponseRedirect
from django.shortcuts import render


from mysite import settings
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

def loginpage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    else:
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
                    return HttpResponseRedirect('/index')

                else:
                    messages.warning(request , "Login error ! Please check username and password")
                    return HttpResponseRedirect(url)

        return render(request , 'login.html')


        
def index(request):
    if request.user.is_authenticated:
 
        question = QuestionAnwers.objects.all().order_by('-id')
        context = {
            "question" : question  ,
        }
        return render(request , "home.html" , context)
    else:
        return HttpResponseRedirect('/')
        
           
def imagepage(request):
    if request.user.is_authenticated:
        if 'uploadimage' in request.POST:
            if request.method == 'POST':
 
                files  = request.FILES.getlist('uploadedfile')  
                for image in files:  
                    Images.objects.create(
                        image = image , 
                        pidit = request.user.name
                        
                    )
                return HttpResponseRedirect('/refresh')
        image = Images.objects.all().order_by('-id')
        context = {
            "image" : image  ,
        }
        return render(request , "image.html" , context)
    else:
        return HttpResponseRedirect('/')

def refresh(request):
    return HttpResponseRedirect('/imagepage')
        
def postquestion(request):
    if request.user.is_authenticated:
        print("test pass")
 
        if 'questionpost' in request.POST:
            if request.method == 'POST':
                question  = request.POST['question']
                answer  = request.POST['answer']
                
                QuestionAnwers.objects.create(
                    question = question , 
                    answer = answer , 
                    pidit = request.user.name
                    
                )

                return render(request , "post.html" )


        return render(request , "post.html" )
    else:
        return HttpResponseRedirect('/')
        
    
 
        
def searchquestion(request):
    if request.user.is_authenticated:
        print("search pass")
 
        if 'searchquestion' in request.POST:
            if request.method == 'POST':
                ques  = request.POST['searchques']
                
                question = QuestionAnwers.objects.filter(Q(question__icontains=ques) | Q(answer__icontains=ques)  ).order_by('-id')
                
                context = {
                    "question" : question
                }
                
                return render(request , "search.html" , context )


        return render(request , "search.html" )
    else:
        return HttpResponseRedirect('/')
        
    
