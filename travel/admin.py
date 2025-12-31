from django.contrib import admin
from .models import Travel

class TravelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    filter_horizontal = ('tags',)

admin.site.register(Travel, TravelAdmin)