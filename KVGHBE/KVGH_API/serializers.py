from rest_framework import serializers
from .models import Hotel, Room_Type, Room, User, Customer, Reservation, Session


class Hotel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('hotel_id', 
                  'hotel_name', 
                  'hotel_address', 
                  'hotel_telephone', 
                  'hotel_email')


class Room_Type_Serializer(serializers.ModelSerializer):
    #hotel = Hotel_Serializer()
    class Meta:
        model = Room_Type
        fields = ('type_id', 
                  'type_name', 
                  'type_price', 
                  'type_single_beds', 
                  'type_double_beds', 
                  'type_twin_beds', 
                  'type_child_beds', 
                  'type_wifi', 
                  'type_hotwater', 
                  'type_max_guests'
                  'hotel')


class Room_Serializer(serializers.ModelSerializer):
    #hotel = Hotel_Serializer()
    #room_type = Room_Type_Serializer()
    class Meta:
        model = Room
        fields = ('room_id',
                  'room_number', 
                  'room_status',
                  'room_type' 
                  'hotel', )


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 
                  'user_role', 
                  'user_pass', 
                  'user_first_name', 
                  'user_last_name', 
                  'user_dob', 
                  'user_gender', 
                  'user_address', 
                  'user_telephone', 
                  'user_email', 
                  'user_discount',)


class Customer_Serializer(serializers.ModelSerializer):
    #user = User_Serializer()
    class Meta:
        model = Customer
        fields = ('customer_id',
                  'customer_first_name'
                  'customer_last_name', 
                  'customer_dob', 
                  'customer_gender', 
                  'customer_address', 
                  'customer_telephone', 
                  'customer_email',
                  'user',)


class Reservation_Serializer(serializers.ModelSerializer):
    #user = User_Serializer()
    #room = Room_Serializer()
    #customer = Customer_Serializer()
    class Meta:
        model = Reservation
        fields = ('res_id', 
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
                  'res_paid',
                  'res_post_comments',
                  'customer'
                  'user', 
                  'room', )


class Session_Serializer(serializers.ModelSerializer):
    #user = User_Serializer()
    class Meta:
        model = Session
        fields = ('session_id', 
                  'session_key', 
                  'session_auth',
                  'session_exp',
                  'user',) 