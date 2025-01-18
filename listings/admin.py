from django.contrib import admin
from listings.models import Publication

# Register your models here.
class PublicationAdmin(admin.ModelAdmin):
    list_display= ('message', 'date')
admin.site.register(Publication, PublicationAdmin)