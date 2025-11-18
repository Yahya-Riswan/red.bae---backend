from django.shortcuts import render
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser



class UserListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = CustomUser.objects.filter(role='user')
        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class RegisterView(APIView):
    def post(self, request):
        data = request.data.copy()

        if CustomUser.objects.filter(email=data.get("email")).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ USERNAME HANDLING — if exists, auto-increment numbers
        original_username = data.get("username")
        new_username = original_username
        counter = 1

        while CustomUser.objects.filter(username=new_username).exists():
            new_username = f"{original_username}{counter}"
            counter += 1

        data["username"] = new_username  

        # 3️⃣ Now validate + save
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "username": new_username
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            # check password
            if not user.check_password(password):
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            # create tokens
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
