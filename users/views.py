from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'users/dashboard.html', {
        })

def projects(request):
    return render(request, 'users/projects.html', {
        })