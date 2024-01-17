from django.shortcuts import render , redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import PostForm
from .models import Post , Like , Comment , Reply 
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import ProfileInfo
# Create your views here.
class HomePageView(View):
    template_name = 'forum/home.html'
    def get(self, request):
        return render(request, self.template_name)
    

class ContactPageView(View):
    template_name = 'forum/contact.html'
    def get(self, request):
        return render(request, self.template_name)
    

class ForumPageView(View):
    template_name = 'forum/forum_page.html'

    def get(self, request):
        if request.user:
            user_profile = ProfileInfo.objects.get(user=request.user)
            following_users = user_profile.follows.all()

            # Get posts from users the current user is following
            followed_posts = Post.objects.filter(author__profile__in=following_users).order_by('-created_at')

            # Get posts from other users
            other_posts = Post.objects.exclude(author__profile__in=following_users).order_by('-created_at')

            # Concatenate the two querysets
            posts = followed_posts | other_posts

        else:
            posts = Post.objects.all().order_by('-created_at')

        return render(request, self.template_name, {'posts': posts})
    
class PostDetailView(View):
    template_name = 'forum/post_detail.html'
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        # recent_posts = Post.objects.exclude(pk=pk)[:5]
        return render(request, self.template_name, {'post' : post })
    
class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
            return redirect('forum:forum_page')
        return redirect('forum:forum_page')
    
    
class AskQuestionView(LoginRequiredMixin , View):
    login_url = 'authentication:login'
    def get(self, request):
        form = PostForm()
        return render(request, 'forum/ask_question.html', {'form': form})

    def post(self, request):
        current_user = request.user
        form = PostForm(request.POST , request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('forum:forum_page')
        else:
            return render(request , 'forum/ask_question.html' , {'form': form})
        
class LikeView(View):
    def post(self, request, pk):
        if request.user:
            post = get_object_or_404(Post, pk=pk)
            user = request.user 
            existing_like = Like.objects.filter(post=post, user=user).first()

            if existing_like:
                existing_like.delete()
            else:
                new_like = Like(post=post, user=user)
                new_like.save()

        return redirect('forum:forum_page')

        
class CreateCommentView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user  # Assuming you have authentication enabled
        content = request.POST.get('content')

        comment = Comment(post=post, user=user, content=content)
        comment.save()

        return redirect('forum:post_detail', pk=pk)

class DeleteCommentView(View):
    def post(self, request,  pk , post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user 
        if user == comment.user:
            comment.delete()
        return redirect('forum:post_detail', pk=post_pk)
    
class CreateReplyView(View):
    def post(self, request, pk, comment_pk):
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user 
        content = request.POST.get('content')

        reply = Reply(comment=comment, user=user, content=content)
        reply.save()

        return redirect('forum:post_detail', pk=pk)
    
