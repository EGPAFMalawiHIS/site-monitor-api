# Author name       :   Charlie
# Phone             :
# Email             :   charlie@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-09-13
# Modified by       :   Joel

import json
import requests
import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from twilio.rest import Client
from django.core.mail import send_mail



