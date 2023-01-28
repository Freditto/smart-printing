from django.contrib import admin
from django.urls import path
from .views import stationery_list, create_doc, CostView, document_list

urlpatterns = [
    path('stationerylist', stationery_list),
    path('upload_document', create_doc),
    path('document_list', document_list, name='document_list'),
    path('cost', CostView.as_view()),
    # path('owner-registration', OwnerRegistration.as_view()),
    # path('contacts', Contacts.as_view()),
    # path('users', GetUsers.as_view()),


    # path(r'register', AuthUserRegistrationView.as_view()),
    # path(r'login', AuthUserLoginView.as_view()),


]