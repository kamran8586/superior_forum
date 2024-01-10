from django.urls import path
from . import views
app_name = 'forum'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactPageView.as_view(), name='contact'), 
    path('forum/' , views.ForumPageView.as_view() , name='forum_page'), 
    path('forum/post/<int:pk>' , views.PostDetailView.as_view() , name='post_detail'), 
    path('forum/post/<int:pk>/like' , views.LikeView.as_view() , name='like_post'), 
    path('forum/post/<int:pk>/comment/' , views.CreateCommentView.as_view() , name = 'create_comment' ),
    path('forum/post/<int:pk>/comment/<int:comment_pk>/' , views.CreateReplyView.as_view() , name = 'create_reply' ),
]