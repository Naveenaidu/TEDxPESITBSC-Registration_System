from django.contrib import admin

from .models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information',    {'fields': ['participant_id', 'name', 'phone']}),
        ('Event Information',       {'fields': ['barcode', 'registered',
             'checked_in', 'had_lunch', 'had_dinner', 'had_breakfast',
            ]})
    ]
    list_display = ('participant_id', 'name', 'phone')
    search_fields = ('participant_id', 'name', 'barcode')

admin.site.register(Participant, ParticipantAdmin)

class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1
    # fields = ('name', 'gender', 'barcode', 'participant_id', '/checked_in', 'had_lunch', 'had_dinner', 'had_breakfast')

