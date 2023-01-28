from django.contrib import admin
from django.urls import path
from .views import RequesOTP, VerifyOTP, GetUsers, AuthUserRegistrationView, AuthUserLoginView

urlpatterns = [
    path('verify-otp', VerifyOTP.as_view()),
    path('request-otp', RequesOTP.as_view()),
    # path('owner-registration', OwnerRegistration.as_view()),
    # path('contacts', Contacts.as_view()),
    path('users', GetUsers.as_view()),


    path(r'register', AuthUserRegistrationView.as_view()),
    path(r'login', AuthUserLoginView.as_view()),


    # url(r'^logout/', LogoutView.as_view()),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    # url(r'^admin/$', AuthAdminRegistrationView.as_view(), name='register_admin'),
    # url(r'^employee/$', AuthEmployeeRegistrationView.as_view(), name='register_employee'),
    # url(r'^manager/$', AuthManagerRegistrationView.as_view(), name='register_manager'),


]