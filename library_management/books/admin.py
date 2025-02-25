from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import User
from .models import Book, Loan

# Register your models here.
admin.site.unregister(User)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')

    # def clean(self):
    #     """Ensure is_staff is True if is_superuser is selected."""
    #     cleaned_data = super().clean()
    #     is_staff = cleaned_data.get('is_staff', False)
    #     is_superuser = cleaned_data.get('is_superuser', False)

    #     if is_superuser:
    #         cleaned_data['is_staff'] = True  # Auto-enable staff for admins

    #     return cleaned_data
    
    def clean_is_staff(self):
        is_staff = self.cleaned_data.get('is_staff')
        is_superuser = self.cleaned_data.get('is_superuser')

        if is_superuser and not is_staff:
            raise forms.ValidationError("Admin users must be staff.")
        return is_staff


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    list_per_page = 30


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'page_count', 'availability')
    ordering = ('-id',)
    list_per_page = 30
    
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'returned_at')
    ordering = ('-id',)
    list_per_page = 30