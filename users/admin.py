from django.contrib import admin
from .models import Player#,userdata
# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
	list_display = ('user', 'current_level', 'current_level_time','points', 'bonus_attempted')
# class userdataadmin(admin.ModelAdmin):
# 	list_display=('username','email','roll','referral_count')
admin.site.register(Player, PlayerAdmin)
# admin.site.register( userdata, userdataadmin)

