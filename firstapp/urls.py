from django.urls import path
from .views import *

urlpatterns = [
    path('first/',firstAPI),
    path('registration/',registrationAPI),
    path('contact/', ContactAPIViewOne.as_view()),
]