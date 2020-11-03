from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    username = models.CharField(verbose_name='Username',max_length=30 , unique = True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    phone = models.CharField(max_length=13,default="")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True) # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) # a superuser

    USER_TYPES = (
    ('restaurant','RESTAURANT'),
    ('customer','CUSTOMER'),
    )
    usertype = models.CharField(max_length = 15, choices = USER_TYPES,default = 'customer')
    fine = models.IntegerField(default=0)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # Email & Password are required by default.


    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.last_name

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Location(models.Model):
    location = models.CharField(max_length = 100)

    def __str__(self):
        return self.location

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length = 100)
    location = models.ForeignKey(Location,on_delete = models.CASCADE)
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    restaurant_id = models.CharField(max_length = 20, unique = True)
    description = models.CharField(max_length = 500)
    city = models.CharField(max_length = 50)
    ratingbystaff = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbyfood = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbylocation = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbyhygiene = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.username

class RestaurantTables(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    tablefor = models.PositiveIntegerField()
    nooftables = models.PositiveIntegerField()

    def __str__(self):
        return self.restaurant_id

class Reservation(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    datetime = models.DateTimeField()
    leavingtime = models.DateTimeField()
    tablesfor = models.CharField(max_length = 20)
    nooftables = models.CharField(max_length = 20)

    def __str__(self):
        return self.username

class Review(models.Model):
    review_id = models.CharField(max_length=20)
    restaurant_name = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    review_title = models.CharField(max_length = 50)
    review = models.CharField(max_length = 500)
    ratingbystaff = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbyfood = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbylocation = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    ratingbyhygiene = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.restaurant_id

class RestaurantPhotos(models.Model):
    restaurant_name = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    photos = models.ImageField(upload_to = 'img/')

    def __str__(self):
        return self.restaurant_name

class CustomerPhotos(models.Model):
    restaurant_name = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    photos = models.ImageField(upload_to = 'img/')

    def __str__(self):
        return self.restaurant_name
