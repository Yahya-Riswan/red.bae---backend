from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    img = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    role = models.CharField(max_length=50,default="user")
    status = models.CharField(max_length=50,default="active")
    
    joined_date = models.CharField(max_length=20)
    last_logined = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "id"]

    objects = UserManager()

    def __str__(self):
        return self.username
