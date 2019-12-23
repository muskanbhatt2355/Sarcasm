from django.contrib import admin
from .models import Level
# Register your models here.
class LevelAdmin(admin.ModelAdmin):
	list_display = ('level_id', 'question', 'answer', 'title')

admin.site.register(Level, LevelAdmin)
