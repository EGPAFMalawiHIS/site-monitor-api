# Author name       :   Joel Kumwenda
# Phone             :   +8615922015417
# Email             :   joel@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-09-14

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class User_Manager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an username')
        user = self.model(email=email,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email, password=password,)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password,)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=60, blank=False, null=False)
    last_name = models.CharField(max_length=60, blank=False, null=False)
    image_url = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(max_length=60, blank=False, unique=False)
    email = models.EmailField(
                verbose_name='email address', max_length=60,
                blank=True, unique=True)
    phone = models.CharField(
                verbose_name='phone number', max_length=60,
                blank=True, unique=False)
    active = models.BooleanField(default=False)
    # Admin user; non super-user
    staff = models.BooleanField(default=False)
    # Superuser
    admin = models.BooleanField(default=False)
    # verification_code = models.CharField(
    #                         max_length=10, blank=False, null=False)
    # expiration_time = models.DateTimeField(blank=True, null=True)
    is_verified = models.PositiveSmallIntegerField(default=0)
    # Notice the absence of a "Password field", that's built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = User_Manager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

    class Meta:
        managed = True
        db_table = 'users'

class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'districts'

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=60, unique=True)
    district_id = models.ForeignKey('District', models.DO_NOTHING)
    longitude = models.CharField(max_length=60)
    latitude = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'sites'


