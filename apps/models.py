from django.db import models

class Driver(models.Model):
    app_user_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    app_user_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class KakaoUser(models.Model):
    app_user_id = models.PositiveIntegerField(unique=True)
    nickname = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname
