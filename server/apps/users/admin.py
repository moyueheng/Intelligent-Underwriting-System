from django.contrib import admin

# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin


class CUserAdmin(UserAdmin):
    # some fields here

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password1"):
            obj.set_password(form.cleaned_data["password1"])
        super().save_model(request, obj, form, change)


admin.site.register(User, CUserAdmin)
