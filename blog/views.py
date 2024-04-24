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
    return render(request, 'blog/person_list.html', {'persons': persons})

def meditation_list(request):
    # Fetch and filter Meditation instances by published date
    meditations = Meditation.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Pass the data to the template context
    return render(request, 'blog/meditation_list.html', {'meditations': meditations})

def journaling_list(request):
    # Fetch and filter Journaling instances by published date
    journalings = Journaling.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Pass the data to the template context
    return render(request, 'blog/journaling_list.html', {'journalings': journalings})

###########################################
#add in a homepage dashboard view
###########################################

# your_app/views.py

from django.shortcuts import render
from .models import Person, Meditation, Journaling

def dashboard(request):
    if request.user.is_authenticated:
        # Assuming the logged-in user is associated with a Person model
        try:
            person = Person.objects.get(user=request.user)
            meditations = Meditation.objects.filter(person=person).order_by('-created_date')[:5]  # Last 5 sessions
            journal_entries = Journaling.objects.filter(person=person).order_by('-date')[:5]  # Last 5 entries
        except Person.DoesNotExist:
            person = None
            meditations = []
            journal_entries = []
        context = {
            'person': person,
            'meditations': meditations,
            'journal_entries': journal_entries,
            'greeting': f"Welcome back, {request.user.first_name}!"
        }
    else:
        # Default context for non-logged in users
        context = {
            'person': None,
            'meditations': [],
            'journal_entries': [],
            'greeting': "Welcome to Wellbeing for Youth!"
        }
    return render(request, 'blog/dashboard.html', context)
