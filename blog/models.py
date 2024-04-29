from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
###########################
#Add in additional classes for this app
###########################

class Person(models.Model):
    WELLBEING_CHOICES = [
        ('poor', 'Poor'),
        ('average', 'Average'),
        ('good', 'Good'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=False, help_text="Enter the full name of the person", default="No Name Yet")
    wellbeing = models.CharField(max_length=7, choices=WELLBEING_CHOICES, default='average')
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

class Meditation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='meditations')
    length = models.PositiveIntegerField(help_text="Duration in minutes")
    impact = models.CharField(max_length=255, blank=True, help_text="Descriptive impact on wellbeing")
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

class Journaling(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='journal_entries')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='journal_entries')
    entry_number = models.PositiveIntegerField()
    entry_text = models.TextField(blank=True)  # Add this field to store the journal entry text
    date = models.DateField(default=now)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

# Note: The WellbeingReport class is conceptual and used for generating reports rather than storing data, so it doesn't require these fields.

##############################################################
#Add in users and user management to this app
##############################################################

