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


def logout_view(request):
    print(request.user)
    logout(request)
    return redirect('signin')

class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)
    confirm_password = forms.CharField(max_length=128)
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

    def clean(self):
        cleaned_data= super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
        return cleaned_data


        
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
        except Exception:
            print( 'Client create Error')
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

@login_required(login_url='/signin')
def company_profile(request, user_id):
    client = get_object_or_404(CustomUser, pk=user_id)
    print(client)
    return render(request, 'users/company_profile.html', {
            'client': client,
        })

@login_required(login_url='/signin')
def company_profile_save(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.client.company = request.POST['company']
    user.client.address = request.POST['address']
    user.client.address2 = request.POST['address2']
    user.client.country = request.POST['country']
    user.client.region = request.POST['region']
    user.client.city = request.POST['city']
    user.client.postal_code = request.POST['postal_code']
    # user.client.main_phone = request.POST['main_phone']
    user.client.main_phone_extension = request.POST['main_phone_extension']
    # user.client.alt_phone = request.POST['alt_phone']
    user.client.alt_phone_extension = request.POST['alt_phone_extension']
    # user.client.fax = request.POST['fax']
    user.client.business_email = request.POST['business_email']
    user.client.industry = request.POST['industry']

    user.client.save()
    return HttpResponse(request.POST['company'])

    
