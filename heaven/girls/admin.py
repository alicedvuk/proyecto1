from django.contrib import admin
from .models import Girl

# Register your models here.
@admin.register(Girl)
class GirlProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'postcode', 'address', 'live_with')
    list_filter = ( 'postcode', 'status')
    #raw_id_fields = ('user',)
    #search_fields = ('name', 'user__username')
    #radio_fields = {'account_type': admin.VERTICAL}
    #date_hierarchy = 'created'
