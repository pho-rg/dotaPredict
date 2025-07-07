from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import check_password

from .models import User
from .serializers import UserSerializer
from .permissions import IsAnalyst

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAnalyst])
def getUsers(request):
    try:
        users = User.objects.values('name', 'email', 'role')
        return Response(list(users), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAnalyst])
def getUser(request, pk):
    try:
        user = User.objects.filter(id=pk).values('name', 'email', 'role').first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(user, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAnalyst])
def createUser(request):
    try:
        data = request.data.copy()
        data['password'] = make_password(data['password'])

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAnalyst])
def updateUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        data = request.data.copy()

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAnalyst])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def register(request):
    data = request.data

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    if not name or not email or not password or not confirmPassword:
        return Response({'detail': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirmPassword:
        return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_412_PRECONDITION_FAILED)

    if User.objects.filter(email=email).exists():
        return Response({'detail': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    user_data = {
        'name': name,
        'email': email,
        'password': make_password(password),
        'role': 'viewer'
    }

    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = AccessToken.for_user(user)
    token['id'] = user.id
    token['role'] = user.role
    token['name'] = user.name
    return Response({
        'token': str(token),
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'name': user.name,
        }
    }, status=status.HTTP_200_OK)
