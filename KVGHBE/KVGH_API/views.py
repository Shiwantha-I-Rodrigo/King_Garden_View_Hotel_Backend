from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room_Type, Room, User_Role, User, Customer, Reservation
from .serializers import Hotel_Serializer, Room_Type_Serializer, Room_Serializer, User_Role_Serializer, User_Serializer, Customer_Serializer, Reservation_Serializer


@api_view(['GET'])
def get_home(request):
    return Response({"response":"home"})


@api_view(['GET'])
def get_room(request, id):
    try:
        room = Room.objects.get(room_id=id)
    except Room.DoesNotExist :
        return Response({'error':'does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = Room_Serializer(room)
    return Response(serializer.data)


@api_view(['POST'])
def add_room(request):
    serializer = Room_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
