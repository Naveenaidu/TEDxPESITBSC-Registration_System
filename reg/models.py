from django.db import models

class Participant(models.Model):
    participant_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    reg_type = models.CharField(max_length=15, default="Student")
    barcode = models.CharField(max_length=50, blank=True)
    registered = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    had_lunch = models.BooleanField(default=False)
    had_dinner = models.BooleanField(default=False)
    had_breakfast = models.BooleanField(default=False)

    def __str__(self):
        return self.name
