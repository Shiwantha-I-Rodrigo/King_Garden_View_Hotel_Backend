from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from datetime import date, timedelta
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation, Session
from .serializers import Hotel_Serializer, Room_Type_Serializer, Room_Serializer, User_Role_Serializer, User_Serializer, Customer_Serializer, Reservation_Serializer, Session_Serializer
from .crypt import get_initials, generate_bits, generate_str, any_to_byte, byte_to_hash, encrypt, decrypt, authenticate, authorize
import sys, json


@api_view(['GET'])
def crypto_prime(request):
    try:
        # session = Session.objects.get(session_id = request.data['session_id'])
        # key_text = byte_to_any(session.session_key,'str')
        # nonce_text = byte_to_any(session.session_nonce,'str')
        initials = get_initials()
        res = {"prime":initials[0], "base":initials[1]}
        return Response(res, status=200)
    except:
        return Response("",status=500)


@api_view(['POST'])
def crypto_link(request):
    try:
        prime = int(request.data['crypto']['prime'])
        base = int(request.data['crypto']['base'])
        client_crypto_mix = int(request.data['crypto']['client_crypto_mix'])
        server_private_key = int(generate_str(600))
        server_crypto_mix = pow(base,server_private_key,prime)
        mutual_private_key = pow(client_crypto_mix,server_private_key,prime)
        key_bytes = any_to_byte(mutual_private_key,"str")
        key_sha256 = byte_to_hash(key_bytes)
        nonce_bytes = generate_bits(16)
        key_b64 = any_to_byte(key_sha256,'b64e')
        nonce_b64 = any_to_byte(nonce_bytes,'b64e')
        data = {"session_key":key_b64,
                "session_nonce":nonce_b64,
                "session_auth":9,
                "session_exp":date.today + timedelta(days=1)}
        session = Session(**data)
        session.save()
        return Response({"server_crypto_mix":server_crypto_mix, "session_id":session.session_id, "nonce":nonce_b64}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def authorize(request):
    try:
        plain_text = decrypt(request)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic['auth']
        user = authenticate(ele_data)
        user_level = authorize(user)
        if user_level < 1:
            key = generate_str(600)
        return Response(user, status=200)
    except:
        return Response("",status=500)


@api_view(['POST'])
def create(request, element):
    try:
        plain_text = decrypt(request)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]
        if element=='hotel':
            item = Hotel(**ele_data)
        elif element == 'room_type':
            item = Room_Type(**ele_data)
        elif element == 'room':
            item = Room(**ele_data)
        elif element == 'user_role':
            item = User_Role(**ele_data)
        elif element == 'user':
            password = ele_data['password']
            salt = generate_bits(16)
            iterations = 10000
            password_sha256 = any_to_byte(password,'str')
            for _ in range(iterations):
                password_sha256 = byte_to_hash(salt+password_sha256)
            ele_data['password'] = password_sha256
            item = User(**ele_data)
        elif element == 'customer':
            item = Customer(**ele_data)
        elif element == 'reservation':
            item = Reservation(**ele_data)
        item.save()
        ele_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cypher_text = encrypt(request,ele_str)
        return Response({"res" : cypher_text}, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['GET'])
def read(request, element, req_id):
    try:
        # req_id hotel/read/123 # id = request.GET['id'] > hotel/read?id=123
        if element=='hotel':
            item = Hotel.objects.get(hotel_id=req_id)
        elif element == 'room_type':
            item = Room_Type.objects.get(type_id=req_id)
        elif element == 'room':
            item = Room.objects.get(room_id=req_id)
        elif element == 'user_role':
            item = User_Role.objects.get(role_id=req_id)
        elif element == 'user':
            item = User.objects.get(user_name=req_id)
        elif element == 'customer':
            item = Customer.objects.get(customer_id=req_id)
        elif element == 'reservation':
            item = Reservation.objects.get(res_id=req_id)
        ele_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cypher_text = encrypt(request,ele_str)
        return Response({"res" : cypher_text}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def delete(request, element):
    try:
        plain_text = decrypt(request)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]
        item = Hotel.objects.get(hotel_id=ele_data['id'])
        if element=='hotel':
            item = Hotel.objects.get(hotel_id=id)
        elif element == 'room_type':
            item = Room_Type.objects.get(type_id=id)
        elif element == 'room':
            item = Room.objects.get(room_id=id)
        elif element == 'user_role':
            item = User_Role.objects.get(role_id=id)
        elif element == 'user':
            item = User.objects.get(user_name=id)
        elif element == 'customer':
            item = Customer.objects.get(customer_id=id)
        elif element == 'reservation':
            item = Reservation.objects.get(res_id=id)
        item.delete()
        ele_str = f"{ele_data['id']} deleted"
        cypher_text = encrypt(request,ele_str)
        return Response({"res" : cypher_text}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def update(request, element):
    try:
        plain_text = decrypt(request)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]
        if element=='hotel':
            item = Hotel(**ele_data)
        elif element == 'room_type':
            item = Room_Type(**ele_data)
        elif element == 'room':
            item = Room(**ele_data)
        elif element == 'user_role':
            item = User_Role(**ele_data)
        elif element == 'user':
            item = User(**ele_data)
        elif element == 'customer':
            item = Customer(**ele_data)
        elif element == 'reservation':
            item = Reservation(**ele_data)

        if 'res_id' in ele_data:
            ele_data.pop('res_id',None)
        elif 'hotel_id' in ele_data:
            ele_data.pop('hotel_id',None)
        elif 'type_id' in ele_data:
            ele_data.pop('type_id',None)
        elif 'room_id' in ele_data:
            ele_data.pop('room_id',None)
        elif 'role_id' in ele_data:
            ele_data.pop('role_id',None)
        elif 'user_name' in ele_data:
            ele_data.pop('user_name',None)
        elif 'customer_id' in ele_data:
            ele_data.pop('customer_id',None)

        item.__dict__.update(ele_data)
        item.save()
        hotel_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cipher_text = encrypt(request,hotel_str)
        return Response({"res":cipher_text}, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)
