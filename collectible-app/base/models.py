import uuid
import os
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings


# Generates the file path for a new Collection image
def collection_image_file_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('uploads/collection/', filename)


class UserManager(BaseUserManager):
    # Creates and Saves a new User
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have a valid E-Mail address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    # Creates and saves a new Superuser
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


# Customizes account so it is based on E-mail and not username.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


# Creates a Tag to be used on a Collection
class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


# Creates an Item to be listed in a Collection
class Item(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# Creates a Collection that is composed of Items with Tags.
class Collection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    items_in_collection = models.IntegerField()
    floor_price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    items = models.ManyToManyField('Item')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=collection_image_file_path)

    def __str__(self):
        return self.title
