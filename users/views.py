from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone




from .models import Client

# Create your views here.
def index(request):
    return render(request, 'users/signin.html', {
            'error_message': "You didn't select a choice.",
        })

def signin(request):
    return render(request, 'users/signin.html')

def dashboard(request):
    return render(request, 'projects/dashboard.html', {
        })

def projects(request):
    return render(request, 'projects/projects.html', {
        })

def signup_post(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save(request)
                print(new_user.pk)
                return JsonResponse({
                                'username': new_user.username,
                                'userid': new_user.pk})
            except Exception:
                JsonResponse({'errors':{'server':'Server Error'} })
                # return HttpResponseServerError()
        else:
            return JsonResponse({'errors':form.errors})
    else:
        form = SignupForm()
    return JsonResponse({'errors':{'method':'GET method'} })

def signin_post(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            try:
                user = form.login(request)
                print(user)
                if user == False:
                    return JsonResponse({'errors': 'Incorrect username or password' })
                elif user == None:
                    return JsonResponse({'errors': 'Incorrect username or password' })
                else:
                    return JsonResponse({
                                'username': user.username,
                                'userid': user.pk})
            except Exception:
                JsonResponse({'errors': 'Server Error' })
        else:
            return JsonResponse({'errors':form.errors})
    else:
        form = SignupForm()
    return JsonResponse({'errors': 'GET method' })

def company_profile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    print(client)
    return HttpResponse("Company Profile Page")
    return render(request, 'users/company_profile.html', {
            'client': client,
        })

def logout(request):
    del request.session["userid"]
    del request.session["username"]
    del request.session["email"]
    return redirect('signin')

class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)

    def clean_email(self):
          data = self.cleaned_data['email']
          if Client.objects.filter(email=data).count() > 0:
              raise forms.ValidationError("Email already exists")
          return data

    def clean_username(self):
          data = self.cleaned_data['username']
          if Client.objects.filter(username=data).count() > 0:
              raise forms.ValidationError("Username already exists")
          return data

    def save(self, request):
        new_user = Client(username=self.cleaned_data['username'])
        new_user.email = self.cleaned_data['email']
        new_user.created_at = timezone.now()
        new_user.set_password(self.cleaned_data['password'])
        new_user.save()
        request.session["userid"] = new_user.pk
        request.session["username"] = new_user.username
        request.session["email"] = new_user.email
        return new_user

class SigninForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(max_length=128)

    def login(self, request):
        try:
            user = Client.objects.get(email=self.cleaned_data['email'])
            if(user.check_password(self.cleaned_data['password'])):
                request.session["userid"] = user.pk
                request.session["username"] = user.username
                request.session["email"] = user.email
                return user
            else:
                return False
        except Exception:
            return None