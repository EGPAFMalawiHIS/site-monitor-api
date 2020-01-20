# Author name       :   Joel Kumwenda
# Phone             :   +8615922015417
# Email             :   joel@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-07-13

import random
from django.conf import settings
from djoser.serializers import (
        UserCreateSerializer as BaseUserRegistrationSerializer)
from django.db.models import Max
from rest_framework import serializers
# from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.validators import UniqueTogetherValidator
from .emr_services import *
from .helper_services import *
from .models import *
from .view_services import *

# # CREATE SERIALIZERS HERE ##


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'phone')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'],
                    phone=validated_data['phone'])  # added phone field.
        user.set_password(validated_data['password'])
        user.save()
        # Adding generated verification code to verification table
        Email.send_email(
                self,
                Email.verificationMail(self, validated_data['email'], 'code'))
        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                    email=validated_data['email'],
                    phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        code = VerificationCode.generate(self)
        # Adding generated verification code to verification table
        verify = VerificationCodes.objects.create(
                    code=code, value=code,
                    verification_type=validated_data['verification_type'])
        verify.save()
        verify.user.add(user)
        verify.save()
        code = verify.code
        return user


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                    username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Email.send_email(
            self,
            Email.verificationMail(self, validated_data['email'], 'code'))
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        code = VerificationCode.generate(self)
        expiration_time = VerificationExpiration.expiration_time(self)
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email'],
                    phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save(verification_code=code)
        user.save(expiration_time=expiration_time)
        user.save()

        if validated_data['verification_type'] == 1:
            Email.send_email(
                self,
                Email.verificationMail(self, validated_data['email'], code))
        elif validated_data['verification_type'] == 2:
            text = SMS.verificationText(self, validated_data['phone'], code)
            SMS.send_text(self, text)
        return user


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    district_id = DistrictSerializer(read_only=True)
    class Meta:
        model = Site
        fields = '__all__'

class SiteSaveSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Site
        fields = '__all__'

class MonitorSerializer(serializers.ModelSerializer):
#site = SiteSerializer(read_only=True) 

    site = SiteSerializer(read_only=True)
    
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorBSerializer(serializers.ModelSerializer):
#site = SiteSerializer(read_only=True) 

    sitecode = SiteSerializer(read_only=True)
    
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorCSerializer(serializers.Serializer):
    district = serializers.CharField(max_length=200)
    site = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)
    status = serializers.IntegerField()
    last_seen = serializers.CharField(max_length=200)
    longitude = serializers.CharField(max_length=200)
    latitude = serializers.CharField(max_length=200)

