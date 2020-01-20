# Author name       :   Joel Kumwenda
# Phone             :   +8615922015417
# Email             :   joel@rombot.com
# Date Created      :   2018-07-13
# Last modified     :   2018-07-13

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from egpaf import views as egpaf_views

# --- ROMBOT ROUTES --- #
router = routers.DefaultRouter()
router.register(r'user', egpaf_views.UserViewSet, base_name='User')
# User management
router.register(r'users', egpaf_views.UsersViewSet, base_name='Users')
router.register(r'user-password',
                egpaf_views.UserPasswordViewSet, base_name='UserPassword')
router.register(r'user_phone',
                egpaf_views.UserPhoneViewSet, base_name='UserPhone')
router.register(r'user_registration', egpaf_views.UserRegistrationViewSet,
                base_name='UserRegistration')

router.register(r'district', egpaf_views.DistrictViewSet,
                base_name='District')
router.register(r'site', egpaf_views.SiteViewSet,
                base_name='Site')

router.register(r'sitesave', egpaf_views.SiteSaveViewSet,
                base_name='SiteSave')

router.register(r'monitorsave', egpaf_views.MonitorViewSet,
                base_name='MonitorSave')

router.register(r'monitor', egpaf_views.MonitorBViewSet,
                base_name='Monitor')
router.register(r'monitorc', egpaf_views.MonitorCViewSet,
                base_name='MonitorC')



'''
router.register(r'genders',
                rombot_views.GendersViewSet, base_name="Genders")
router.register(r'languages',
                rombot_views.LanguagesViewSet, base_name='Languages')
router.register(r'countries',
                rombot_views.CountriesViewSet, base_name='Countries')
router.register(r'locations',
                rombot_views.LocationsViewSet, base_name='Locations')
router.register(r'institutions',
                rombot_views.InstitutionsViewSet, base_name='Institutions')
router.register(r'surgery_types',
                rombot_views.SurgeryTypesViewSet, base_name='SurgeryTypes')
router.register(r'joints',
                rombot_views.JointsViewSet, base_name='Joints')
router.register(r'injury_types',
                rombot_views.InjuryTypesViewSet, base_name='InjuryTypes')
router.register(r'emrs',
                rombot_views.EMRsViewSet, base_name='EMRs')
router.register(r'hospitals',
                rombot_views.HospitalsViewSet, base_name='Hospitals')
router.register(r'verification_code_types',
                rombot_views.VerificationCodeTypesViewSet,
                base_name='VerificationCodeTypes')
router.register(r'roles',
                rombot_views.RolesViewSet, base_name='Roles')
router.register(r'permissions',
                rombot_views.PermissionsViewSet, base_name='Permissions')
router.register(r'role_permissions',
                rombot_views.RolePermissionsViewSet,
                base_name='RolePermissions')
router.register(r'device_types',
                rombot_views.DeviceTypesViewSet, base_name='DeviceTypes')
router.register(r'devices',
                rombot_views.DevicesViewSet, base_name='Devices')
router.register(r'patients',
                rombot_views.PatientsViewSet, base_name='Patients')
router.register(r'professionals',
                rombot_views.ProfessionalsViewSet, base_name='Professionals')
router.register(r'user_roles',
                rombot_views.UserRolesViewSet, base_name='UserRoles')
router.register(r'verification_codes',
                rombot_views.VerificationCodesViewSet,
                base_name='VerificationCodes')
router.register(r'professional_patients',
                rombot_views.ProfessionalPatientsViewSet,
                base_name='ProfessionalPatients')
router.register(r'professional_devices',
                rombot_views.ProfessionalDevicesViewSet,
                base_name='ProfessionalDevices')
router.register(r'patient_surgeries', rombot_views.PatientSurgeriesViewSet,
                base_name='PatientSurgeries')
router.register(r'patient_injuries', rombot_views.PatientInjuriesViewSet,
                base_name='PatientInjuries')
router.register(r'patient_devices', rombot_views.PatientDevicesViewSet,
                base_name='PatientDevices')
router.register(r'rom_records',
                rombot_views.RomRecordsViewSet, base_name='RomRecords')
router.register(r'verification',
                rombot_views.VerificationViewSet, base_name='Verification')
router.register(r'comments',
                rombot_views.CommentsViewSet, base_name='Comments')
router.register(r'admin_comments',
                rombot_views.AdminCommentsViewSet, base_name='AdminComments')
router.register(r'professional_verification',
                rombot_views.ProfessionalVerificationViewSet,
                base_name='ProfessionalVerification')
router.register(r'forgot_password', rombot_views.ForgotPasswordViewSet,
                base_name='ForgotPassword')
router.register(r'program_periods', rombot_views.ProgramPeriodsViewSet,
                base_name='ProgramPeriods')
router.register(r'reps',
                rombot_views.RepsViewSet, base_name='Reps')
router.register(r'sets',
                rombot_views.SetsViewSet, base_name='Sets')
router.register(r'reps_sets',
                rombot_views.RepSetsViewSet, base_name='RepSets')
router.register(r'exercises',
                rombot_views.ExercisesViewSet, base_name='Exercises')
router.register(r'program_exercises', rombot_views.ProgramExercisesViewSet,
                base_name='ProgramExercises')
router.register(r'text_types',
                rombot_views.TextTypesViewSet, base_name='TextTypes')
router.register(r'descriptions',
                rombot_views.DescriptionsViewSet, base_name='Descriptions')
router.register(r'locales',
                rombot_views.Localesviewset, base_name='Locales')
router.register(r'description_locales',
                rombot_views.DescriptionLocalesViewset,
                base_name='DescriptionLocales')
router.register(r'part_of_day',
                rombot_views.PartOfDayViewset, base_name='PartOfDay')
router.register(r'executions',
                rombot_views.ExecutionsViewset, base_name='Executions')
router.register(r'execution_progress', rombot_views.ExecutionProgressViewset,
                base_name='ExecutionProgress')
router.register(r'flyway_schema_history',
                rombot_views.FlywaySchemaHistoryViewset,
                base_name='FlywaySchemaHistory')
router.register(r'patient_diseases', rombot_views.PatientDiseasesViewset,
                base_name='PatientDiseases')
router.register(r'treatment_programs', rombot_views.TreatmentProgramsViewset,
                base_name='TreatmentPrograms')
router.register(r'question_types',
                rombot_views.QuestionTypesViewset, base_name='QuestionTypes')
router.register(r'questions',
                rombot_views.QuestionsViewset, base_name='Questions')
router.register(r'proms',
                rombot_views.PromsViewset, base_name='Proms')
router.register(r'prom_questions',
                rombot_views.PromQuestionsViewset, base_name='PromQuestions')
router.register(r'prom_answers',
                rombot_views.PromAnswersViewset, base_name='PromAnswers')
'''
schema_view = get_swagger_view(title='Snippets API')

# --- URL PARTENS ---
urlpatterns = (
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('djoser.urls.base')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('djoser.social.urls')),
    url(r'^$', egpaf_views.index, name='index'),
    url(r'^swagger/', schema_view),
)
