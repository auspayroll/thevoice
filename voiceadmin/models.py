# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator
from .functions import update_average
from django.contrib.auth.models import User


class Person(models.Model): 
	class Meta:
		abstract = True

	last_name = models.CharField(max_length=200)
	other_names = models.CharField(max_length=200, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

	def __unicode__(self):
		if self.other_names:
			return "%s, %s" % (self.last_name, self.other_names)
		return self.last_name

	@property
	def first_name(self):
		return self.other_names[0]

	def middle_names(self):
		names = self.other_names.split(' ')
		if len(names) > 1:
			return names[1:]
		else:
			return ''


class ScoreField(models.PositiveSmallIntegerField):
    def __init__(self, max_value=100, verbose_name='score', name='score', *args, **kwargs):
        kwargs['validators'] = [MaxValueValidator(max_value, message="Please enter a value less than %s" % max_value)]
        super(ScoreField, self).__init__(verbose_name, name, *args, **kwargs)


class Mentor(Person): 
	pass



class Team(models.Model):
	name = models.CharField(max_length=200)
	mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
	date_formed = models.DateField(blank=True, null=True)
	average_score = models.FloatField(blank=True, null=True)
	no_scores = models.IntegerField(default=0)

	def update_score(self, score, save=False):
		self.average_score, self.no_scores = update_average(self.average_score, self.no_scores, score)
		if save:
			self.save()
		return self.average_score, self.no_scores

	def __unicode__(self):
		return self.name


class Candidate(Person):
	dob = models.DateField('date of birth', null=True, blank=True)
	average_score = models.FloatField(default=0, blank=True, null=True)
	no_scores = models.IntegerField(default=0)
	team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='members')
	last_name = models.CharField(max_length=200)
	other_names = models.CharField(max_length=200)

	def update_score(self, score, save=False):
		self.average_score, self.no_scores = update_average(self.average_score, self.no_scores, score)
		if save:
			self.save()
		return self.average_score, self.no_scores

	@property
	def mentor(self):
		if self.team and self.team.mentor:
			return str(self.team.mentor)

	def __unicode__(self):
		if self.other_names:
			return "%s, %s" % (self.last_name, self.other_names)
		return self.last_name



class Performance(models.Model):
    song = models.CharField(max_length=200)
    date = models.DateTimeField()
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, related_name='candidate_performances')
    average_score = models.FloatField(default=True)
    no_scores = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
		return self.song

    def update_score(self, score, save=False):
		self.average_score, self.no_scores = update_average(self.average_score, self.no_scores, score)
		if save: 
			self.save()
		return self.average_score, self.no_scores


class PerformanceScore(models.Model):
	performance = models.ForeignKey(Performance, on_delete=models.SET_NULL, null=True, related_name='performance_scores')
	mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
	score = ScoreField(default=0)

	#class Meta:
	#	unique_together = ('mentor', 'performance')

	def save(self, *args, **kwargs):
		#update candidate average
		if self.performance and self.performance.candidate: 
			self.performance.candidate.update_score(self.score, True)
		#update team average
		if self.performance.candidate and self.performance.candidate.team:
			self.performance.candidate.team.update_score(self.score, True)
		#update performance
		if self.performance:
			self.performance.update_score(self.score, True)
		return super(PerformanceScore, self).save(*args, **kwargs)





