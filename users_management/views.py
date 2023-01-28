import math
import uuid
from random import random

from django.contrib.auth import authenticate
from django.shortcuts import render
from urllib import request
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from stationery_management.models import Stationery
from .models import User
from .serializers import AuthAdminRegistrationSerializer, AuthUserRegistrationSerializer, AuthUserLoginSerializer, \
    UserSerializer, StationarySerializer


# Create your views here.

class OwnerRegistration(APIView):
    permission_classes = (AllowAny,)

    def __createOwner(self, data):
        self.code = generateOTP()
        try:
            user = User.objects.get(phone_number=str(data['phone_number']))
            user.set_password(self.code)
            user.save()
            self.owner = user
            return True
        except User.DoesNotExist:
            user_data = {
                'phone_number': data['phone_number'],
                'password': str(self.code),
                'role': 1
            }
            user_serializer = AuthUserRegistrationSerializer(data=user_data)
            if user_serializer.is_valid():
                self.owner = user_serializer.save()
                return True
            self.errors = user_serializer.errors
        return False

    def post(self, request):
        if self.__createOwner(request.data):
            print(self.owner)
            data = {
                "company_name": request.data['company'],
                "created_by": self.owner.id
            }
            if self.__createCompany(data):
                print("Code ", self.code)
                return Response({"status": True})

        return Response({"status": False, "details": self.errors})


class AuthAdminRegistrationView(APIView):
    serializer_class = AuthAdminRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        if 'role' not in data:
            return Response('bad request', status=403)

        if str(data['role']) == '1':
            serializer = AuthAdminRegistrationSerializer(data=data)

        elif str(data['role']) == '2':
            serializer = AuthUserRegistrationSerializer(data=data)

        valid = serializer.is_valid(raise_exception=True)

        if valid:
            try:
                serializer.save()
            except ValueError:
                return Response({
                    'success': False,
                    'statusCode': 401
                })
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random() * 10)]

    print("OTP", OTP)
    return OTP


class RequesOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if 'phone_number' in request.data:
            code = generateOTP()
            print(code)
            try:
                user = User.objects.get(phone_number=str(request.data['phone_number']))
                print('saving')
                user.set_password(code)
                user.save()
            except User.DoesNotExist:
                id_ = uuid.uuid4()
                user_data = {
                    'phone_number': request.data['phone_number'],
                    'email': f'${id_}_email@gmail.com',
                    'password': str(code),
                    'role': 2
                }
                print(user_data)
                user_serializer = AuthUserRegistrationSerializer(data=user_data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    print(user.phone_number)

                    return Response({"status": True})

                return Response({"status": False, "errors": user_serializer.errors})

        return Response({"status": False})


class VerifyOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        if "phone_number" in data and "code" in data:
            print(data)
            try:
                the_user = User.objects.get(phone_number=data['phone_number'])
                user = authenticate(email=the_user.email, password=data['code'])
                if user is not None:
                    token = Token.objects.get_or_create(user=user)
                    user_serializer = UserSerializer(instance=user, many=False)

                    response = {
                        'token': str(token[0]),
                        'user': user_serializer.data
                    }
                    return Response(response)

                return Response({"message": "Invalid OTP"}, status=401)
            except User.DoesNotExist:
                return Response("User not found", status=404)

        return Response({"message": "Bad Request"}, status=400)


class Contacts(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data['contacts']
        contacts = str(data).rstrip().replace('[', '').replace(',', '').replace(']', '').split()
        # print(request.data)
        found_contacts = []
        for contact in contacts:
            try:
                user = User.objects.get(phone_number=str(contact))
                print(contact)
                found_contacts.append(contact)
            except User.DoesNotExist:
                print('Not', contact)
                pass
        return Response(found_contacts)


class GetUsers(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def createStationary(data):
        serializer = StationarySerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            return {"status": True, "serializer": serializer}
        return {"status": False, "errors": serializer.errors}

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            save_stationary = self.createStationary(request.data)
            if save_stationary['status']:
                user_ = serializer.save()
                save_stationary['serializer'].save(created_by=user_)
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'User successfully registered!',
                    'user': serializer.data
                }

                return Response(response, status=status_code)
            return Response(save_stationary['errors'])


class AuthUserLoginView(APIView):
    serializer_class = AuthUserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print("Data", request.data)
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            stationary = {}
            try:
                _stationary = Stationery.objects.get(created_by=serializer.data['id'])
                stationary = StationarySerializer(instance=_stationary, many=False).data
            except Stationery.DoesNotExist:
                pass
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                "stationary": stationary,
                'user': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                    'id': serializer.data['id'],
                    'phone_number': serializer.data['phone_number']
                }
            }

            return Response(response, status=status_code)
