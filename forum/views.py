from django.shortcuts import render
from django.views import View
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
        return render(request, self.template_name)