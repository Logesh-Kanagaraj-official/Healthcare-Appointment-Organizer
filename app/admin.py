from django.contrib import admin
from .models import Register, Patent

# Customize the admin site header
admin.site.site_header  = "Healthcare Appointment Organizer — Admin"
admin.site.site_title   = "Healthcare Admin"
admin.site.index_title  = "Dashboard"

# ── Registered Users ──────────────────────────────────────────────
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display  = ('id', 'uname', 'email', 'mobno')   # columns shown in list
    search_fields = ('uname', 'email', 'mobno')           # search bar fields
    ordering      = ('id',)
    list_per_page = 20

# ── Appointment / Booking History ─────────────────────────────────
@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'fname', 'uname', 'docname', 'patdt', 'mobno', 'email', 'prpse')
    search_fields = ('fname', 'uname', 'docname', 'email', 'mobno')
    list_filter   = ('docname', 'patdt')                  # filter sidebar
    ordering      = ('-patdt',)                           # newest first
    list_per_page = 20
    date_hierarchy = 'patdt'                              # drill down by date