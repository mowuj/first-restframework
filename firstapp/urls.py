from django.urls import path
from .views import *

urlpatterns = [
    path('first/',firstAPI),
    path('registration/',registrationAPI),
    path('contact/', ContactAPIViewOne.as_view()),
    path('post/', PostCreateAPIView.as_view()),
    # path('post/<int:id>/', PostRetrieveAPIView.as_view()),
    path('post/<int:id>/', PostUpdateAPIView.as_view()),
    # path('postlist/', PostListAPIView.as_view()),
]