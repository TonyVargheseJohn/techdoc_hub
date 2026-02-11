from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    employeid = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True)
    gender = models.CharField(max_length=50)
    photo = models.FileField(upload_to='UserPhoto/')
    password = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tbl_user'