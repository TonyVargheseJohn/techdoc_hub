from django.db import models
from guest.models import User
from wadmin.models import Machine


class UserMachineFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    file = models.FileField(upload_to='UserMachineFiles/')
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_machine_file"

    def __str__(self):
        return f"{self.user.name} - {self.machine.machine_name}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.user.name}"
    




class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_msgs")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_msgs")
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="sent")  # sent / seen

    class Meta:
        db_table = 'tbl_chat'