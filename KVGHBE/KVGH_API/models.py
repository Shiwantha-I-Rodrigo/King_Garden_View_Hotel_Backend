from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
# to reset migrations delete db and migrations folder
# force makemigrations with manage.py makemigrations APPNAME


class Hotel(models.Model):
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    hotel_id = models.BigAutoField(primary_key=True)
    hotel_name = models.CharField(max_length=128, unique=True)
    hotel_address = models.CharField(max_length=256)
    hotel_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    hotel_email = models.EmailField()


class Room_Type(models.Model):
    type_id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=128)
    type_price = models.DecimalField(max_digits=8, decimal_places=2)
    type_single_beds = models.PositiveSmallIntegerField()
    type_double_beds = models.PositiveSmallIntegerField()
    type_twin_beds = models.PositiveSmallIntegerField()
    type_child_beds = models.PositiveSmallIntegerField()
    type_wifi = models.BooleanField(default=False)
    type_hotwater = models.BooleanField(default=False)
    type_max_guests = models.PositiveSmallIntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)


class Room(models.Model):
    room_id = models.BigAutoField(primary_key=True)
    room_number = models.CharField(max_length=8)
    room_status = models.BooleanField(default=False)
    room_type = models.ForeignKey(Room_Type, on_delete=models.PROTECT)
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)


class User(models.Model):
    GENDERS = [
        ("M","Male"),
        ("F","Female"),
    ]
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    user_name = models.CharField(max_length=128, primary_key=True)
    user_role = models.DecimalField(max_digits=3, decimal_places=0)
    user_pass = models.BinaryField()
    user_first_name = models.CharField(max_length=128)
    user_last_name = models.CharField(max_length=128)
    user_dob = models.DateField()
    user_gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    user_address = models.CharField(max_length=256)
    user_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    user_email = models.EmailField()
    user_discount = models.DecimalField(max_digits=3, decimal_places=1)


class Customer(models.Model):
    GENDERS = [
        ("M","Male"),
        ("F","Female"),
    ]
    phone_regex = RegexValidator(regex='^\+?1?\d{9,15}$', message="invalid phone number")
    customer_id = models.BigAutoField(primary_key=True)
    customer_first_name = models.CharField(max_length=128)
    customer_last_name = models.CharField(max_length=128)
    customer_dob = models.DateField()
    customer_gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    customer_address = models.CharField(max_length=256)
    customer_telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    customer_email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Reservation(models.Model):
    res_id = models.BigAutoField(primary_key=True)
    res_date = models.DateTimeField(auto_now_add=True)
    res_mod_date = models.DateTimeField(auto_now=True)
    res_check_in = models.DateTimeField()
    res_check_out = models.DateField()
    res_adults = models.DecimalField(max_digits=2, decimal_places=0)
    res_children = models.DecimalField(max_digits=2, decimal_places=0)
    res_special_req = models.CharField(max_length=512)
    res_discount = models.DecimalField(max_digits=3, decimal_places=1)
    res_price = models.DecimalField(max_digits=8, decimal_places=2)
    res_breakfast = models.BooleanField(default=False)
    res_lunch = models.BooleanField(default=False)
    res_dinner = models.BooleanField(default=False)
    res_paid = models.BooleanField(default=False)
    res_post_comments = models.CharField(max_length=512)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)


class Session(models.Model):
    session_id = models.BigAutoField(primary_key=True)
    session_key = models.BinaryField(max_length=2048)
    session_auth = models.DecimalField(max_digits=3, decimal_places=0)
    session_exp = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
