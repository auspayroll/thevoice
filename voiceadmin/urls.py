from django.conf.urls import url
from . import views as admin_views
from django.contrib.auth import views as auth_views
#from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', admin_views.index, name='index'),
    url(r'login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'teams/$', admin_views.teams, name='teams'),
    url(r'mentors/$', admin_views.mentors, name='mentors'),
    url(r'team/(?P<team_pk>[0-9]+)/$', admin_views.team, name='team'),  
    url(r'candidates/$', admin_views.candidates, name='candidates'),
    url(r'candidate/(?P<candidate_pk>[0-9]+)/$', admin_views.view_candidate, name='candidate'),
    url(r'performances/$', admin_views.performances, name='performances'),
    url(r'performance/(?P<performance_pk>[0-9]+)/$', admin_views.performance, name='performance'),

]

