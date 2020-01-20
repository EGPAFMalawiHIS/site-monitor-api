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


class Email(object):
    def send_email(self, mail):
        subject = mail['subject']
        message = mail['message']
        from_email = mail['from_email']
        to_email = mail['to_email']
        # print('Here from')
        # print(from_email)
        # print('Here TO')
        # print(to_email)
        print ("Here from %s to %s " % (from_email, to_email))

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

    def verificationMail(self, email, code):
        subject = "No Reply"
        message = "Herewith your Email Verification Code for Rombot: " + code
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        return ({
                    'subject': subject,
                    'message': message,
                    'from_email': from_email,
                    'to_email': to_email})


class SMS(object):
    def send_text(self, text):
        client = Client(
                    settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        phone = text['to_phone']
        text = text['text']

        if phone is not None:
            try:
                message = client.messages.create(
                            to=phone, from_='+16082086194', body=text)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

    def verificationText(self, phone, code):
        text = "Rombot Verification Code: " + code
        to_phone = phone
        return ({'text': text, 'to_phone': to_phone})


class VerificationCode(object):
    def generate_multiple(self, unique):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        while True:
            value = "".join(random.choice(chars) for _ in range(5))
            if value not in unique:
                unique.add(value)
                break

    def generate(self):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        value = "".join(random.choice(chars) for _ in range(6))
        return value


class VerificationExpiration():
    def expiration_time(self):
        return (
                datetime.now()
                + timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M')
