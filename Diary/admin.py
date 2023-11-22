from django.contrib import admin
from .models import Diary 

class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_time')
    
    '''filter options'''
    list_filter = ('author', )

    '''10 items per page'''
    list_per_page = 10

admin.site.register(Diary, DiaryAdmin)