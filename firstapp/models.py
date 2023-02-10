from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=125)
    subject=models.CharField(max_length=100)
    details=models.TextField()
    def __str(self):
        return self.name