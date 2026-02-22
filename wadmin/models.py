from django.db import models

# Create your models here.

class MachineCategory(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_machine_category'



# class Machine(models.Model):
#     category = models.ForeignKey('MachineCategory', on_delete=models.CASCADE)
#     machine_name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.FileField(upload_to='MachineImage/', null=True, blank=True)

#     class Meta:
#         db_table = 'tbl_machine'


class Machine(models.Model):
    category = models.ForeignKey('MachineCategory', on_delete=models.CASCADE)
    machine_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='MachineImage/', null=True, blank=True)
    spare_manual = models.FileField(upload_to='MachineManuals/', null=True, blank=True)
    software_file = models.FileField(upload_to='MachineSoftware/', null=True, blank=True)

    class Meta:
        db_table = 'tbl_machine'


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_announcement'

