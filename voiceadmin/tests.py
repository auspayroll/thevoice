# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from random import randint
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
from voiceadmin.models import *
from django.db.models import Sum
from django.db.models import Avg
from functions import update_average

first_names = ['John', 'Richard', 'Harry', 'David', 'Simon', 'Tam', 'Fiona', 'Alice']
last_names = ['Smith', 'Johns', 'Jones', 'Habib', 'Grant', 'Walker', 'Harrison', 'White']
songs = ['Love me Tender', 'Over the hill', 'Clocks', 'Unbreakable', 'Scatterbrain', 'Django', 'Live and let die', 'Wild West', 'Kiss Me', 'Heartbreak Hotel']

mentor_teams = {'Simon Cowell':'Hooley Dooleys', 
                'Lady Gaga':'The commitments', 
                'Sting':'Pretenders', 
                'Elvis':'Loners', 
                'Bono':'Radioheads'}

team_names = mentor_teams.values()
mentor_names = mentor_teams.keys()

def choose(choices):
    return choices[randint(0,len(choices)-1)]

def random_date():
    return now() - timedelta(days=randint(1,100))

def random_dob():
    return now()  - timedelta(days=(365*20 + randint(1,365)))

class ScoreTestCase(TestCase):

    def setUp(self):
    
        teams = []
        self.mentors = mentors = []
        for mentor_name, team_name in mentor_teams.items():
            try:
                first, second = mentor_name.split(' ')
            except:
                second = mentor_name
                first = ''

            m = Mentor.objects.create(last_name=second, other_names=first)
            mentors.append(m)

            team = Team.objects.create(name=team_name, mentor=m) 
            teams.append(team)

        self.candidates = candidates = []
        self.performances = []
        for i in range(50):
            candidate = Candidate.objects.create(last_name=choose(last_names), other_names=choose(first_names), team=choose(teams), dob=random_dob())
            candidates.append(candidate)
            performance = Performance.objects.create(song=choose(songs), candidate=candidate, date=random_date())
            for mentor in mentors:
                PerformanceScore.objects.create(performance=performance, mentor=mentor, score=randint(1,100))
                self.performances.append(performance)


    def test_team_averages(self):
        teams = Team.objects.annotate(test_score=Avg('members__average_score'))
        test_scores = [(team.test_score) for team in teams]
        average_scores = [(team.average_score) for team in teams]
        test_scores = [int(team.test_score) for team in teams]
        average_scores = [int(team.average_score) for team in teams]
        self.assertSequenceEqual(test_scores, average_scores)


    def test_candidate_averages(self):
    	candidates = Candidate.objects.annotate(test_score=Avg('candidate_performances__performance_scores__score'))
    	test_scores = [int(c.test_score) for c in candidates]
    	average_scores = [int(c.average_score) for c in candidates]
    	self.assertSequenceEqual(test_scores, average_scores)

    def test_score(self):
    	performance = choose(self.performances)
    	team_score = performance.candidate.team.average_score
    	team_no_scores = performance.candidate.team.no_scores
    	candidate_score = performance.candidate.average_score
    	candidate_no_scores = performance.candidate.no_scores

    	score = PerformanceScore.objects.create(performance=performance, mentor=self.mentors[0], score=randint(1,100))
    	team_score_should_be, _ = update_average(team_score, team_no_scores, score.score)
    	candidate_score_should_be, _ = update_average(candidate_score, candidate_no_scores, score.score)
    	self.assertEqual(int(team_score_should_be), int(performance.candidate.team.average_score))
    	self.assertEqual(int(candidate_score_should_be), int(performance.candidate.average_score))









