from django.db import models
from authentication.models import UserProfile
from django.utils import timezone

class Category(models.Model):
    title = models.TextField(max_length = 100)
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.TextField(max_length = 100)

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE , related_name = "post_set")
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='static/media/posts', blank=True)
    category = models.ForeignKey(Category , on_delete= models.CASCADE)
    tags = models.ManyToManyField(Tag , blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_posted_time_in_minutes(self):
        minutes = (timezone.now() - self.created_at).total_seconds() / 60
        return int(minutes)
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file when the post is deleted
        if self.image:
            storage, path = self.image.storage, self.image.path
            super(Post, self).delete(*args, **kwargs)
            storage.delete(path)
        else:
            super(Post, self).delete(*args, **kwargs)
            
    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    

class Like(models.Model):
    post = models.ForeignKey(Post,related_name='likes' , on_delete=models.CASCADE , db_index = True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE , db_index = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.post.title}"
    
    def is_already_liked(self):
        return self.user in self.post.likes.all()

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments' ,  on_delete=models.CASCADE , db_index = True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.post.title}"

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name = "replies" , on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.comment.content}"