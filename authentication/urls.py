from django.urls import path
from . import views
app_name = "authentication"
urlpatterns = [
    path('login/' , views.LoginView.as_view(), name="login"),
    path('signup/' , views.CreateUser.as_view(), name="signup"),
    path('profile_info/' , views.ProfileInfoView.as_view(), name="profile_info"),
    path('user_profile/<int:pk>' , views.UserProfileInfoView.as_view(), name="user_profile"),
    path('edit_profile/' , views.AddProfileInfoView.as_view(), name="edit_profile"),
    path('follow/<int:pk>/' , views.FollowUserView.as_view(), name="follow"),
    path('unfollow/<int:pk>/' , views.UnFollowUserView.as_view(), name="unfollow"),
    path('logout/' , views.LogoutView.as_view(), name="logout"),
]