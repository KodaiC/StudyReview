from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "type")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don\'t match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("email", "password", "type", "is_active", "is_admin")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "username", "type", "is_admin")
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "type", "content", "introduction", "url", "icon", "tags", "subjects")}),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "type",
                "password1",
                "password2",
                "is_active",
                "is_admin",
            ),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


@admin.register(Rating)
class Rating(admin.ModelAdmin):
    pass


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
