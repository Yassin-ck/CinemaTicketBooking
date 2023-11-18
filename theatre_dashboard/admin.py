from django.contrib import admin
from .models import (
    TheareOwnerDetails,
    TheatreDetails,
    ScreenDetails,
    ScreenSeatArrangement,
    Shows,
    ShowTime,
    ShowDates
)

# Register your models here.
admin.site.register(TheareOwnerDetails)
admin.site.register(ShowDates)
admin.site.register(TheatreDetails)
admin.site.register(ScreenDetails)
admin.site.register(ScreenSeatArrangement)
admin.site.register(Shows)
admin.site.register(ShowTime)
