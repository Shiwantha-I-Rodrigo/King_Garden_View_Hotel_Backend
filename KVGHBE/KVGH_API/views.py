import sys, json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from datetime import date, timedelta
from .models import Hotel, Room_Type, Room, User, Customer, Reservation, Session
from .crypt import get_initials, generate_bytes, generate_str, any_to_byte, byte_to_hash,\
        encrypt, decrypt, authenticate, auth_calculate, byte_to_any, convert_string_to_aes_key,\
        auth_levels


@api_view(['GET'])
def crypto_prime(request):
    try:
        initials = get_initials()
        res = {"prime":initials[0],
               "base":initials[1]}
        return Response(res,status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)


@api_view(['POST'])
def crypto_link(request):
    try:
        prime = int(request.data['req']['crypto']['prime'])
        base = int(request.data['req']['crypto']['base'])
        client_crypto_mix = int(request.data['req']['crypto']['client_crypto_mix'])
        server_private_key = int(generate_str(600))
        server_crypto_mix = pow(base,server_private_key,prime)
        mutual_private_key = pow(client_crypto_mix,server_private_key,prime)
        key_bytes = any_to_byte(mutual_private_key,"str")
        salt_bytes = key_bytes[:16]
        aes_key_bytes = convert_string_to_aes_key(key_bytes, salt_bytes)
        aes_key_bytes_b64 = any_to_byte(aes_key_bytes,'b64e')
        user = User.objects.get(user_name='_')
        data = {"session_key":aes_key_bytes_b64,
                "session_auth":0,
                "user":user,
                "session_exp":date.today() + timedelta(days=1)}
        session = Session(**data)
        session.save()
        res = {"server_crypto_mix":server_crypto_mix,
               "session_id":session.session_id}
        return Response(res,status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)


@api_view(['POST'])
def authorize(request):
    try:
        plain_text, auth_level, user_name = decrypt(request)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic['auth']
        is_authenticated, session_id, session_key = authenticate(ele_data)
        if is_authenticated:
            ele_str = json.dumps({"session_id":session_id,"session_key":session_key})
            cypher_text = encrypt(request,ele_str)
            return Response({"res":cypher_text},status=200)
        else:
            return Response({},status=401)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)


@api_view(['POST'])
def create(request, element):
    try:
        plain_text, auth_level, user_name = decrypt(request)
        ro,co,uo,ra,ca,ua,da = auth_levels(auth_level)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]

        if element=='hotel' and ca:
            item = Hotel(**ele_data)
        elif element == 'room_type' and ca:
            hotel = Hotel.objects.get(hotel_id=ele_data['hotel_id'])
            ele_data.pop('hotel_id')
            ele_data['hotel'] = hotel
            item = Room_Type(**ele_data)
        elif element == 'room' and ca:
            hotel = Hotel.objects.get(hotel_id=ele_data['hotel_id'])
            ele_data.pop('hotel_id')
            ele_data['hotel'] = hotel
            room_type = Room_Type.objects.get(type_id=ele_data['type_id'])
            ele_data.pop('type_id')
            ele_data['room_type'] = room_type
            item = Room(**ele_data)
        elif element == 'user':
            ele_data['user_role'] = auth_calculate(ro,co,uo,ra,ca,ua,da,int(ele_data['user_role']))
            client_pass_hash_b64 = any_to_byte(ele_data['user_pass'],'str')
            client_pass_hash = any_to_byte(client_pass_hash_b64,'b64d')
            salt_bytes = generate_bytes(16)
            client_pass_hash_hash = byte_to_hash(salt_bytes+client_pass_hash)
            client_pass_hash_hash_b64 = any_to_byte(client_pass_hash_hash,'b64e')
            salt_b64 = any_to_byte(salt_bytes,'b64e')
            ele_data['user_pass'] = salt_b64 + client_pass_hash_hash_b64
            item = User(**ele_data)
        elif element == 'customer' and ( co or ca ):
            user_name_x = ele_data['user_name'] if ca else user_name
            user = User.objects.get(user_name=user_name_x)
            ele_data.pop('user_name')
            ele_data['user'] = user
            item = Customer(**ele_data)
        elif element == 'reservation' and ( co or ca ):
            user_name_x = ele_data['user_name'] if ca else user_name
            user = User.objects.get(user_name=user_name_x)
            ele_data.pop('user_name')
            ele_data['user'] = user
            customer = Customer.objects.get(customer_id=ele_data['customer_id'])
            ele_data.pop('customer_id')
            ele_data['customer'] = customer
            room = Room.objects.get(room_id=ele_data['room_id'])
            ele_data.pop('room_id')
            ele_data['room'] = room
            item = Reservation(**ele_data)

        item.save()
        ele_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cypher_text = encrypt(request,ele_str)
        return Response({"res":cypher_text},status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({"res":""},status=500)


@api_view(['GET'])
def read(request, element, req_id):
    try:
        # req_id hotel/read/123 # id = request.GET['id'] > hotel/read?id=123
        plain_text, auth_level, user_name = decrypt(request)
        ro,co,uo,ra,ca,ua,da = auth_levels(auth_level)

        if element=='hotel' and ( ro or ra ):
            item = Hotel.objects.get(hotel_id=req_id)
        elif element == 'room_type' and ( ro or ra ):
            item = Room_Type.objects.get(type_id=req_id)
        elif element == 'room' and ( ro or ra ):
            item = Room.objects.get(room_id=req_id)
        elif element == 'user' and user_name == req_id:
            item = User.objects.get(user_name=req_id)
        elif element == 'customer':
            item = Customer.objects.get(customer_id=req_id)
            if item['user_name'] != user_name and not ra:
                return Response({},status=401)
        elif element == 'reservation':
            item = Reservation.objects.get(res_id=req_id)
            if item['user_name'] != user_name and not ra:
                return Response({},status=401)
        
        ele_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cypher_text = encrypt(request,ele_str)
        return Response({"res":cypher_text},status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)


@api_view(['POST'])
def delete(request, element):
    try:
        plain_text, auth_level, user_name = decrypt(request)
        ro,co,uo,ra,ca,ua,da = auth_levels(auth_level)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]

        if element=='hotel' and da:
            item = Hotel.objects.get(hotel_id=ele_data['hotel_id'])
        elif element == 'room_type' and da:
            item = Room_Type.objects.get(type_id=ele_data['type_id'])
        elif element == 'room' and da:
            item = Room.objects.get(room_id=ele_data['room_id'])
        elif element == 'user' and da:
            item = User.objects.get(user_name=ele_data['user_name'])
        elif element == 'customer' and da:
            item = Customer.objects.get(customer_id=ele_data['customer_id'])
        elif element == 'reservation' and da:
            item = Reservation.objects.get(res_id=ele_data['res_id'])
        
        item.delete()
        ele_str = f"{ele_data['id']} deleted"
        cypher_text = encrypt(request,ele_str)
        return Response({"res":cypher_text},status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)


