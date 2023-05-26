import django_filters
from .models import User, Profile


########################################################################
class UserFilter(django_filters.FilterSet):
    role = django_filters.ChoiceFilter(choices=User.ROLES)

    class Meta:
        model = User
        fields = ['role', 'username', 'email', 'id']


########################################################################
class ProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user__username')
    bio_contains = django_filters.CharFilter(field_name='bio', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['username', 'bio_contains', 'id']
