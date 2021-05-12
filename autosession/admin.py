from django.contrib import admin
from .models import tune, key, instrument, note, recording

# Register your models here.
admin.site.register(tune)
admin.site.register(key)
admin.site.register(instrument)
admin.site.register(note)
admin.site.register(recording)