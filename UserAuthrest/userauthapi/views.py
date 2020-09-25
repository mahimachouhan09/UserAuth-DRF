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

from django.contrib.auth import get_user_model, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Profile
from .serializers import ProfileSerializer
from .utils import create_user_account, get_and_authenticate_user

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.EmptySerializer
    queryset = User.objects.all()
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
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
        import pdb
        pdb.set_trace()
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class ProfileViewSet(generics.UpdateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    # import pdb;pdb.set_trace()
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # lookup_field = 'username'

    def partial_update(self, request, pk=None):
        serializer = ProfileSerializer(
            request.user, data=request.data, partial=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    # # @login_required
    # def get_object(self):
    #     queryset = Profile.objects.filter(user=self.request.user.id)
    #     # obj = queryset[0]
    #     return queryset

    # def put(self, request, pk, format=None):
    #     queryset = self.get_object(pk)
    #     serializer = ProfileSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
