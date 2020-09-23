# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserSerializer
# from django.contrib.auth.models import User

# class UserCreate(APIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer 

#   def post(self, request, format='json'):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#       user = serializer.save()
#       if user:
#         token = Token.objects.create(user=user)
#         json = serializer.data
#         json['token'] = token.key
#       return Response(json, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework import generics
from .models import Profile
# from .serializers import UserLoginSerializer,AuthUserSerializer,PasswordChangeSerializer
# class AuthViewSet(viewsets.ModelViewSet):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

from django.contrib.auth import get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from . import serializers
from .utils import get_and_authenticate_user, create_user_account
from .serializers import ProfileSerializer

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
  permission_classes = [AllowAny]
  serializer_class = serializers.EmptySerializer
  serializer_classes = {'login': serializers.UserLoginSerializer,
                        'register': serializers.UserRegisterSerializer,
                        'password_change': serializers.PasswordChangeSerializer,
                        }

  @action(methods=['POST', ], detail=False)
  def login(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_and_authenticate_user(**serializer.validated_data)
    data = serializers.AuthUserSerializer(user).data
    return Response(data=data, status=status.HTTP_200_OK)

  @action(methods=['POST', ], detail=False)
  def register(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = create_user_account(**serializer.validated_data)
    data = serializers.AuthUserSerializer(user).data
    return Response(data=data, status=status.HTTP_201_CREATED)

  @action(methods=['POST', ], detail=False)
  def logout(self, request):
    logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

  @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
  def password_change(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def get_serializer_class(self):
    if not isinstance(self.serializer_classes, dict):
      raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

    if self.action in self.serializer_classes.keys():
      return self.serializer_classes[self.action]
    return super().get_serializer_class()

# class ProfileViewSet(viewsets.ModelViewSet):
#   queryset = User.objects.all()
#   serializer_class = ProfileSerializer

class ProfileViewSet(generics.UpdateAPIView):
  queryset = Profile.objects.all()
  serializer_class = serializers.ProfileSerializer
  # import pdb;pdb.set_trace()
  # @login_required
  def get_object(self):
    queryset = Profile.objects.filter(user=self.request.user)
    # obj = queryset[0]
    return queryset