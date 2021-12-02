from django.contrib import admin
from .models import User, Match


admin.site.register(Match)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')
