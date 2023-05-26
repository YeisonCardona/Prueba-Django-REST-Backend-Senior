from django.contrib import admin
from .models import User, Profile


########################################################################
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ['username', 'email']
    list_filter = ('role',)


admin.site.register(User, UserAdmin)


########################################################################
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ['user__username', 'bio']


admin.site.register(Profile, ProfileAdmin)
