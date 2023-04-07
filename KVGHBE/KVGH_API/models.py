from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Hotel(models.Model):
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    hotel_id = models.BigAutoField(primary_key=True, unique=True)
    hotel_name = models.CharField(max_length=128, unique=True)
    hotel_address = models.CharField(max_length=256)
    hotel_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    hotel_email = models.EmailField()


class Room_Type(models.Model):
    type_id = models.BigAutoField(primary_key=True, unique=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    type_name = models.CharField(max_length=128)
    type_price = models.DecimalField(max_digits=8, decimal_places=2)
    type_single_beds = models.PositiveSmallIntegerField(max_length=2)
    type_double_beds = models.PositiveSmallIntegerField(max_length=2)
    type_twin_beds = models.PositiveSmallIntegerField(max_length=2)
    type_child_beds = models.PositiveSmallIntegerField(max_length=2)
    type_wifi = models.BooleanField(default=False)
    type_hotwater = models.BooleanField(default=False)
    type_max_guests = models.PositiveSmallIntegerField(max_length=2)


class Room(models.Model):
    room_id = models.BigAutoField(primary_key=True, unique=True)
    type_id = models.ForeignKey(Room_Type, on_delete=models.PROTECT)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    room_number = models.CharField(max_length=8)
    room_status = models.BooleanField(default=False)


class User_Role(models.Model):
    role_id = models.BigAutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=128)
    role_validator = models.CharField(max_length=256)


class User(models.Model):
    GENDERS = [
        ("M","Male"),
        ("F","Female"),
    ]
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    user_id = models.BigAutoField(primary_key=True, unique=True)
    role_id = models.ForeignKey(User_Role, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=128, unique=True)
    user_pass = models.CharField(max_length=256)
    user_first_name = models.CharField(max_length=128)
    user_last_name = models.CharField(max_length=128)
    user_dob = models.DateField()
    user_gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    user_address = models.CharField(max_length=256)
    user_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    user_email = models.EmailField()
    user_discount = models.DecimalField(max_digits=2, decimal_places=2)


class Customer(models.Model):
    GENDERS = [
        ("M","Male"),
        ("F","Female"),
    ]
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    customer_id = models.BigAutoField(primary_key=True, unique=True)
    customer_first_name = models.CharField(max_length=128)
    customer_last_name = models.CharField(max_length=128)
    customer_dob = models.DateField()
    customer_gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    customer_address = models.CharField(max_length=256)
    customer_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    customer_email = models.EmailField()


class Reservation(models.Model):
    res_id = models.BigAutoField(primary_key=True, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    room_id = models.ForeignKey(Room, on_delete=models.PROTECT)
    res_date = models.DateTimeField(auto_now_add=True)
    res_mod_date = models.DateTimeField(auto_now=True)
    res_check_in = models.DateTimeField()
    res_check_out = models.DateField()
    res_adults = models.DecimalField(max_digits=2, decimal_places=0)
    res_children = models.DecimalField(max_digits=2, decimal_places=0)
    res_special_req = models.CharField(max_length=512)
    res_discount = models.DecimalField(max_digits=2, decimal_places=2)
    res_price = models.DecimalField(max_digits=8, decimal_places=2)
    res_breakfast = models.BooleanField(default=False)
    res_lunch = models.BooleanField(default=False)
    res_dinner = models.BooleanField(default=False)
    res_paid = models.BooleanField(default=False)
    res_post_comments = models.CharField(max_length=512)