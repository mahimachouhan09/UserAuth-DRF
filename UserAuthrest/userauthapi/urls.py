from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/auth', views.AuthViewSet, basename='auth')
# router.register('profile-update/', views.ProfileViewSet.as_view(), basename='update')

# urlpatterns = router.urls
urlpatterns = [         
  path('api-auth/', include(router.urls)),
  path('profile-update/', views.ProfileViewSet.as_view()),
  url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]

# urlpatterns = [
#   # url(r'api/users^$', views.AuthViewSet),
#   path('api-auth/', include(router.urls)),
#   # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

# from .views import AuthViewSet
# router.register('api/auth', AuthViewSet, basename='auth')

# urlpatterns = [
#   # path('admin/', admin.site.urls),
#   path('api/auth', include(router.urls))  
# ]

