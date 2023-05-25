from rest_framework import viewsets
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsAdmin, IsEditor, IsBlogger


########################################################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]


########################################################################
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]
