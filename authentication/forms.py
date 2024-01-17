from django import forms
from .models import UserProfile , ProfileInfo
from django.contrib.auth.hashers import make_password

class LoginUserForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'input'}),
            'first_name' : forms.TextInput(attrs={'class': 'input'}),
            'last_name' : forms.TextInput(attrs={'class': 'input'}),
            'password' : forms.PasswordInput(attrs={'class': 'input'}),
        }

    def clean(self): # Execute when form is validating
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True): # Execute when form is saving
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = ProfileInfo
        fields = ['profile_pic' , 'bio' , 'date_of_birth' , 'location']
        widgets = {
            'profile_pic' : forms.FileInput(attrs={'class': 'input'}),
            'bio' : forms.Textarea(attrs={'class': 'input'}),
            'date_of_birth' : forms.DateInput(attrs={'class': 'input' , 'type' : 'date'}),
            'location' : forms.TextInput(attrs={'class': 'input'}),
        }

