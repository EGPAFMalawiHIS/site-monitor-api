# Author name       :   Joel
# Phone             :   +8615922015417
# Email             :   charlie@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-07-13

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


# User filter service class
class FilterUser(object):
    def get_user(self, queryset, username):
        if username is not None:
            code_result = queryset.filter(username=username)
            if code_result.exists():
                return code_result
            else:
                raise APIException({
                    'code': 'username code not available', 'status_code': 0})
        else:
            return queryset


# Verification code service class
class FilterVerificationCode(object):
    def get_verification_code(self, queryset, verification_code):
        if verification_code is not None:
            code_result = queryset.filter(code=verification_code)
            if code_result is not None:
                return code_result
            else:
                return [{
                        'code': 'Verification code not available',
                        'status_code': 0}]
        else:
            return queryset


# Device service class
class FilterDevice(object):
    def get_device(
            self, devices_queryset, patient_devices_queryset, device_name):
        if device_name is not None:
            device = devices_queryset.filter(device_name=device_name)
            if device.exists():
                patient_device = patient_devices_queryset.filter(
                                    device_id=device[0])
                if patient_device.exists():
                    return [{
                            'serial_number': 'Device Already Assigned',
                            'status_code': 3}]
                else:
                    return [{
                            'device_id': device[0].device_id,
                            'serial_number': 'Device is available',
                            'status_code': 2}]
            else:
                return [{'serial_number': 'Device not registered',
                        'status_code': 0}]
        else:
            return devices_queryset


# Patient registration service class
class FilterRegistrationMethod(object):
    def registration_method(self, queryset, email, phone):
        if email is not None:
            queryset = queryset.filter(email=email)
            return queryset
        elif phone is not None:
            queryset = queryset.filter(phone=phone)
            return queryset


# Surgeries service class
class FilterPatientSurgeries(object):
    def get_patient_surgeries(self, queryset, patient_id):
        if patient_id is not None:
            surgeries = queryset.filter(
                                patient_id=patient_id).order_by(
                                        '-patient_surgery_id')[:1]
            if surgeries.exists():
                return surgeries
            else:
                raise APIException("Patient surgeries not found !")
        else:
            return queryset


# Injuries service class
class FilterPatientInjuries(object):
    def get_patient_injuries(self, queryset, patient_id):
        if patient_id is not None:
            injuries = queryset.filter(patient_id=patient_id)
            if injuries.exists():
                return injuries
            else:
                raise APIException("Patient injuries not found !")
        else:
            return queryset


# Patient devices service class
class FilterPatientDevices(object):
    def get_patient_devices(self, queryset, patient_id):
        if patient_id is not None:
            patient_devices = queryset.filter(
                                    patient_id=patient_id).order_by(
                                            '-patient_device_id')[:1]
            if patient_devices.exists():
                return patient_devices
            else:
                raise APIException("Patient devices not found !")
        else:
            return queryset


# Patient service class
class FilterPatient(object):
    def get_patient(self, queryset, user_id, patient_id):
        if user_id is not None:
            patient = queryset.filter(user_id=user_id)
            if patient.exists():
                return patient
            else:
                raise APIException("Patient with user id not found !")
        elif patient_id is not None:
            patient = queryset.filter(patient_id=patient_id)
            if patient.exists():
                return patient
            else:
                raise APIException("Patient not found !")
        else:
            return queryset


# ROM Records service class
class FilterPatientRomRecords(object):
    def get_patient_rom_records(
            self, queryset, patient_id, patient_device_id, record_type):
        if patient_id and record_type is not None:
            if record_type == 'pre':
                rom_record = queryset.select_related(
                        'patient_device_id').filter(
                            patient_device_id__patient_id=patient_id).filter(
                                record_type_id=1)[:1]
            elif record_type == 'post':
                rom_record = queryset.select_related(
                        'patient_device_id').filter(
                            patient_device_id__patient_id=patient_id).filter(
                                record_type_id=2)[:1]
            elif record_type == 'current':
                rom_record = queryset.select_related(
                        'patient_device_id').order_by(
                            '-record_date').filter(
                                patient_device_id__patient_id=patient_id)[:1]
            else:
                raise APIException("pre post record not found !")

            if rom_record.exists():
                return rom_record
            else:
                raise APIException("pre post record not found !")

        elif patient_id is not None:
            patient = queryset.select_related(
                    'patient_device_id').filter(
                        patient_device_id__patient_id=patient_id).filter(
                            record_type_id=3)
            if patient.exists():
                return patient
            else:
                raise APIException("ROM record not found !")

        elif patient_device_id is not None:
            patient = queryset.filter(patient_device_id=patient_device_id)

            if patient.exists():
                return patient
        else:
            return queryset


# Patient Comments service class
class FilterPatientComments(object):
    def get_patient_comments(self, queryset, patient_id):
        if patient_id is not None:
            comments = queryset.filter(patient_id=patient_id)
            if comments.exists():
                return comments
            else:
                raise APIException("Patient comments not found !")
        else:
            return queryset


# Professional Comments service class
class FilterAdminComments(object):
    def get_admin_comments(self, queryset, professional_id):
        if professional_id is not None:
            comments = queryset.filter(professional_id=professional_id)
            if comments.exists():
                return comments
            else:
                raise APIException("Profession comments not found !")
        else:
            return queryset


# Professional patients class
class FilterProfessionalPatients(object):
    def get_professional_patients(
            self, queryset, pro_devices_queryset, professional_id):
        if professional_id is not None:
            professional_patients = queryset.filter(
                                        professional_id=professional_id)
            if professional_patients.exists():
                return professional_patients
            else:
                raise APIException("Patients not found !")
        else:
            return queryset


# Professional patients class
class FilterProfessional(object):
    def get_professional(self, queryset, user_id):
        if user_id is not None:
            professional = queryset.filter(user_id=user_id)[:1]
            if professional.exists():
                return professional
            else:
                raise APIException("Professional with user id not found !")
        else:
            return queryset


# Professional service class
class FilterProfessionalDevices(object):
    def get_professional_devices(self, queryset, professional_id):
        if professional_id is not None:
            professional_devices = queryset.filter(
                                    professional_id=professional_id)
            if professional_devices.exists():
                return professional_devices
            else:
                raise APIException("Devices not found !")
        else:
            return queryset


class CreateUser(object):
    def add_new_user(self, queryset, username, phone, email, password):
        if phone is not None:
            queryset.create(username=username, phone=phone, password=password)
            return queryset
        elif email is not None:
            raise APIException("Email registration !")


# search user/check by attributes/column
class UserFilter(object):
    def checkEmail(self, queryset, email):
        if email is not None:
            user = queryset.filter(email=email)
            if user.exists():
                return user
            else:
                raise APIException("Record Not Found !")
        else:
            raise APIException("Blank Email")


class VerificationType(object):
    def check_verification_type(self, user):
        verification_type = 1
        if user.phone:
            verification_type = 2
        else:
            verification_type = 1
        return verification_type


class FilterEMR(object):
    def get_user_emr(self, queryset, filter):
        country = filter.get('country')
        role = filter.get('role')
        if country and role is not None:
            emr_record = queryset.filter(
                            country=filter.get('country'),
                            role=filter.get('role'))
            if emr_record.exists():
                return emr_record
            else:
                raise APIException('EMR record not found!')
        else:
            return queryset
