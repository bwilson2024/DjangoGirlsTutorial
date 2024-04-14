from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    #run the query set and
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #pass the post to the "template context" by updating the render function call
    return render(request, 'blog/post_list.html', {'posts': posts})