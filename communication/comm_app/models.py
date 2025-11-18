from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)  # Обязательный email

    def __str__(self):
        return self.username


class Client(models.Model):
    tg_chat_id = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return str(self.tg_chat_id)


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("appointed", "Appointed"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets", null=True
    )
    chat = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="tickets")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.pk} ({self.status})"


class MessageOut(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_out"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket_id = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="messages_out", null=True
    )

    def __str__(self):
        return f"OUT {self.pk} from {self.user}"


class MessageIn(models.Model):
    chat_id = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="messages_in"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket_id = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, related_name="messages_in"
    )

    def __str__(self):
        return f"IN {self.pk} from chat {self.chat_id}"
