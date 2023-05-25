from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, Group, Permission


########################################################################
class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('blogger', 'Blogger'),
    )
    role = models.CharField(choices=ROLES, default='blogger', max_length=10)

    # auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse accessor for 'users.User.groups'.
        # HINT: Add or change a related_name argument to the definition for 'auth.User.groups' or 'users.User.groups'.
    # users.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'users.User.groups' clashes with reverse accessor for 'auth.User.groups'.
        # HINT: Add or change a related_name argument to the definition for 'users.User.groups' or 'auth.User.groups'.
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    # auth.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 'users.User.user_permissions'.
        # HINT: Add or change a related_name argument to the definition for 'auth.User.user_permissions' or 'users.User.user_permissions'.
    # users.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'users.User.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'.
        # HINT: Add or change a related_name argument to the definition for 'users.User.user_permissions' or 'auth.User.user_permissions'.
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )


########################################################################
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
