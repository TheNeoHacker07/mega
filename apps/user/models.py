from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_active", True)
        extra.setdefault("is_superuser", True)

        user = self.create_user(email, password, **extra)
        return user
    

class User(AbstractUser):
    STATUS_CHOICES = [
        ("manager", "Manager"),
        ("customer", "Customer"),
    ]

    username = None
    email = models.EmailField(unique=True)
    # role = models.CharField(choices=STATUS_CHOICES, max_length=20)
    # vip = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email