from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, OtpCode


# Unregister the default User admin
# admin.site.unregister(User)

# class UserProfileInline(admin.StackedInline):
#     """Inline admin for UserProfile in User admin."""
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = "User Profile"

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """Custom admin for User model with UserProfile inline."""
#     inlines = (UserProfileInline,)
#     list_display = ('username', 'email', 'is_active', 'is_staff', 'phone_number')
#     list_filter = ('is_active', 'is_staff')
#     search_fields = ('username', 'email', 'userprofile__phone_number')
#     list_per_page = 20

#     def phone_number(self, obj):
#         """Display phone number from UserProfile."""
#         return obj.userprofile.phone_number if hasattr(obj, 'userprofile') else '-'
#     phone_number.short_description = "Phone Number"

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    """Admin interface for OtpCode model."""
    list_display = ('phone_number', 'code', 'created_at')
    search_fields = ('phone_number', 'code')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20
