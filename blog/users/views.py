from rest_framework import viewsets
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsAdmin
from .filters import UserFilter, ProfileFilter


########################################################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filterset_class = UserFilter


########################################################################
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdmin]
    filterset_class = ProfileFilter
