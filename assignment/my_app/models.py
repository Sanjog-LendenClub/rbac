from django.db import models

# Create your models here.
# class Registration(models.Model):
#     name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     # confirm_password = models.CharField(max_length=100)
#     class Meta:
#         db_table = "user_database"

# class Role(models.Model):
#     name = models.CharField(max_length=50, unique=True)

# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=100)
#     role = models.ForeignKey(Role, on_delete=models.PROTECT)

# class API(models.Model):
#     name = models.CharField(max_length=100)

class API(models.Model):
    api_name = models.CharField(max_length=100)

class CustomUser(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Viewer', 'Viewer'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES)
    apis = models.ManyToManyField(API)

class profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(choices=[('Admin', 'Admin'),('User', 'User'),('Viewer', 'Viewer')], max_length=10)
    token = models.CharField(max_length=750, blank=True, null=True)