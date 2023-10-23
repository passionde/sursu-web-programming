"""
Definition of urls for blog.
"""

from datetime import datetime

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from blog import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('task_navigation/', views.task_navigation, name='task_navigation'),
    path('links/', views.links, name='links'),
    path('anketa/', views.anketa, name='anketa'),
    path('blog', views.blog, name='blog'),
    path('videopost', views.videopost, name='videopost'),
    re_path(r'^(?P<parametr>\d+)/$', views.blogpost, name='blogpost'),
    path('newpost', views.newpost, name='newpost'),
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    re_path(r'^registration$', views.registration, name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()