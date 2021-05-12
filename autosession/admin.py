from django.contrib import admin
from .models import Tune, Key, Instrument, Note, Recording

# Register your models here.
admin.site.register(Tune)
admin.site.register(Key)
admin.site.register(Instrument)
admin.site.register(Note)
admin.site.register(Recording)