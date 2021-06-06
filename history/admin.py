from django.contrib import admin

from history.models import ReservartionHistory
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(ReservartionHistory, HistoryAdmin)