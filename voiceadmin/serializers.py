from rest_framework import serializers
from .models import Candidate, Team, Mentor, Performance, PerformanceScore
from django.urls import reverse


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    mentor = serializers.SerializerMethodField()
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Candidate
        fields = ('id', 'last_name', 'team', 'team_name', 'mentor', 'average_score')

    def get_mentor(self, obj):
        return obj.team.mentor.__unicode__()


class TeamSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    web_url = serializers.SerializerMethodField()
    members = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'url', 'name', 'mentor', 'mentor_name', 'members', 'average_score', 'web_url')

    def get_mentor_name(self, obj):
        if obj.mentor:
    	   return obj.mentor.__unicode__()

    def get_web_url(self, obj):
        return reverse('team', args=[obj.pk])


class MentorSerializer(serializers.HyperlinkedModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = ('last_name', 'other_names', 'teams')


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Performance
        fields = ('song', 'date', 'candidate', 'average_score', 'url')


class PerformanceScoreSerializer(serializers.HyperlinkedModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    class Meta:
        model = PerformanceScore
        fields = ('performance', 'score', 'mentor_name', 'mentor')

    def get_mentor_name(self, obj):
        if obj.mentor:
           return obj.mentor.__unicode__()
