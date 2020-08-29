from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    pass

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    time_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=240)
    ticket_author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="ticket_author", blank=True, null=True)
    INPROGRESS = "IP"
    TICKET_STATUS = [
        ('New', 'New'),
        (INPROGRESS, 'In Progress'),
        ('Done', 'Done'),
        ('Invalid', 'Invalid'),
    ]
    ticket_status = models.CharField(choices=TICKET_STATUS, max_length=7, default="New")
    user_assigned_to_ticket = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_assigned_to_ticket", blank=True, null=True)
    user_completed_ticket = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_completed_ticket", blank=True, null=True)

    def __str__(self):
        return self.title