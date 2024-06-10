from django.urls import path
from .views import AgencyOverview, AgencyAwards, AgencyNewAwardsCount, AgencyAwardsCount

# profile app urls 
urlpatterns = [
    path("agency/<str:toptier_code>/", AgencyOverview.as_view(), name="agency_overview"),
    path("agency/<str:toptier_code>/awards/", AgencyAwards.as_view(), name="agency_awards"),
    path("agency/<str:toptier_code>/awards/new/count/", AgencyNewAwardsCount.as_view(), name="agency_new_awards_count"),
    path("agency/awards/count/", AgencyAwardsCount.as_view(), name="agency_awards_count"),
]