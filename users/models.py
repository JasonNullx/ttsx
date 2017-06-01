from django.db import models

# Create your models here.


class Users(models.Model):
    uname = models.CharField(max_length=30, null=False)
    upass = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    recipient = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.uname

