from django.shortcuts import render
from django.utils import timezone
from .models import Post, Person, Meditation, Journaling

def post_list(request):
    #run the query set and
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #pass the post to the "template context" by updating the render function call
    return render(request, 'blog/post_list.html', {'posts': posts})

################################################################
#Add views for models
################################################################

def person_list(request):
    # Fetch and filter Person instances by published date
    persons = Person.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Pass the data to the template context
    return render(request, 'your_app/person_list.html', {'persons': persons})

def meditation_list(request):
    # Fetch and filter Meditation instances by published date
    meditations = Meditation.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Pass the data to the template context
    return render(request, 'your_app/meditation_list.html', {'meditations': meditations})

def journaling_list(request):
    # Fetch and filter Journaling instances by published date
    journalings = Journaling.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Pass the data to the template context
    return render(request, 'your_app/journaling_list.html', {'journalings': journalings})
