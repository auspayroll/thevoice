# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Candidate, Team, Performance, PerformanceScore, Mentor
from .candidate_views import index as candidate_index
from .mentor_views import index as mentor_index
from .functions import in_group, is_member


@login_required
def index(request):
    if False:
        return mentor_index(request)
    elif False:
        return candidate_index(request)
    else:
        teams = Team.objects.all().prefetch_related('members').order_by('name')
        return render(request, 'teams.html', {'teams': teams})


@login_required
@user_passes_test(in_group(['admin']))
def mentors(request):
    mentors = Mentor.objects.all().order_by('last_name')
    return render(request, 'mentors.html', {'mentors': mentors})


@login_required
@user_passes_test(in_group(['admin','mentor']))
def teams(request):
    if is_member(request.user, 'admin'):
       teams = Team.objects.all().prefetch_related('members').order_by('name')
    else:
        teams = Team.objects.filter(mentor=request.user).prefetch_related('members').order_by('name')

    return render(request, 'teams.html', {'teams': teams})


@login_required
@user_passes_test(in_group(['admin','mentor']))
def team(request, team_pk):
    if is_member(request.user, 'admin'):
       team = get_object_or_404(Team, pk=team_pk) #display performance
    else:
        team = get_object_or_404(Team, pk=team_pk, mentor=request.user)

    performances = Performance.objects.filter(candidate__team=team).order_by('-date')
    members = team.members.all()
    return render(request, 'team.html', {'team': team, 'members': members, 'performances': performances})


def performance(request, performance_pk):
    p = get_object_or_404(Performance, pk=performance_pk) #display performance
    scores = p.performance_scores.all().order_by('-score')
    return render(request, 'performance.html', {'performance': performance, 'scores': scores})


@login_required
@user_passes_test(in_group(['admin','mentor']))
def candidates(request):
    if is_member(request.user, 'admin'):
        candidates = Candidate.objects.all().order_by('last_name')
    else:
        candidates = Candidate.objects.filter(team__mentor=request.user).order_by('last_name')
    return render(request, 'candidates.html', {'candidates': candidates})


@login_required
def view_candidate(request, candidate_pk):
    if is_member(request.user, 'admin'):
        candidate = get_object_or_404(Candidate, pk=candidate_pk)
    elif is_member(request.user, 'mentor'):
        candidate = get_object_or_404(Candidate, pk=candidate_pk, team__candidate=request.user)
    else:
        candidate = get_object_or_404(Candidate, pk=candidate_pk)

    performances = candidate.candidate_performances.all()
    return render(request, 'candidate.html', {'candidate':candidate, 'performances': performances})


def performances(request):
    performances = Performance.objects.all().order_by('-date')
    return render(request, 'performances.html', {'performances': performances})


def performance(request, performance_pk):
    performance = get_object_or_404(Performance, pk=performance_pk)
    scores = performance.performance_scores.all()
    return render(request, 'performance.html', {'performance': performance, 'scores': scores})







