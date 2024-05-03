from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Person, Meditation, Journaling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm


def post_list(request):
    #run the query set and
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #pass the post to the "template context" by updating the render function call
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

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

#        two_days_ago = timezone.now() - datetime.timedelta(days=2)
#        meditations = Meditation.objects.filter(person=person, created_date__gte=two_days_ago).order_by('-created_date')[:5]
        meditations = Meditation.objects.filter(person=person).order_by('-created_date')[:1]
        journal_entries = Journaling.objects.filter(person=person).order_by('-date')[:3]

        # Truncate the journal entry text to display only the first few sentences
        # for entry in journal_entries:
        #     print(f"entry is {entry}")
        #     sentences = entry.entry_text.split(' ')
        #     entry.truncated_text = '.'.join(sentences[:15]) + '.' if len(sentences) > 3 else entry.entry_text
        # print(f"Sentences are {sentences}")

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
        'greeting': f"Welcome, {request.user.get_username()}!"

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
    try:
        person = request.user.person
        meditations = Meditation.objects.filter(person=person).order_by('created_date')
        journals = Journaling.objects.filter(person=person).order_by('date')

        data = []
        for meditation in meditations:
            data.append({'date': meditation.created_date.date(), 'meditation_count': 1, 'journal_count': 0})
        for journal in journals:
            data.append({'date': journal.date, 'meditation_count': 0, 'journal_count': 1})

        return render(request, 'blog/wellbeing_report.html', {'data': data})
    except Person.DoesNotExist:
        return render(request, 'blog/wellbeing_report.html', {'data': []})
##########################################################
# add in add journaling view
##########################################################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MeditationForm, JournalingForm

@login_required
def add_journaling(request):
    if request.method == 'POST':
        form = JournalingForm(request.POST)
        if form.is_valid():
            journaling = form.save(commit=False)
            journaling.person = request.user.person
            journaling.save()
            return redirect('dashboard')
    else:
        form = JournalingForm()
    return render(request, 'blog/add_journaling.html', {'form': form})