'''
    def create(self, validated_data):
        data = Monitor(status=validated_data['status'],sitecode=validated_data['sitecode'])
        data.save()
        return data


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class InstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institutions
        fields = '__all__'


class JointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joints
        fields = '__all__'


class InjuryTypesSerializer(serializers.ModelSerializer):
    joint = JointsSerializer(read_only=True)
    joint_data = serializers.PrimaryKeyRelatedField(
                    queryset=Joints.objects.all(),
                    write_only=True, source='joint')

    class Meta:
        model = InjuryTypes
        fields = '__all__'


class EMRsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMRs
        fields = '__all__'


class HospitalsSerializer(serializers.ModelSerializer):
    location = LocationsSerializer(read_only=True)
    location_data = serializers.PrimaryKeyRelatedField(
                        queryset=Locations.objects.all(),
                        write_only=True, source='location')

    class Meta:
        model = Hospitals
        fields = '__all__'


class VerificationCodeTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCodeTypes
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class RolePermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermissions
        fields = '__all__'


class ProfessionalsSerializer(serializers.ModelSerializer):
    role = RolesSerializer(read_only=True)
    role_data = serializers.PrimaryKeyRelatedField(
                    queryset=Roles.objects.all(),
                    write_only=True, source='role')

    language = LanguagesSerializer(read_only=True)
    language_data = serializers.PrimaryKeyRelatedField(
                        queryset=Languages.objects.all(),
                        write_only=True, source='language')

    hospital = HospitalsSerializer(read_only=True)
    hospital_data = serializers.PrimaryKeyRelatedField(
                        queryset=Hospitals.objects.all(),
                        write_only=True, source='hospital')

    emr = EMRsSerializer(read_only=True)
    emr_data = serializers.PrimaryKeyRelatedField(
                queryset=EMRs.objects.all(), write_only=True, source='emr')

    institution = InstitutionsSerializer(read_only=True)
    institution_data = serializers.PrimaryKeyRelatedField(
                        queryset=Institutions.objects.all(),
                        write_only=True, source='institution')

    user = UserSerializer(read_only=True)
    user_data = serializers.PrimaryKeyRelatedField(
                    queryset=User.objects.all(),
                    write_only=True, source='user')

    class Meta:
        model = Professionals
        fields = '__all__'


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'


class DeviceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTypes
        fields = '__all__'


class DevicesSerializer(serializers.ModelSerializer):
    device_type = DeviceTypesSerializer(read_only=True)
    device_type_data = serializers.PrimaryKeyRelatedField(
                        queryset=DeviceTypes.objects.all(),
                        write_only=True, source='device_type')

    class Meta:
        model = Devices
        exclude = ['auth_key']

    def create(self, validated_data):
        new_auth_key = False
        devices = Devices.objects.all()
        # if new_auth_key on the devices, generate another random number
        # if new_auth_key does not exist use the generated random number
        count = 0
        while not new_auth_key:
            # count =+ 1
            count += 1
            if count > 10:
                break

            auth_key = str(random.randint(1, 10**6 - 1))

            if len(auth_key) != 6:
                new_auth_key = False
                continue

            device = devices.filter(auth_key=auth_key)

            if not device:
                new_auth_key = True

        device = Devices(
                    device_type=validated_data['device_type'],
                    device_mac=validated_data['device_mac'],
                    serial_number=validated_data['serial_number'],
                    manufacturing_date=validated_data['manufacturing_date'],
                    device_name=validated_data['device_name'],
                    auth_key=auth_key,)

        device.save()

        return device


class PatientsSerializer(serializers.ModelSerializer):
    gender = GendersSerializer(read_only=True)
    gender_name = serializers.PrimaryKeyRelatedField(
                    queryset=Genders.objects.all(),
                    write_only=True, source='gender')

    country = CountriesSerializer(read_only=True)
    country_name = serializers.PrimaryKeyRelatedField(
                    queryset=Countries.objects.all(),
                    write_only=True, source='country')

    class Meta:
        model = Patients
        fields = '__all__'


class PatientDevicesSerializer(serializers.ModelSerializer):
    device = DevicesSerializer(read_only=True)
    device_data = serializers.PrimaryKeyRelatedField(
                    queryset=Devices.objects.all(),
                    write_only=True, source='device')

    patient = PatientsSerializer(read_only=True)
    patient_data = serializers.PrimaryKeyRelatedField(
                    queryset=Patients.objects.all(), write_only=True,
                    source='patient')

    joint = JointsSerializer(read_only=True)
    joint_data = serializers.PrimaryKeyRelatedField(
                    queryset=Joints.objects.all(),
                    write_only=True, source='joint')

    class Meta:
        model = PatientDevices
        fields = '__all__'


class ProfessionalPatientsSerializer(serializers.ModelSerializer):
    patient_id = PatientsSerializer(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(
                queryset=Patients.objects.all(),
                write_only=True, source='patient_id')
    professional_id = ProfessionalsSerializer(read_only=True)
    professional = serializers.PrimaryKeyRelatedField(
                    queryset=Professionals.objects.all(),
                    write_only=True, source='professional_id')

    class Meta:
        model = ProfessionalPatients
        fields = '__all__'


class ProfessionalDevicesSerializer(serializers.ModelSerializer):
    device_id = DevicesSerializer(read_only=True)
    device = serializers.PrimaryKeyRelatedField(
                queryset=Devices.objects.all(),
                write_only=True, source='device_id')

    class Meta:
        model = ProfessionalDevices
        fields = '__all__'


class VerificationCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCodes
        fields = '__all__'


class SurgeryTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgeryTypes
        fields = '__all__'


class PatientDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiseases
        fields = '__all__'


class PatientSurgeriesSerializer(serializers.ModelSerializer):
    surgery_type = SurgeryTypesSerializer(read_only=True)
    surgery_type_data = serializers.PrimaryKeyRelatedField(
                            queryset=SurgeryTypes.objects.all(),
                            write_only=True, source='surgery_type')
    patient_disease = PatientDiseasesSerializer(read_only=True)
    patient_disease_data = serializers.PrimaryKeyRelatedField(
                                queryset=PatientDiseases.objects.all(),
                                write_only=True,
                                source='patient_disease')

    class Meta:
        model = PatientSurgeries
        fields = '__all__'


class PatientInjuriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInjuries
        fields = '__all__'


class RomRecordsSerializer(serializers.ModelSerializer):
    patient_device = PatientDevicesSerializer(read_only=True)
    patient_device_data = serializers.PrimaryKeyRelatedField(
                            queryset=PatientDevices.objects.all(),
                            write_only=True, source='patient_device')

    class Meta:
        model = RomRecords
        fields = '__all__'


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCodes
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class TextTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTypes
        fields = '__all__'


class DescriptionsSerializer(serializers.ModelSerializer):
    text_type = TextTypesSerializer(read_only=True)
    text_type_data = serializers.PrimaryKeyRelatedField(
                        queryset=TextTypes.objects.all(),
                        write_only=True, source='text_type')

    class Meta:
        model = Descriptions
        fields = '__all__'


class AdminCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminComments
        fields = '__all__'


class RepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reps
        fields = '__all__'


class SetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sets
        fields = '__all__'


class RepsSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepsSets
        fields = '__all__'

    rep = RepsSerializer(read_only=True)
    rep_data = serializers.PrimaryKeyRelatedField(
                queryset=Reps.objects.all(),
                write_only=True, source='rep')

    sets = SetsSerializer(read_only=True)
    sets_data = serializers.PrimaryKeyRelatedField(
                    queryset=Sets.objects.all(),
                    write_only=True, source='sets')


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = '__all__'

    reps_sets = RepsSetsSerializer(read_only=True)
    reps_sets_data = serializers.PrimaryKeyRelatedField(
                        queryset=RepsSets.objects.all(),
                        write_only=True, source='reps_sets')

    rom_records = RomRecordsSerializer(read_only=True)
    rom_records_data = serializers.PrimaryKeyRelatedField(
                        queryset=RomRecords.objects.all(),
                        write_only=True, source='rom_records')


class LocalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locales
        fields = '__all__'


class DescriptionLocalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionLocales
        fields = '__all__'


class PartOfDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfDay
        fields = '__all__'


class ExecutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executions
        fields = '__all__'


class ExecutionProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionProgress
        fields = '__all__'


class FlywaySchemaHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlywaySchemaHistory
        fields = '__all__'


class TreatmentProgramsSerializer(serializers.ModelSerializer):
    patient = PatientsSerializer(read_only=True)
    patient_name = serializers.PrimaryKeyRelatedField(
                    queryset=Patients.objects.all(),
                    write_only=True, source='patient')
    joint = JointsSerializer(read_only=True)
    joint_name = serializers.PrimaryKeyRelatedField(
                    queryset=Joints.objects.all(),
                    write_only=True, source='joint')

    class Meta:
        model = TreatmentPrograms
        fields = '__all__'


class ProgramPeriodsSerializer(serializers.ModelSerializer):
    treatment_program = TreatmentProgramsSerializer(read_only=True)
    program = serializers.PrimaryKeyRelatedField(
                queryset=TreatmentPrograms.objects.all(),
                write_only=True, source='treatment_program')

    class Meta:
        model = ProgramPeriods
        fields = '__all__'


class ProgramExercisesSerializer(serializers.ModelSerializer):
    program_period = ProgramPeriodsSerializer(read_only=True)
    program_period_name = serializers.PrimaryKeyRelatedField(
                            queryset=ProgramPeriods.objects.all(),
                            write_only=True, source='program_period')
    exercise = ExercisesSerializer(read_only=True)
    exercise_name = serializers.PrimaryKeyRelatedField(
                        queryset=Exercises.objects.all(),
                        write_only=True, source='exercise')

    class Meta:
        model = ProgramExercises
        fields = '__all__'


class QuestionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTypes
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'


class PromsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proms
        fields = '__all__'


class PromQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromQuestions
        fields = '__all__'


class PromAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromAnswers
        fields = '__all__'
'''