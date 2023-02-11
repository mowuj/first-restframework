from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from rest_framework.views import APIView
def homeView(request):
    return render(request,'index.html')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated,])
def firstAPI(request):
    if request.method=="POST":
        name=request.data['name']
        age=request.data['age']
        print(name,age)
        return Response({"name":name,"age":age})
    context={
        'name':'Ahsan',
        'university':'Nation University'
    }
    return Response(context)

@api_view(['POST',])
def registrationAPI(request):
    if request.method=='POST':
        username=request.data['username']
        email=request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        

        if User.objects.filter(username=username).exists():
            return Response({"error":"An user with that username already exists!"})
        if password1 != password2:
            return Response({"error":"Password are not matched!"})

        user=User()
        user.username=username
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.is_active=True
        user.set_password(raw_password=password1)
        user.save()
        return Response({"Success":"User Successfully Registered ."})

# function based view 

@api_view(['POST',])
def contactPost(request):
    if request.method=="POST":
        data=request.data
        name = data['name']
        email=data['email']
        subject=data['subject']
        phone=data['phone']
        details=data['details']

        contact=Contact(name=name,email=email,subject=subject,phone=phone,details=details)
        contact.save()
        return Response({"Success":"Successfully Saved.."})
    
# Class based view 

from .serializers import ContactSerializer,ContactForm
class ContactAPIView(APIView):
    permission_classes=[AllowAny,]
    def post(self,request,format=None):
        # data=request.data    
            # simple data get 

        # name = data['name']
        # email=data['email']
        # subject=data['subject']
        # phone=data['phone']
        # details=data['details']

        # contact=Contact(name=name,email=email,subject=subject,phone=phone,details=details)
        # contact.save()

            # form get data 
        # from =ContactForm(request.POST)
        # if form.is_valid():
        #     form.save()

        # serializer get data 

        serializer=ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    def get(self,request,format=None):
        queryset=Contact.objects.all()
        serializer=ContactSerializer(queryset,many=True)
        return Response(serializer.data)