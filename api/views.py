# views.py
from rest_framework import status
from django.db import models
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer,TeamSerializer,ProfileSerializer,ManagerSerializer,SlotSerializer,ReserveSlotSerializer,FixtureSerializer
from user.models import Profile,Manager,Team, Slot,Reserve_slot,Fixture
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(f"Serializer data: {serializer.data}")  # Debug statement
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })
    else:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
 
class ProfileCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProfileUpdateDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None

    def get(self, request, format=None):
        profile = self.get_object()
        if profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        profile = self.get_object()
        if profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        profile = self.get_object()
        if profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

# class TeamCreateAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

class TeamCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    
class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        try:
            print(self.request.FILES)
            logger.debug(f"Files: {self.request.FILES}")
            logger.debug(f"Data: {self.request.data}")
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"Error creating manager: {e}")
            raise e

    def get_queryset(self):
        queryset = super().get_queryset()
        # Ensure users can only access their own manager profile
        return queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this manager profile.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this manager profile.")
        instance.delete()
        
class SlotViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    

#fixture 

class ReserveSlotViewSet(viewsets.ModelViewSet):
    queryset = Reserve_slot.objects.all()
    serializer_class = ReserveSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter queryset based on the request user's manager team
        return self.queryset.filter(team=self.request.user.manager.team)

    def perform_create(self, serializer):
        serializer.save()

class FixtureViewSet(viewsets.ModelViewSet):
    queryset = Fixture.objects.all()
    serializer_class = FixtureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter queryset based on the request user's manager team
        return self.queryset.filter(
                models.Q(team_1__team_name=self.request.user.manager.team) |
                models.Q(team_2__team_name=self.request.user.manager.team)
            )