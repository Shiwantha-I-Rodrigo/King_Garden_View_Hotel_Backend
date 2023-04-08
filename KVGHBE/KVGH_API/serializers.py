from rest_framework import serializers
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation


class Hotel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('hotel_id', 
                  'hotel_name', 
                  'hotel_address', 
                  'hotel_telephone', 
                  'hotel_email')


class Room_Type_Serializer(serializers.ModelSerializer):
    hotel_id = Hotel_Serializer()
    class Meta:
        model = Room_Type
        fields = ('type_id', 
                  'hotel_id'
                  'type_name', 
                  'type_price', 
                  'type_single_beds', 
                  'type_double_beds', 
                  'type_twin_beds', 
                  'type_child_beds', 
                  'type_wifi', 
                  'type_hotwater', 
                  'type_max_guests')


class Room_Serializer(serializers.ModelSerializer):
    hotel_id = Hotel_Serializer()
    type_id = Room_Type_Serializer()
    class Meta:
        model = Room
        fields = ('room_id', 
                  'type_id' 
                  'hotel_id', 
                  'room_number', 
                  'room_status',)


class User_Role_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Role
        fields = ('role_id', 
                  'role_name' 
                  'role_validator',) 


class User_Serializer(serializers.ModelSerializer):
    role_id = User_Role_Serializer()
    class Meta:
        model = User
        fields = ('user_id', 
                  'role_id'
                  'user_name', 
                  'user_pass', 
                  'user_first_name', 
                  'user_last_name', 
                  'user_dob', 
                  'user_gender', 
                  'user_address', 
                  'user_telephone', 
                  'user_email', 
                  'user_discount')


class Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 
                  'customer_first_name'
                  'customer_last_name', 
                  'customer_dob', 
                  'customer_gender', 
                  'customer_address', 
                  'customer_telephone', 
                  'customer_email',)


class Reservation_Serializer(serializers.ModelSerializer):
    user_id = User_Serializer()
    room_id = Room_Serializer()
    customer_id = Customer_Serializer()
    class Meta:
        model = Reservation
        fields = ('res_id', 
                  'customer_id'
                  'user_id', 
                  'room_id', 
                  'res_date', 
                  'res_mod_date', 
                  'res_check_in', 
                  'res_check_out', 
                  'res_adults', 
                  'res_children', 
                  'res_special_req', 
                  'res_discount', 
                  'res_price', 
                  'res_breakfast', 
                  'res_lunch', 
                  'res_dinner', 
                  'res_paid',)
