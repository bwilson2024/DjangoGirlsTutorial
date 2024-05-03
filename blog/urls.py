from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# add url pattern
urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('persons/', views.person_list, name='person_list'),
    path('meditations/', views.meditation_list, name='  '),
    path('journals/', views.journaling_list, name='journaling_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),    
    path('add_meditation/', views.add_meditation, name='add_meditation'),
    path('signup/', views.signup, name='signup'),
    path('wellbeing-report/', views.wellbeing_report, name='wellbeing_report'),
    path('add_journaling/', views.add_journaling, name='add_journaling')

]