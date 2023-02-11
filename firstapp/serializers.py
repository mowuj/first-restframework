from django import forms
from .models import *
from rest_framework import serializers

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        # fields=['name','email','phone','subject','details']