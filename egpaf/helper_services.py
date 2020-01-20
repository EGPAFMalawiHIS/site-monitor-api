# Author name       :   Charlie
# Phone             :   +8615922015417
# Email             :   charlie@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-07-13

import json
import requests
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from twilio.rest import Client
from .models import *



