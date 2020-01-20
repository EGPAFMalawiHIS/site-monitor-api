

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
