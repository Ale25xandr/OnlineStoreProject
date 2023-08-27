from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('ads/', AdsList.as_view(), name='Ads'),
    path('', StartView.as_view(), name='start'),
    path('ads/<int:pk>', AdsDetail.as_view(), name='ads_one'),
    path('logout/', logout_user, name='logout'),
    path('my_ads/', MyAdsList.as_view(), name='my_ads'),
    path('my_responses/', MyResponses.as_view(), name='my_resp'),
    path('create_ads/', AdsCreate.as_view(), name='ads_create'),
    path('delete_resp/<int:pk>', DeleteResponse.as_view(), name='del_resp'),
    path('response/<int:pk>', ResponseDetail.as_view(), name='r_det'),
    path('response_accepted/', ResponseDetail.accept, name='r_a'),
    path('response_create/<int:pk>', ResponseCreate.as_view(), name='r_c'),
    path('registrations/code', Registration_code.as_view(), name='code',),
    path('check/', CheckView, name='check'),
    path('ads_update/<int:pk>', AdsUpdate.as_view(), name='a_u'),
    path('search/', MyResponsesSearch.as_view(), name='search')
]

