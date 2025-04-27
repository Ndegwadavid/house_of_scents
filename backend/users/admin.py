from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'name', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Personal Info', {'fields': ('address', 'phone', 'receive_stock_alerts', 'verification_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login', 'verification_token')
    actions = ['make_admin', 'make_superuser']

    def make_admin(self, request, queryset):
        queryset.update(role='admin', is_staff=True, is_active=True)
        self.message_user(request, "Selected users have been made admins.")
    make_admin.short_description = "Set selected users as admins"

    def make_superuser(self, request, queryset):
        queryset.update(role='admin', is_staff=True, is_superuser=True, is_active=True)
        self.message_user(request, "Selected users have been made superusers.")
    make_superuser.short_description = "Set selected users as superusers"
    

##create user with role admin
##from users.models import User
##user = User.objects.get(email='adams1@gmail.com')
##user.role = 'admin'
##user.is_active = True
##user.save()
##exit()