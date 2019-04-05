from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import login_required

from .models import *


# Create your views here.
def index(request):
    return render(request, 'users/signin.html', {
            'error_message': "You didn't select a choice.",
        })

def signin(request):
    return render(request, 'users/signin.html')

def signup_post(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save(request)

                login(request, new_user)
                return JsonResponse({
                                'username': new_user.username,
                                'userid': new_user.pk})
            except Exception:
                return JsonResponse({'errors':{'server':'Server Error'} })
                # return HttpResponseServerError()
        else:
            return JsonResponse({'errors':form.errors})
    else:
        form = SignupForm()
    return JsonResponse({'errors':{'method':'GET method'} })



def signin_post(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({
                                'username': user.username,
                                'userid': user.pk})
            else:
                # Return a 'disabled account' error message
                return JsonResponse({'errors': 'Account is disabled or has not yet been activated' })
        else:
            return JsonResponse({'errors': 'Invalid Username or Password' })
    return JsonResponse({'errors': 'GET method' })

@login_required(login_url='/signin')
def company_profile(request, client_id):
    client = get_object_or_404(CustomUser, pk=client_id)
    print(client)
    return render(request, 'users/company_profile.html', {
            'client': client,
        })

def logout_view(request):
    print(request.user)
    logout(request)
    return redirect('signin')

class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)
    company = forms.CharField(max_length=200)
    
    def clean_email(self):
          data = self.cleaned_data['email']
          if CustomUser.objects.filter(email=data).count() > 0:
              raise forms.ValidationError("Email already exists")
          return data

    def clean_username(self):
          data = self.cleaned_data['username']
          if CustomUser.objects.filter(username=data).count() > 0:
              raise forms.ValidationError("Username already exists")
          return data

    def save(self, request):
        new_user = CustomUser(username=self.cleaned_data['username'])
        new_user.email = self.cleaned_data['email']
        new_user.set_password(self.cleaned_data['password'])
        new_user.is_active = True
        new_user.role = 'client'
        new_user.save()

        try:
            client = Client(user=new_user, company=self.cleaned_data['company'])
            client.save()
        except Exception(e):
            print(e)
            return new_user
        return new_user

class SigninForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)

    def login(self, request):
        try:
            user = CustomUser.objects.get(email=self.cleaned_data['email'])
            if(user.check_password(self.cleaned_data['password'])):
                request.session["userid"] = user.pk
                request.session["username"] = user.username
                request.session["email"] = user.email
                return user
            else:
                return False
        except Exception:
            return None

@login_required(login_url='/signin')
def dashboard(request):
    return render(request, 'projects/dashboard.html', {
        })

@login_required(login_url='/signin')
def projects(request):
    return render(request, 'projects/projects.html', {
        })

@login_required(login_url='/signin')
def new_project(request):
    return render(request, 'projects/new_project.html', {
        })