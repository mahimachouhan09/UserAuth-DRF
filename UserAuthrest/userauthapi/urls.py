from django.conf.urls import re_path, url
from django.urls import include, path
from rest_auth.views import PasswordResetConfirmView, PasswordResetView
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/auth', views.AuthViewSet, basename='auth')

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('profile-update/', views.ProfileViewSet.as_view()),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path(r'^password/reset/$', PasswordResetView.as_view(),
         name='rest_password_reset'),

    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(
    ), name='password_reset_confirm'),

]