@api_view(['POST'])
def update(request, element):
    try:
        plain_text, auth_level, user_name = decrypt(request)
        ro,co,uo,ra,ca,ua,da = auth_levels(auth_level)
        ele_dic = json.loads(plain_text)
        ele_data = ele_dic[str(element)]

        if element=='hotel' and ua:
            item = Hotel(**ele_data)
        elif element == 'room_type' and ua:
            hotel = Hotel.objects.get(hotel_id=ele_data['hotel_id'])
            ele_data.pop('hotel_id')
            ele_data['hotel'] = hotel
            item = Room_Type(**ele_data)
        elif element == 'room' and ua:
            hotel = Hotel.objects.get(hotel_id=ele_data['hotel_id'])
            ele_data.pop('hotel_id')
            ele_data['hotel'] = hotel
            room_type = Room_Type.objects.get(type_id=ele_data['type_id'])
            ele_data.pop('type_id')
            ele_data['room_type'] = room_type
            item = Room(**ele_data)
        elif element == 'user' and ( uo and user_name == ele_data['user_name']) or ua:
            item = User(**ele_data)
        elif element == 'customer': 
            user_name_x = ele_data['user_name'] if ua else user_name
            user = User.objects.get(user_name=user_name_x)
            ele_data.pop('user_name')
            ele_data['user'] = user
            item = Customer(**ele_data)
            if item['user_name'] != user_name and not ua:
                return Response({"res":""},status=401)
        elif element == 'reservation':
            user_name_x = ele_data['user_name'] if ua else user_name
            user = User.objects.get(user_name=user_name_x)
            ele_data.pop('user_name')
            ele_data['user'] = user
            customer = Customer.objects.get(customer_id=ele_data['customer_id'])
            ele_data.pop('customer_id')
            ele_data['customer'] = customer
            room = Room.objects.get(room_id=ele_data['room_id'])
            ele_data.pop('room_id')
            ele_data['room'] = room
            item = Reservation(**ele_data)
            if item['user_name'] != user_name and not ua:
                return Response({"res":""},status=401)

        if 'res_id' in ele_data:
            ele_data.pop('res_id',None)
        elif 'hotel_id' in ele_data:
            ele_data.pop('hotel_id',None)
        elif 'type_id' in ele_data:
            ele_data.pop('type_id',None)
        elif 'room_id' in ele_data:
            ele_data.pop('room_id',None)
        elif 'user_name' in ele_data:
            ele_data.pop('user_name',None)
        elif 'customer_id' in ele_data:
            ele_data.pop('customer_id',None)

        item.__dict__.update(ele_data)
        item.save()
        hotel_str = json.dumps(model_to_dict(item), ensure_ascii=False)
        cipher_text = encrypt(request,hotel_str)
        return Response({"res":cipher_text},status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        print(f"error > {ex_type} > {ex_value} > {ex_traceback}")
        return Response({},status=500)
