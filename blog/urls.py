from django.urls import path
from . import views

# add url pattern
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('persons/', views.person_list, name='person_list'),
    path('meditations/', views.meditation_list, name='meditation_list'),
    path('journals/', views.journaling_list, name='journaling_list'),
    path('dashboard/', views.dashboard, name='dashboard')

]