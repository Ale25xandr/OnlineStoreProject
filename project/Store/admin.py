from urllib import request

from django.contrib import admin

from .models import *

from django_summernote.admin import SummernoteModelAdmin
from .models import Ads
from .forms import AdsForm


class AdsAdmin(SummernoteModelAdmin):
    summernote_fields = ('Content',)


admin.site.register(Ads, AdsAdmin)

# admin.site.register(Ads)
admin.site.register(User_1)
admin.site.register(Response)
