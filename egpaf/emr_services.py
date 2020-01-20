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


# Verify professional record with EMR
class ProfesionalVerification(object):
    def verifyProfessional(self, professional_data):
        emr_id = professional_data.get('emr_id')
        emr_record = EMRs.objects.get(emr_id=emr_id)
        slug = emr_record.slug

        if slug == 'better_doctor':
            data = BetterDoctor.search_doctor(
                    self, professional_data, emr_record)

        elif slug == 'china_emr':
            data = ChinaEMR.search_doctor(
                    self, professional_data, emr_record)

        return data


# Better Doctor EMR good for USA Doctors
class BetterDoctor(object):
    def search_doctor(self, doctor_data, emr_record):
        fname = doctor_data.get('first_name')
        lname = doctor_data.get('last_name')
        baseurl = emr_record.api_url
        key = emr_record.api_key
        request_url = (
                        baseurl + '/'
                        + str(datetime.datetime.now().year)
                        + '-03-01/doctors/?fields=profile,uid,'
                        + 'specialties&first_name=' + fname
                        + '&last_name=' + lname + '&user_key=' + key)
        doctor_records = BetterDoctor.retrieve_data(self, request_url)

        if doctor_records['data'] != '':
            first_name = doctor_records['data'][0]['profile']['first_name']
            last_name = doctor_records['data'][0]['profile']['last_name']
            if first_name == fname and last_name == lname:
                doctor_record = BetterDoctor.find(
                    self,
                    lambda record: record['profile']['first_name'] == fname
                    and record['profile']['last_name'] == lname,
                    doctor_records['data'])

                return doctor_record
            else:
                return 'No record found!'
        else:
            return 'No record found'
        return doctor_records

    def retrieve_data(self, url):
        r = requests.get(url)
        items = r.json()
        return items

    def find(self, record, seq):
        for record_data in seq:
            if record(record_data):
                return record_data


class ChinaEMR(object):
    def search_doctor(self, doctor_data, emr_record):
        return "China EMR System"
