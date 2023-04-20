from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation, Session
from .serializers import Hotel_Serializer, Room_Type_Serializer, Room_Serializer, User_Role_Serializer, User_Serializer, Customer_Serializer, Reservation_Serializer, Session_Serializer
from .crypt import get_initials, get_private_key,generate_nonce, chacha20_encrypt, chacha20_decrypt, any_to_byte, byte_to_any
import sys, json


@api_view(['GET'])
def crypto_in(request):
    try:
        initials = get_initials()
        res = {"prime":initials[0],"base":initials[1]}
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
        key = any_to_byte(mutual_private_key,True)
        nonce = generate_nonce()
        data = {"session_key":key,
                "session_nonce":nonce}
        session = Session(**data)
        session.save()
        nonce_str = byte_to_any(nonce,'b64')
        return Response({"server_crypto_mix":server_crypto_mix, "session_id":session.session_id, "session_nonce":nonce_str}, status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_create(request):
    try:
        session = Session.objects.get(session_id = request.data['session_id'])
        hotel_data = request.data['hotel']
        hotel = Hotel(**hotel_data)
        hotel.save()
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cipher = chacha20_encrypt(session.session_key, session.session_nonce,hotel_str)
        res = {"res":byte_to_any(cipher,"b64")}
        return Response(res, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['GET'])
def hotel_read(request, req_id):
    session = Session.objects.get(session_id = request.data['session_id'])
    try:
        id = req_id # add hotel/read/123/ to the end of the url > id=123
        # id = request.GET['id'] # add hotel/delete?id=123 to the end of url > id=123
        hotel = Hotel.objects.get(hotel_id=id)
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cipher = chacha20_encrypt(session.session_key, session.session_nonce,hotel_str)
        res = {"res":byte_to_any(cipher,"b64")}
        return Response(res,status=200)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_delete(request):
    session = Session.objects.get(session_id = request.data['session_id'])
    try:
        hotel = Hotel.objects.get(hotel_id=request.data['hotel']['hotel_id'])
        hotel.delete()
        res = {"res":"record deleted"}
        return Response(res,status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)


@api_view(['POST'])
def hotel_update(request):
    session = Session.objects.get(session_id = request.data['session_id'])
    try:
        hotel = Hotel.objects.get(hotel_id=request.data['hotel']['hotel_id'])
        data = request.data['hotel']
        if 'hotel_id' in data:
            data.pop('hotel_id',None)
        hotel.__dict__.update(data)
        hotel.save()
        hotel_str = json.dumps(model_to_dict(hotel), ensure_ascii=False)
        cipher = chacha20_encrypt(session.session_key, session.session_nonce,hotel_str)
        res = {"res":byte_to_any(cipher,"b64")}
        return Response(res, status=201)
    except:
        ex_type, ex_value, ex_traceback = sys.exc_info() # remove in production
        return Response(f"error > {ex_type} > {ex_value} > {ex_traceback}",status=500)
