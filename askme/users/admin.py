from django.contrib import admin
from .models import User, Profile
from .forms import UserCreationForm, UserUpdateForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserUpdateForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_staff')
    # activates the filters in the right sidebar on the change list page
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # A list or tuple containing extra CSS classes to apply to the fieldset.
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    # enabled a search box on the admin change page
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    search_fields = ('email',)
    # Set ordering to specify how lists of objects should be ordered in the Django admin views.
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.ordering
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
