from django import forms
from .models import *
from rest_framework import serializers

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

# Model Serializer 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        # fields=['name','email','phone','subject','details']

# serializers 
class ContactSerializerOne(serializers.Serializer):
    name=serializers.CharField(max_length=150)
    email=serializers.EmailField()
    phone=serializers.CharField(max_length=100)
    subject=serializers.CharField(max_length=100)
    details=serializers.CharField(max_length=100)

    def create(self,validated_data):
        return Contact(**validated_data)

    def update(self,instance,validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.email=validated_data.get('email',instance.email)
        instance.phone=validated_data.get('phone',instance.phone)
        instance.subject=validated_data.get('subject',instance.subject)
        instance.details=validated_data.get('details',instance.details)
        instance.save()
        return instance
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogPost
        # fields="__all__"
        exclude=['user','is_active']

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields="__all__"
        # exclude = ['user', 'is_active']
