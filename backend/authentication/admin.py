from django.contrib import admin
from authentication.models import User
from django.contrib.auth.admin import UserAdmin
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserModel(UserAdmin):
    
    add_form = CustomUserCreationForm  
    form = CustomUserChangeForm  
    model = User  

    list_display = ('username', 'email', 'role', 'is_active', 'is_deleted', 'is_staff', 'is_superuser', 'is_verified', 'created_on', 'created_by', 'modified_on', 'modified_by')
    list_filter = ('is_active', 'is_deleted', 'is_staff')
    fieldsets = (  
        ('User Info', {'fields': ('username', 'password', 'email', 'phone',)}),  
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'is_deleted', 'is_verified',)}),  
        ('User Settings', {'fields': ('created_on', 'created_by', 'modified_by', 'modified_on')}),  
        ('Group Settings', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active','role','phone','is_verified', 'created_by')}  
        ),  
    )  
    search_fields = ('username', 'email')
    list_per_page = 500
    readonly_fields = ["created_on", 'modified_on']
    filter_horizontal = ()  