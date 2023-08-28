
from django.contrib import admin

from .models import *

from django_summernote.admin import SummernoteModelAdmin
from .models import Ads


class AdsAdmin(SummernoteModelAdmin):
    summernote_fields = ('Content',)


admin.site.register(Ads, AdsAdmin)

admin.site.register(Response)
