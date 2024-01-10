from django.shortcuts import render , redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Post , Like , Comment , Reply
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
    posts = Post.objects.all().order_by('-updated_at')
    def get(self, request):
        return render(request, self.template_name , {'posts' : self.posts})
    
class PostDetailView(View):
    template_name = 'forum/post_detail.html'
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        # recent_posts = Post.objects.exclude(pk=pk)[:5]
        return render(request, self.template_name, {'post' : post })
    
class LikeView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user  # Assuming you have authentication enabled

        # Check if the user has already liked the post
        if not Like.objects.filter(post=post, user=user).exists():
            # If not, create a new Like instance
            like = Like(post=post, user=user)
            like.save()
            return JsonResponse({'status': 'liked'})
        else:
            # If the user has already liked the post, you can handle it accordingly
            return JsonResponse({'status': 'already_liked'})
        
class CreateCommentView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user  # Assuming you have authentication enabled
        content = request.POST.get('content')

        comment = Comment(post=post, user=user, content=content)
        comment.save()

        return redirect('forum:post_detail', pk=pk)
    
class CreateReplyView(View):
    def post(self, request, pk, comment_pk):
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user 
        content = request.POST.get('content')

        reply = Reply(comment=comment, user=user, content=content)
        reply.save()

        return redirect('forum:post_detail', pk=pk)