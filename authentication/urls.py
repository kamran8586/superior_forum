from django.urls import path
from . import views
app_name = "authentication"
urlpatterns = [
    path('login/' , views.LoginView.as_view(), name="login"),
    path('signup/' , views.CreateUser.as_view(), name="signup"),
    path('logout/' , views.LogoutView.as_view(), name="logout"),
]