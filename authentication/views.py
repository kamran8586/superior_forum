from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .forms import LoginUserForm , ProfileInfoForm
from django.views import View
from .models import UserProfile , ProfileInfo

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
    
class ProfileInfoView(View):
    template_name = 'registration/profile_info.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name , {'post_user' : user})

class UserProfileInfoView(View):
    template_name = 'registration/profile_info.html'
    def get(self, request  , pk):
        user = UserProfile.objects.get(pk=pk)
        return render(request, self.template_name, {'post_user': user })
    
    
class AddProfileInfoView(View):
    template_name = 'registration/edit_profile.html'
    
    def get(self, request):
        # profile_instance = request.user.profile if hasattr(request.user, 'profile') else None
        form = ProfileInfoForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ProfileInfoForm(request.POST , request.FILES)

        if form.is_valid():
            profile_info = form.save(commit=False)
            profile_info.user = request.user
            profile_info.save()
            return redirect('authentication:profile_info')

        return render(request, self.template_name, {'form': form})

    
class FollowUserView(View):
    def get(self, request, pk):
        user = UserProfile.objects.get(pk=pk)
        user.profile.followed_by.add(request.user.profile)
        return redirect('authentication:user_profile', pk=user.pk)

class UnFollowUserView(View):
    def get(self, request, pk):
        user = UserProfile.objects.get(pk=pk)
        user.profile.followed_by.remove(request.user.profile)
        return redirect('authentication:user_profile', pk=user.pk)

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
                return redirect('authentication:edit_profile') 
            else:
                form.add_error(None, "Invalid email or password")
                

        return render(request, self.template_name, {'form': form})
    

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('authentication:login')
    
