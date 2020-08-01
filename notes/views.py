from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    CustomUser,
    Note
)

key = b'DsC2pgO5vaB_uLdR9LilbGXomjGMCDDKTJWvA3OCg8g='

from cryptography.fernet import Fernet

from .serializers import (
    UserSerializer,
    NoteSerializer,
    NoteViewSerializer
)

from .password_hasher import (
    hash_password,
    check_password
)

from django.core.exceptions import ObjectDoesNotExist
process = Fernet(key)

class UserRegistrationView(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save(password=hash_password(request.data.get('password')))
            return Response({'status': 'account created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        params = ['username', 'password']
        for i in params:
            if i not in request.data:
                return Response({'error': '{} missing'.format(i)}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user_check = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'No user by this username'}, status=status.HTTP_404_NOT_FOUND)
        
        if check_password(user_check.password, password):
            return Response({ 'status': 'success', 'userId': user_check.userId }, status=status.HTTP_200_OK)
        else:
            return Response({ 'error': 'Password incorrect' }, status=status.HTTP_403_FORBIDDEN)


class AddNoteView(APIView):
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        try:
            user = CustomUser.objects.get(userId=request.query_params.get('user'))
        except ObjectDoesNotExist:
            return Response({'error': 'No user by this id'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(user=user, note=process.encrypt(bytes(request.data.get('note'), 'utf-8')))
            return Response({ 'status': 'success' }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserNotesListView(APIView):
    serializer_class = NoteViewSerializer
    def get(self, request):
        serialzer = NoteViewSerializer(
            Note.objects.filter(user__userId=request.query_params.get('user')), 
            many=True
            )
        for i in serialzer.data:
            i['note'] = process.decrypt(bytes(i['note'], 'utf-8'))
        return Response({serializer.data}, status=status.HTTP_200_OK)
