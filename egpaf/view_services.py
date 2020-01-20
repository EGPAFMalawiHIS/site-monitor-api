

import json
import requests
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from twilio.rest import Client
from .models import *



