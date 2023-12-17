from django.contrib import admin
from .models import Report
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    readonly_fields = ('created_at', 'id')
    
admin.site.register(Report, UserAdmin)
