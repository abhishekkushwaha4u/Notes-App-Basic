from django.db import models

class CustomUser(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    note = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
