from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    employeid = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True)
    gender = models.CharField(max_length=50)
    photo = models.FileField(upload_to='UserPhoto/')
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'tbl_user'



class Admin(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    employeid = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True)
    gender = models.CharField(max_length=50)
    photo = models.FileField(upload_to='AdminPhoto/', null=True, blank=True)
    password = models.CharField(max_length=50)
    

    class Meta:
        db_table = 'tbl_admin'




# ADD AT THE BOTTOM of guest/models.py
class Message(models.Model):
    sender_type = models.CharField(max_length=10)  # 'admin' or 'user'
    sender_id = models.IntegerField()
    receiver_type = models.CharField(max_length=10)
    receiver_id = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_messages'
        ordering = ['timestamp']