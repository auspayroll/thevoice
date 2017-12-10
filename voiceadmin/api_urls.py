from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views as views

urlpatterns = [

    url(r'team_search/$', views.team_search, name='team_search'),

    url(r'candidates/$', views.CandidateList.as_view(), name='candidate_list'),
    url(r'candidates/(?P<pk>[0-9]+)$', views.CandidateDetail.as_view(),name='candidate-detail'),
    
    url(r'teams/$', views.TeamList.as_view(), name='team-list'),
    url(r'teams/(?P<pk>[0-9]+)$', views.TeamDetail.as_view(), name='team-detail'),

    url(r'performances/$', views.PerformanceList.as_view(), name='performance-list'),
    url(r'performances/(?P<pk>[0-9]+)$', views.PerformanceDetail.as_view(), name='performance-detail'),
    url(r'performances/(?P<pk>[0-9]+)/scores/$', views.PerformanceDetail.as_view(), name='post-performance-score'),

    url(r'mentors/$', views.MentorList.as_view(), name='mentor-list'),
    url(r'mentors/(?P<pk>[0-9]+)$', views.MentorDetail.as_view(), name='mentor-detail'),

    url(r'performance_scores/$', views.PerformanceScoreList.as_view(), name='performance-scores-detail'),
    url(r'performance_scores/(?P<pk>[0-9]+)/$', views.PerformanceScoreDetail.as_view(), name='performance-scores-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

