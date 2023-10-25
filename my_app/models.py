from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
import uuid
from django.utils import timezone

# Create your models here.

STATUS_CHOICES = [('active', 'active'), ('disabled', 'disabled')]


# class UserManager(BaseUserManager):

#     def reg_user(self, username, email, password, first_name, last_name, **rest):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not username or email:
#             raise ValueError('User must have a username and an email')
#         if not first_name:
#             raise ValueError('User must have a first name')
#         user = self.model(username=username, first_name=first_name, last_name=last_name, email=self.normalize_email(
#             email), password=password, **rest)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=120, unique=True, db_index=True)
    phone = models.CharField(max_length=120, null=True, blank=True)
    stutus = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ImageField(upload_to="users/%y/%m/%d", blank=True)
    address = models.CharField(
        max_length=100, blank=True, verbose_name="Address"
    )
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    postal_code = models.CharField(
        max_length=10, blank=True, verbose_name="Postal Code"
    )
    state = models.CharField(max_length=100, blank=True, verbose_name="State")
    country = models.CharField(
        max_length=100, blank=True, verbose_name="Country")

    groups = models.ManyToManyField(
        "auth.Group", blank=True, related_name="my_app_user_groups")
    user_permissions = models.ManyToManyField(
        "auth.Permission", blank=True, related_name="my_app_user_permissions")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_login or ''}'s profile - {self.id}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None


class Book(models.Model):
    """table representation for the book"""
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount = models.DecimalField(decimal_places=2, max_digits=2, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveSmallIntegerField(default=0)  # max is 32767

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    @property
    def sale_price(self):
        return round(self.price * 0.8, 2)

    # @property
    # def discount(self):
    #     return round(float(self.price) * 0.2, 2)
# GO to admin.py to for registering models
