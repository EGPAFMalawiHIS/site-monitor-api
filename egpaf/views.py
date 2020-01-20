# Author name       :   Joel Kumwenda
# Phone             :   +8615922015417
# Email             :   joel@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-07-13

from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from rest_framework import filters, request, generics, status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from titlecase import titlecase
from twilio.rest import Client
from .emr_services import *
from .helper_services import *
from .models import *
from .permissions import PublicEndpoint
from .serializer import *
from .view_services import *
from datetime import timedelta,datetime
from celery.decorators import task
from celery.utils.log import get_task_logger




def index(request):
    context = {'latest_question_list': ''}
    return render(request, 'frontend/index.html', context)


#class ProfessionalVerificationViewSet(viewsets.ModelViewSet):
#    def list(self, request):
#        data = ProfesionalVerification.verifyProfessional(self, request.GET)
#        return Response(data)


def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: http://stackoverflow.com/a/1551394/141084
    """
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        raise ValueError('invalid date %s of type %s' % (time, type(time)))
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(round(second_diff)) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( round(second_diff / 60 )) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( round(second_diff / 3600 )) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(round(day_diff)) + " days ago"
    if day_diff < 31:
        return str(round(day_diff/7)) + " weeks ago"
    if day_diff < 365:
        return str(round(day_diff/30)) + " months ago"
    return str(round(day_diff/365)) + " years ago"

def pushToSocket():
    this_hour = timezone.now()
    one_hour_later = this_hour + timedelta(hours=1)

    sites_queryset = Site.objects.all()
    data = []
    for site in  sites_queryset.iterator():
        queryset = Monitor.objects.filter(created_at__range=(this_hour, one_hour_later),sitecode=site.code)
        #print(queryset)
        querysetb = Monitor.objects.filter(sitecode=site.code).order_by('-created_at')
        
        if len(queryset) > 0:
            if len(querysetb)>0:
                print('last_seen:',time_ago(querysetb[0].created_at))
                data.append({'district':site.district_id.name,
                            'site':site.name,
                            'code':site.code,
                            'status':1,
                            'last_seen': time_ago(querysetb[0].created_at)})
        else:
            if len(querysetb)>0:
                data.append({'district':site.district_id.name,
                                'site':site.name,
                                'code':site.code,
                                'status':1,
                                'last_seen': time_ago(querysetb[0].created_at)})
            else:
                data.append({'district':site.district_id.name,
                                'site':site.name,
                                'code':site.code,
                                'status':0,
                                'last_seen': 'Never'})
    print(data)
    

class ForgotPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = UserFilter.checkEmail(
                    self, queryset, self.request.query_params.get('email'))
        return data


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (PublicEndpoint,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = FilterUser.get_user(
            self,
            queryset,
            self.request.query_params.get('username'))
        return data


class UserPhoneViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPhoneSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = CreateUser.add_new_user(
            self, queryset,
            self.request.query_params.get('username'),
            self.request.query_params.get('phone'),
            self.request.query_params.get('email'),
            self.request.query_params.get('password'))
        return data


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UserPasswordViewSet(viewsets.ModelViewSet):
    permission_classes = (PublicEndpoint,)
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class SiteSaveViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSaveSerializer

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer


class MonitorBViewSet(viewsets.ModelViewSet):
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    one_hour_later = this_hour + timedelta(hours=1)
    queryset = Monitor.objects.filter(created_at__range=(this_hour, one_hour_later))
    serializer_class = MonitorBSerializer

class MonitorCViewSet(viewsets.ModelViewSet):

    serializer_class = MonitorCSerializer

    def get_queryset(self):
        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        one_hour_later = this_hour + timedelta(hours=1)
        sites_queryset = Site.objects.all()
        data = []
        for site in  sites_queryset.iterator():
            queryset = Monitor.objects.filter(created_at__range=(this_hour, one_hour_later),sitecode=site.code)
            querysetb = Monitor.objects.filter(sitecode=site.code).order_by('-created_at')
            
            if len(queryset) > 0:
                if len(querysetb)>0:
                    print('last_seen:',time_ago(querysetb[0].created_at))
                    data.append({'district':site.district_id.name,
                                'site':site.name,
                                'code':site.code,
                                'status':1,
                                'last_seen': time_ago(querysetb[0].created_at),
                                'longitude':site.longitude,
                                'latitude':site.latitude})
            else:
                if len(querysetb)>0:
                    data.append({'district':site.district_id.name,
                                    'site':site.name,
                                    'code':site.code,
                                    'status':0,
                                    'last_seen': time_ago(querysetb[0].created_at),
                                    'longitude':site.longitude,
                                    'latitude':site.latitude})
                else:
                    data.append({'district':site.district_id.name,
                                    'site':site.name,
                                    'code':site.code,
                                    'status':0,
                                    'last_seen': 'Never',
                                    'longitude':site.longitude,
                                    'latitude':site.latitude})
        return data


