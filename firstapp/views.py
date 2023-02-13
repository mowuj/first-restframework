from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveAPIView,UpdateAPIView,RetrieveUpdateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView

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

# Model Serializer 
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
    
# Serializer 
class ContactAPIViewOne(APIView):
    permission_classes=[AllowAny,]
    def post(self,request,format=None):
        serializer = ContactSerializerOne(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    def put(self,request,format=None):
        contact=Contact.objects.get(id=1)
        serializer = ContactSerializerOne(data=request.data,instance=contact)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    def get(self, request, format=None):
        queryset = Contact.objects.all()
        serializer = ContactSerializerOne(queryset, many=True)
        return Response(serializer.data)

from rest_framework import status
# List create view 
class PostCreateAPIView(ListCreateAPIView):
    permission_classes=[IsAuthenticated,]
    queryset=BlogPost.objects.all()
    serializer_class=PostSerializer
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance=self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer=PostDetailSerializer(instance=instance,many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # List cerate api 
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)
    # Query Set customize
    def get_queryset(self):
        queryset=BlogPost.objects.filter()
        return queryset
    # List API VIEW 
# class PostListAPIView(ListAPIView):
#     permission_classes=[IsAuthenticated]
#     queryset=BlogPost.objects.all()
#     serializer_class = PostDetailSerializer

class PostRetrieveAPIView(RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    lookup_field='id'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)


class PostUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.filter(is_active=True)
    serializer_class = PostSerializer
    lookup_field='id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance= self.perform_update(serializer)
        serializer = PostDetailSerializer(instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active=False
        instance.save()

# Delete API 
# class PostDeleteAPIView(DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = BlogPost.objects.filter(is_active=True)
#     serializer_class = PostSerializer
#     lookup_field = 'id'
