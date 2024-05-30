from django.urls import path
from .views import AllAffiliations, An_Affiliation

# paths for interest_app views for all interest categories and an interest category
urlpatterns = [
    path("", AllAffiliations.as_view(), name="all_interest_categories"),
    path("<str:interest>/", An_Affiliation.as_view(), name="an_interest"),
]