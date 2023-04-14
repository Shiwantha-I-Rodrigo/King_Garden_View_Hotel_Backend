from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation
from .serializers import Hotel_Serializer, Room_Type_Serializer, Room_Serializer, User_Role_Serializer, User_Serializer, Customer_Serializer, Reservation_Serializer
from .crypt import get_initials, get_private_key


@api_view(['GET'])
def crypto_in(request):
    headers = request.META
    res = {"prime":get_initials()[0],"base":get_initials()[1]}
    return Response(res)


@api_view(['POST'])
def crypto_out(request):
    headers = request.META
    prime = int(request.data['crypto']['prime'])
    base = int(request.data['crypto']['base'])
    client_crypto_mix = int(request.data['crypto']['client_crypto_mix'])
    private_key = int(get_private_key())
    server_crypto_mix = pow(base,private_key,prime)
    user_token = pow(client_crypto_mix,private_key,prime)
    res={"server_crypto_mix":server_crypto_mix, "secret":user_token}
    return Response(res)


@api_view(['POST'])
def hotel_create(request):
    data = request.data['hotel']
    serializer = Hotel_Serializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def hotel_read(request, req_id):
    headers = request.META
    try:
        id = req_id # add hotel/read/123/ to the end of the url > id=123
        # id = request.GET['id'] # add hotel/delete?id=123 to the end of url > id=123
        hotel = Hotel.objects.get(hotel_id=id)
    except Hotel.DoesNotExist :
        return Response({'error':'hotel does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = Hotel_Serializer(hotel)
    return Response(serializer.data)


@api_view(['POST'])
def hotel_delete(request):
    headers = request.META
    try:
        hotel = Hotel.objects.get(hotel_id=request.data['hotel']['hotel_id'])
    except hotel.DoesNotExist:
        return Response({'error':'hotel does not exist'}, status=status.HTTP_404_NOT_FOUND)
    hotel.delete()
    return Response(status=201)


@api_view(['POST'])
def hotel_update(request):
    headers = request.META
    try:
        hotel = Hotel.objects.get(hotel_id=request.data['hotel']['hotel_id'])
    except hotel.DoesNotExist:
        return Response({'error':'hotel does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = Hotel_Serializer(hotel, data=request.data['hotel'])
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
