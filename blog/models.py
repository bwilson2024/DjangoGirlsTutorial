from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    name = models.CharField(max_length=100, blank=False, help_text="Enter the full name of the person", default="No Name Yet")
    wellbeing = models.CharField(max_length=7, choices=WELLBEING_CHOICES, default='average')
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

class Meditation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='meditations')
    length = models.PositiveIntegerField(help_text="Duration in minutes")
    impact = models.CharField(max_length=255, blank=True, help_text="Descriptive impact on wellbeing")
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

class Journaling(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='journal_entries')
    entry_number = models.PositiveIntegerField()
    date = models.DateField(default=now)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

# Note: The WellbeingReport class is conceptual and used for generating reports rather than storing data, so it doesn't require these fields.