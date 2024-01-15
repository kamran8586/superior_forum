from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .forms import LoginUserForm 
from django.views import View
from .models import UserProfile

class CreateUser(View):
    template_name = 'registration/create_user.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect('authentication:login')

        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'registration/login_user.html' 
    def get(self, request):
        form = LoginUserForm()
        return render(request, self.template_name , {'form': form})
    
    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('forum:home') 
            else:
                form.add_error(None, "Invalid email or password")

        return render(request, self.template_name, {'form': form})
    

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('authentication:login')
    
