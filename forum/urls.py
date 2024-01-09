from django.urls import path
from . import views
app_name = 'forum'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactPageView.as_view(), name='contact'), 
    path('forum/' , views.ForumPageView.as_view() , name='forum_page')
]