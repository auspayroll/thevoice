from django.core.management.base import BaseCommand, CommandError
from voiceadmin.models import *
from django.contrib.auth.models import User, Group
from random import randint
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.hashers import make_password


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

class Command(BaseCommand):
    help = 'Initalize data'

    def handle(self, *args, **options):
            PerformanceScore.objects.all().delete()
            Performance.objects.all().delete()
            Candidate.objects.all().delete()
            Team.objects.all().delete()

            admin_group, _ = Group.objects.get_or_create(name='admin')
            mentor_group, _ = Group.objects.get_or_create(name='mentor')
            candidate_group, _ = Group.objects.get_or_create(name='candidate')

            admin_user, _ = User.objects.update_or_create(username='admin', defaults=dict(email='admin@gmail.com', first_name="John", 
                is_staff=True, last_name='Doe', password=make_password('password')))
            self.stdout.write("admin username: admin, password: password")
            admin_user.groups.add(admin_group)         
            
            teams = []
            mentors = []
            for mentor_name, team_name in mentor_teams.items():
                try:
                    first, second = mentor_name.split(' ')
                except:
                    second = mentor_name
                    first = ''

                m , _ = Mentor.objects.update_or_create(last_name=second, other_names=first)
                mentors.append(m)

                team, _ = Team.objects.update_or_create(name=team_name, mentor=m) 
                teams.append(team)

            #create a user from one of the mentors
            choose_mentor = choose(mentors)
            mentor_user, created = User.objects.update_or_create(username='mentor', defaults=dict(email='mentor@gmail.com', first_name=choose_mentor.other_names, 
                is_staff=True, last_name=choose_mentor.last_name, password=make_password('password')))
            self.stdout.write("Mentor username: mentor, password: password")
            if not created: # reset previous one-to-one mentor/user link
                Mentor.objects.filter(user=mentor_user).update(user=None)
    
            mentor_user.groups.add(mentor_group)   
            choose_mentor.user = mentor_user
            choose_mentor.save()

            candidates = []
            for i in range(50):
                candidate = Candidate.objects.create(last_name=choose(last_names), other_names=choose(first_names), team=choose(teams), dob=random_dob())
                candidates.append(candidate)
                performance = Performance.objects.create(song=choose(songs), candidate=candidate, date=random_date())
                for mentor in mentors:
                    PerformanceScore.objects.create(performance=performance, mentor=mentor, score=randint(1,100))

            #create a user from one of the mentors
            choose_candidate = choose(candidates)
            candidate_user, created = User.objects.update_or_create(username='candidate', defaults=dict(email='candidate@gmail.com', 
                first_name=choose_candidate.other_names, 
                is_staff=True, last_name=choose_candidate.last_name, password=make_password('password')))
            self.stdout.write("Mentor username: mentor, password: password")
            if not created: # reset previous one-to-one mentor/user link
                Candidate.objects.filter(user=candidate_user).update(user=None)
    
            candidate_user.groups.add(candidate_group)   
            choose_candidate.user = candidate_user
            choose_candidate.save()


            self.stdout.write(self.style.SUCCESS('Successfully initialized'))