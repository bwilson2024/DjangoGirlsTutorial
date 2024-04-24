from django.shortcuts import render
from django.utils import timezone
from .models import Post, Person, Meditation, Journaling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
    print(f"Journaling is  + {journalings}")
    # Pass the data to the template context
    return render(request, 'blog/journaling_list.html', {'journalings': journalings})

###########################################
#add in a homepage dashboard view
###########################################

# your_app/views.py

from django.shortcuts import render
from .models import Person, Meditation, Journaling

# def dashboard(request):
#     if request.user.is_authenticated:
#         # Assuming the logged-in user is associated with a Person model
#         try:
#             person = Person.objects.get(user=request.user)
#             meditations = Meditation.objects.filter(person=person).order_by('-created_date')[:5]  # Last 5 sessions
#             journal_entries = Journaling.objects.filter(person=person).order_by('-date')[:5]  # Last 5 entries
#         except Person.DoesNotExist:
#             person = None
#             meditations = []
#             journal_entries = []
#         context = {
#             'person': person,
#             'meditations': meditations,
#             'journal_entries': journal_entries,
#             'greeting': f"Welcome back, {request.user.first_name}!"
#         }
#     else:
#         # Default context for non-logged in users
#         context = {
#             'person': None,
#             'meditations': [],
#             'journal_entries': [],
#             'greeting': "Welcome to Wellbeing for Youth!"
#         }
#     return render(request, 'blog/dashboard.html', context)


@login_required
def dashboard(request):
    try:
        person = request.user.person
        meditations = Meditation.objects.filter(person=person).order_by('-created_date')[:5]
        journal_entries = Journaling.objects.filter(person=person).order_by('-date')[:5]
    except Person.DoesNotExist:
        person = None
        meditations = []
        journal_entries = []

    context = {
        'person': person,
        'meditations': meditations,
        'journal_entries': journal_entries,
        #'greeting': f"Welcome back, {request.user.first_name}!"
        #'greeting': f"Welcome back, {request.user.get_full_name()}!"
        'greeting': f"Welcome back, {request.user.get_username()}!"

    }
    return render(request, 'blog/dashboard.html', context)


###############################################################
# add in add meditation view
################################################################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MeditationForm

@login_required
def add_meditation(request):
    if request.method == 'POST':
        form = MeditationForm(request.POST)
        if form.is_valid():
            meditation = form.save(commit=False)
            meditation.person = request.user.person
            meditation.save()
            return redirect('dashboard')
    else:
        form = MeditationForm()
    return render(request, 'blog/add_meditation.html', {'form': form})

###############################################################
#add signup
###############################################################

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Person profile for the new user
            person = Person.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

#####################################################################
#add a wellbeing report view
#####################################################################

from django.db.models import Count
from django.db.models.functions import TruncDate

@login_required
def wellbeing_report(request):
    meditations = Meditation.objects.filter(person=request.user.person).annotate(entry_date=TruncDate('created_date')).values('entry_date').annotate(count=Count('id')).order_by('entry_date')
    journals = Journaling.objects.filter(person=request.user.person).annotate(entry_date=TruncDate('date')).values('entry_date').annotate(count=Count('id')).order_by('entry_date')

    dates = sorted(set(meditations.values_list('entry_date', flat=True)) | set(journals.values_list('entry_date', flat=True)))

    data = []
    for date in dates:
        meditation_count = next((m['count'] for m in meditations if m['entry_date'] == date), 0)
        journal_count = next((j['count'] for j in journals if j['entry_date'] == date), 0)
        data.append({'date': date, 'meditation_count': meditation_count, 'journal_count': journal_count})

    return render(request, 'blog/wellbeing_report.html', {'data': data})