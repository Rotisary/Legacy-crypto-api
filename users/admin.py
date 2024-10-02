from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Wallet, Fund

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'user_id', 'username', 'name', 'date_joined']
    search_fields = ['email', 'username', 'user_id', 'name']
    readonly_fields = ['date_joined', 'last_login']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__name', 'user__username', 'balance']
    search_fields = ['user__email', 'user__username', 'user__name', 'user__user_id']


# class WalletAdmin(admin.ModelAdmin):



class FundAdmin(admin.ModelAdmin):
    list_display = ['owner__user__name', 'amount']
    search_fields = ['owner__user__email', 'owner__user__username', 'owner__user__name', 'owner__user__user_id']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet)
admin.site.register(Fund, FundAdmin)
