from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', )}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_photo', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
