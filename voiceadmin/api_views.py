from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Candidate, Team, Mentor, Performance, PerformanceScore
from .serializers import CandidateSerializer, TeamSerializer, PerformanceSerializer, PerformanceScoreSerializer, MentorSerializer
from rest_framework import generics, permissions




@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def team_search(request):
    search = request.GET.get('search')
    if search:
        teams = Team.objects.filter(name__icontains=request.GET.get('search'))
    else:
        teams = Team.objects.all()
    serializer_context = {'request': Request(request)}
    serializer = TeamSerializer(teams, many=True, context=serializer_context)
    return Response(serializer.data)


class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PerformanceList(generics.ListCreateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class PerformanceScoreList(generics.ListCreateAPIView):
    queryset = PerformanceScore.objects.all()
    serializer_class = PerformanceScoreSerializer


class PerformanceScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerformanceScore.objects.all()
    serializer_class = PerformanceScoreSerializer


class MentorList(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class MentorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer