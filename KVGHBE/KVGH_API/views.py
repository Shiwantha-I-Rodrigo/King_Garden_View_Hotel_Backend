from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation, Session
from .serializers import Hotel_Serializer, Room_Type_Serializer, Room_Serializer, User_Role_Serializer, User_Serializer, Customer_Serializer, Reservation_Serializer, Session_Serializer
from .crypt import get_initials, get_private_key,generate_nonce, any_to_byte, byte_to_hash, encrypt, decrypt
import sys, json


@api_view(['GET'])
def crypto_in(request):
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
def crypto_out(request):
    try:
        prime = int(request.data['crypto']['prime'])
        base = int(request.data['crypto']['base'])
        client_crypto_mix = int(request.data['crypto']['client_crypto_mix'])
        server_private_key = int(get_private_key())
        server_crypto_mix = pow(base,server_private_key,prime)
        mutual_private_key = pow(client_crypto_mix,server_private_key,prime)
        key_bytes = any_to_byte(mutual_private_key,"str")
        key_sha256 = byte_to_hash(key_bytes)
        nonce_bytes = generate_nonce()
        key_b64 = any_to_byte(key_sha256,'b64e')
        nonce_b64 = any_to_byte(nonce_bytes,'b64e')
        data = {"session_key":key_b64,
                "session_nonce":nonce_b64}
        session = Session(**data)
        session.save()
        return Response({"server_crypto_mix":server_crypto_mix, "session_id":session.session_id}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_create(request):
    try:
        plain_text = decrypt(request)
        hotel_dic = json.loads(plain_text)
        hotel_data = hotel_dic['hotel']
        hotel = Hotel(**hotel_data)
        hotel.save()
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cypher_text = encrypt(request,hotel_str)
        return Response({"res" : cypher_text}, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['GET'])
def hotel_read(request, req_id):
    try:
        id = req_id # hotel/read/123 # id = request.GET['id'] > hotel/read?id=123
        hotel = Hotel.objects.get(hotel_id=id)
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cypher_text = encrypt(request,hotel_str)
        return Response({"res" : cypher_text}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_delete(request):
    try:
        plain_text = decrypt(request)
        hotel_dic = json.loads(plain_text)
        hotel_data = hotel_dic['hotel']
        hotel = Hotel.objects.get(hotel_id=hotel_data['hotel_id'])
        hotel.delete()
        hotel_str = f"{hotel_data['hotel_id']} deleted"
        cypher_text = encrypt(request,hotel_str)
        return Response({"res" : cypher_text}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_update(request):
    try:
        plain_text = decrypt(request)
        hotel_dic = json.loads(plain_text)
        hotel_data = hotel_dic['hotel']
        hotel = Hotel.objects.get(hotel_id=hotel_data['hotel_id'])
        if 'hotel_id' in hotel_data:
            hotel_data.pop('hotel_id',None)
        hotel.__dict__.update(hotel_data)
        hotel.save()
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cipher_text = encrypt(request,hotel_str)
        return Response({"res":cipher_text}, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)
