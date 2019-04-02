from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django import forms
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth.hashers import make_password

from .models import Client

# Create your views here.
def index(request):
    return render(request, 'users/signin.html', {
            'error_message': "You didn't select a choice.",
        })

def signin(request):
    return render(request, 'users/signin.html', {
            'error_message': "You didn't select a choice.",
        })

def dashboard(request):
    return render(request, 'projects/dashboard.html', {
        })

def projects(request):
    return render(request, 'projects/projects.html', {
        })

# def signup_post(request):
#     context = {'text': 'text'}
#     return render(request, 'users/index.html', context)

def signup_post(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                new_request = form.save()
                return HttpResponse("success.")
            except Exception:
                return HttpResponseServerError()
        else:
            print(form.errors)
        return HttpResponse("GET method.")

    else:
        form = SignupForm()
    return HttpResponse("GET method.")

# def signup_post(request, cmspage=None):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             try:
#                 new_request = form.save()
#                 return HttpResponseRedirect("/project")
#             except Exception:
#                 return HttpResponseServerError()
#     else:
#         form = SignupForm()
#     return render(request, 'projects/projects.html', {
#         })

class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)

    def save(self):
        new_user = Client(username=self.cleaned_data['username'])
        new_user.email = self.cleaned_data['email']

        hash_password = make_password(self.cleaned_data['password'], None, 'md5')
        new_user.password = hash_password

        #new_user.set_password(self.cleaned_data['password'])
        new_user.save()

        return new_user