
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from firstapp.views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from .views import MyTokenObtainPairView
from rest_framework.authentication import TokenAuthentication
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeView),
    path('api/login-api/',obtain_auth_token),
    path('api/token/', MyTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/',include('rest_framework.urls')),
    path('api/firstapp/',include('firstapp.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