class Monitor(models.Model):
    monitor_id = models.AutoField(primary_key=True, unique=True)
    status = models.IntegerField(blank=True, null=True)
    sitecode = models.ForeignKey(Site, related_name='site', to_field="code", db_column="sitecode", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'monitors'

'''
class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=60)
    code = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'languages'


class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'countries'


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'locations'


class Institutions(models.Model):
    institution_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'institutions'


class Joints(models.Model):
    joint_id = models.IntegerField(primary_key=True)
    api_key = models.CharField(max_length=60)
    is_active = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'joints'


class InjuryTypes(models.Model):
    injury_type_id = models.IntegerField(primary_key=True)
    joint = models.ForeignKey('Joints', models.DO_NOTHING)
    injury_type = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'injury_types'


class SurgeryTypes(models.Model):
    surgery_type_id = models.IntegerField(primary_key=True)
    surgery_name = models.CharField(max_length=100)
    joint = models.ForeignKey(Joints, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'surgery_types'


class VerificationCodeTypes(models.Model):
    type_id = models.IntegerField(primary_key=True)
    api_key = models.CharField(
                unique=True, max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'verification_code_types'


class DeviceTypes(models.Model):
    device_type_id = models.BigAutoField(primary_key=True)
    api_key = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'device_types'


class Devices(models.Model):
    device_id = models.BigAutoField(primary_key=True)
    device_mac = models.CharField(max_length=20)
    serial_number = models.CharField(
                        unique=True, max_length=60, blank=True, null=True)
    manufacturing_date = models.DateTimeField(blank=True, null=True)
    device_type = models.ForeignKey(DeviceTypes, models.DO_NOTHING)
    device_name = models.CharField(max_length=120)
    auth_key = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = True
        db_table = 'devices'


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    api_key = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'roles'


class Permissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    api_key = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'permissions'


class RolePermissions(models.Model):
    role_permission_id = models.BigAutoField(unique=True, primary_key=True)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'role_permissions'


class EMRs(models.Model):
    emr_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    country = models.ForeignKey(Countries, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=60, unique=True)
    api_url = models.CharField(max_length=100)
    api_key = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = True
        db_table = 'emrs'


class Hospitals(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    location = models.ForeignKey(
                'Locations', models.DO_NOTHING, blank=True, null=True)
    emr = models.ForeignKey(EMRs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hospitals'


class Professionals(models.Model):
    professional_id = models.AutoField(primary_key=True)
    pid = models.CharField(unique=True, blank=True, null=True, max_length=60)
    dob = models.CharField(max_length=60, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    years_of_pratice = models.CharField(max_length=11)
    degree = models.CharField(max_length=109, blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)
    emr = models.ForeignKey(EMRs, models.DO_NOTHING, blank=True, null=True)
    hospital = models.ForeignKey(Hospitals, models.DO_NOTHING)
    language = models.ForeignKey(Languages, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'professionals'


class UserRoles(models.Model):
    user_role_id = models.BigAutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'user_roles'


class ProfessionalDevices(models.Model):
    professional_device_id = models.AutoField(primary_key=True)
    assignment_date = models.DateField()
    device = models.ForeignKey(Devices, models.DO_NOTHING)
    professional = models.ForeignKey(Professionals, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'professional_devices'


class TextTypes(models.Model):
    text_type_id = models.AutoField(primary_key=True)
    api_key = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'text_types'


class Descriptions(models.Model):
    description_id = models.BigAutoField(unique=True, primary_key=True)
    text_type = models.ForeignKey(TextTypes, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'descriptions'


class Locales(models.Model):
    locale_key = models.CharField(primary_key=True, max_length=5)

    class Meta:
        managed = True
        db_table = 'locales'


class DescriptionLocales(models.Model):
    description = models.ForeignKey(Descriptions, models.DO_NOTHING)
    locale_key = models.ForeignKey(
                    Locales, models.DO_NOTHING, db_column='locale_key')
    description_value = models.CharField(max_length=250)

    class Meta:
        managed = True
        db_table = 'description_locales'
        unique_together = (('description', 'locale_key'),)


class Reps(models.Model):
    rap_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'reps'


class Sets(models.Model):
    set_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'sets'


class RepsSets(models.Model):
    rap_set_id = models.BigAutoField(primary_key=True)
    rep = models.ForeignKey(Reps, on_delete=models.CASCADE)
    sets = models.ForeignKey(Sets, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reps_sets'
        unique_together = (('rep', 'sets'),)


class Exercises(models.Model):
    exercise_id = models.BigAutoField(primary_key=True)
    file_id = models.CharField(max_length=36)
    name_description = models.ForeignKey(
                    Descriptions, models.DO_NOTHING, blank=True, null=True)
    holding_time = models.IntegerField(blank=True, null=True)
    reps_sets = models.ForeignKey(
                    RepsSets, models.DO_NOTHING, blank=True, null=True)
    rom_records = models.ForeignKey(
                    'RomRecords', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'exercises'


class PartOfDay(models.Model):
    part_of_day_id = models.IntegerField(primary_key=True)
    api_key = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'part_of_day'


class ProgramExercises(models.Model):
    program_exercise_id = models.BigAutoField(primary_key=True)
    program_period = models.ForeignKey('ProgramPeriods', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING)
    sets = models.IntegerField(blank=True, null=True)
    repetitions = models.IntegerField(blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    part_of_day = models.ForeignKey(PartOfDay, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'program_exercises'


class Executions(models.Model):
    execution_id = models.BigAutoField(primary_key=True)
    program_exercise = models.ForeignKey(ProgramExercises, models.DO_NOTHING)
    date = models.DateTimeField(blank=True, null=True)
    feedback = models.CharField(max_length=250, blank=True, null=True)
    duration_in_sec = models.IntegerField()
    extension = models.IntegerField()
    flexure = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'executions'
        unique_together = (('program_exercise', 'date'),)


class ExecutionProgress(models.Model):
    execution_progress_id = models.BigAutoField(primary_key=True)
    execution = models.ForeignKey('Executions', models.DO_NOTHING)
    set_number = models.IntegerField()
    repetition_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'execution_progress'


class FlywaySchemaHistory(models.Model):
    installed_rank = models.IntegerField(primary_key=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    script = models.CharField(max_length=1000)
    checksum = models.IntegerField(blank=True, null=True)
    installed_by = models.CharField(max_length=100)
    installed_on = models.DateTimeField()
    execution_time = models.IntegerField()
    success = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'flyway_schema_history'


class Patients(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    email = models.CharField(
                unique=True, max_length=60, blank=True, null=True)
    phone = models.CharField(
                unique=True, max_length=60, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(
                Genders, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(
                Countries, on_delete=models.CASCADE, blank=True, null=True)
    email_is_verified = models.IntegerField(blank=True, null=True)
    phone_is_verified = models.IntegerField(blank=True, null=True)
    registration_is_completed = models.IntegerField(blank=True, null=True)
    ethnicity = models.CharField(max_length=60, blank=True, null=True)
    weight_unit = models.CharField(max_length=10, blank=True, null=True)
    height_unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patients'


class PatientDevices(models.Model):
    patient_device_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(
                Patients, models.DO_NOTHING, blank=True, null=True)
    device = models.ForeignKey(
                Devices, models.DO_NOTHING, blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)
    setup_min = models.IntegerField(blank=True, null=True)
    setup_max = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    joint = models.ForeignKey(
                Joints, models.DO_NOTHING, blank=True, null=True)
    right_side = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient_devices'
        unique_together = (('patient', 'device'),)


class PatientDiseases(models.Model):
    patient_disease_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    right_side = models.IntegerField()
    disease_name = models.CharField(max_length=255, blank=True, null=True)
    joint = models.ForeignKey(Joints, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'patient_diseases'


class PatientInjuries(models.Model):
    patient_injury_id = models.BigAutoField(primary_key=True)
    patient_disease = models.ForeignKey(
                        PatientDiseases, models.DO_NOTHING)
    injury_type = models.ForeignKey(InjuryTypes, models.DO_NOTHING)
    injury_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient_injuries'


class PatientSurgeries(models.Model):
    patient_surgery_id = models.BigAutoField(primary_key=True)
    patient_disease = models.ForeignKey(PatientDiseases, models.DO_NOTHING)
    surgery_type = models.ForeignKey(SurgeryTypes, models.DO_NOTHING)
    surgery_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient_surgeries'


class VerificationCodes(models.Model):
    verification_code_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(
                Patients, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey(
            VerificationCodeTypes, models.DO_NOTHING, blank=True, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    expiration_time = models.DateTimeField()
    value = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'verification_codes'


class ProfessionalPatients(models.Model):
    professional_patient_id = models.BigAutoField(primary_key=True)
    professional = models.ForeignKey(Professionals, models.DO_NOTHING)
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    assignment_code = models.CharField(max_length=8)
    assignment_date = models.DateField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'professional_patients'


class TreatmentPrograms(models.Model):
    program_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    professional = models.ForeignKey(
                    Professionals, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    is_deleted = models.IntegerField()
    joint = models.ForeignKey(Joints, models.DO_NOTHING)
    right_side = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'treatment_programs'


class ProgramPeriods(models.Model):
    program_period_id = models.BigAutoField(primary_key=True)
    treatment_program = models.ForeignKey(
                            TreatmentPrograms, models.DO_NOTHING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'program_periods'


class QuestionTypes(models.Model):
    question_type_id = models.IntegerField(primary_key=True)
    question_type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'question_types'


class Questions(models.Model):
    question_id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=300)
    max_value = models.IntegerField(blank=True, null=True)
    question_type = models.ForeignKey(QuestionTypes, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'questions'


class Proms(models.Model):
    prom_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    professional = models.ForeignKey(Professionals, models.DO_NOTHING)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'proms'


class PromQuestions(models.Model):
    prom_question_id = models.BigAutoField(primary_key=True)
    prom = models.ForeignKey(Proms, models.DO_NOTHING)
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    question_order = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'prom_questions'
        unique_together = (('prom', 'question'),)


class PromAnswers(models.Model):
    prom_answer_id = models.BigAutoField(primary_key=True)
    prom_question = models.ForeignKey(PromQuestions, models.DO_NOTHING)
    date = models.DateField()
    value = models.IntegerField(blank=True, null=True)
    text_answer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'prom_answers'
        unique_together = (('prom_question', 'date'),)


class RomRecords(models.Model):
    rom_record_id = models.BigAutoField(primary_key=True)
    patient_device = models.ForeignKey(
                        PatientDevices, models.DO_NOTHING,
                        blank=True, null=True)
    record_date = models.DateTimeField(blank=True, null=True)
    min = models.IntegerField(blank=True, null=True)
    max = models.IntegerField(blank=True, null=True)
    rtc = models.IntegerField(blank=True, null=True)
    steps = models.IntegerField(blank=True, null=True)
    application_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'rom_records'


class AdminComments(models.Model):
    admin_comment_id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    comment_date = models.DateTimeField()
    professional = models.ForeignKey(Professionals, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'admin_comments'


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    comment_date = models.DateTimeField()
    patient = models.ForeignKey(Patients, models.DO_NOTHING)
    professional = models.ForeignKey(Professionals, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'comments'
'''