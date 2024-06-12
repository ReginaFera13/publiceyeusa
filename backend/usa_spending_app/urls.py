from django.urls import path
from .agency_views import AgencyOverview, AgencyAwards, AgencyNewAwardsCount, AgencyAwardsCount, BudgetFunction, BudgetFunctionCount, BudgetaryResources, FederalAccountList, FederalAccountCount, ObjectClassList, ObjectClassCount, ObligationsByAwardCategory, ProgramActivityList, ProgramActivityCount, SubAgencyList, SubAgencyCount, BureauFederalAccountList, SubcomponentList, TasObjectClassList, TasProgramActivityList
from .autocomplete_views import TasAutocompleteA, TasAutocompleteAid,TasAutocompleteAta, TasAutocompleteBpoa, TasAutocompleteEpoa, TasAutocompleteMain, TasAutocompleteSub, AwardingAgencyAutocomplete, AwardingAgencyOfficeAutocomplete, FundingAgencyOfficeAutocomplete, CfdaAutocomplete, CityAutocomplete, RecipientAutocomplete

# profile app urls 
urlpatterns = [
    # Agency URLs:
    path("agency/<str:toptier_code>/", AgencyOverview.as_view(), name="agency_overview"),
    path("agency/<str:toptier_code>/awards/", AgencyAwards.as_view(), name="agency_awards"),
    path("agency/<str:toptier_code>/awards/new/count/", AgencyNewAwardsCount.as_view(), name="agency_new_awards_count"),
    path("agency/awards/count/", AgencyAwardsCount.as_view(), name="agency_awards_count"),
    path("agency/<str:toptier_code>/budget_function/", BudgetFunction.as_view(), name="budget_function"),
    path("agency/<str:toptier_code>/budget_function/count/", BudgetFunctionCount.as_view(), name="budget_function_count"),
    path("agency/<str:toptier_code>/budgetary_resources/", BudgetaryResources.as_view(), name="budgetary_resources"),
    path("agency/<str:toptier_code>/federal_account/", FederalAccountList.as_view(), name="federal_account_list"),
    path("agency/<str:toptier_code>/federal_account/count/", FederalAccountCount.as_view(), name="federal_account_count"),
    path("agency/<str:toptier_code>/object_class/", ObjectClassList.as_view(), name="object_class_list"),
    path("agency/<str:toptier_code>/object_class/count/", ObjectClassCount.as_view(), name="object_class_count"),
    path("agency/<str:toptier_code>/obligations_by_award_category/", ObligationsByAwardCategory.as_view(), name="obligations_by_award_category"),
    path("agency/<str:toptier_code>/program_activity/", ProgramActivityList.as_view(), name="program_activity_list"),
    path("agency/<str:toptier_code>/program_activity/count/", ProgramActivityCount.as_view(), name="program_activity_count"),
    path("agency/<str:toptier_code>/sub_agency/", SubAgencyList.as_view(), name="sub_agency_list"),
    path("agency/<str:toptier_code>/sub_agency/count/", SubAgencyCount.as_view(), name="sub_agency_count"),
    path("agency/<str:toptier_code>/sub_components/<str:bureau_slug>/", BureauFederalAccountList.as_view(), name="bureau_federal_account_list"),
    path("agency/<str:toptier_code>/sub_components/", SubcomponentList.as_view(), name="sub_components_list"),
    path("agency/treasury_account/<str:tas>/object_class/", TasObjectClassList.as_view(), name="treasury_account_object_class_list"),
    path("agency/treasury_account/<str:tas>/program_activity/", TasProgramActivityList.as_view(), name="treasury_account_program_activity_list"),
    
    # Autocomplete URLs:
    path("autocomplete/accounts/a/", TasAutocompleteA.as_view(), name="tas_autocomplete_a"),
    path("autocomplete/accounts/aid/", TasAutocompleteAid.as_view(), name="tas_autocomplete_aid"),
    path("autocomplete/accounts/ata/", TasAutocompleteAta.as_view(), name="tas_autocomplete_ata"),
    path("autocomplete/accounts/bpoa/", TasAutocompleteBpoa.as_view(), name="tas_autocomplete_bpoa"),
    path("autocomplete/accounts/epoa/", TasAutocompleteEpoa.as_view(), name="tas_autocomplete_epoa"),
    path("autocomplete/accounts/main/", TasAutocompleteMain.as_view(), name="tas_autocomplete_main"),
    path("autocomplete/accounts/sub/", TasAutocompleteSub.as_view(), name="tas_autocomplete_sub"),
    path("autocomplete/awarding_agency/", AwardingAgencyAutocomplete.as_view(), name="autocomplete_awarding_agency"),
    path("autocomplete/awarding_agency_office/", AwardingAgencyOfficeAutocomplete.as_view(), name="autocomplete_awarding_agency_office"),
    path("autocomplete/funding_agency_office/", FundingAgencyOfficeAutocomplete.as_view(), name="autocomplete_funding_agency_office"),
    path("autocomplete/cfda/", CfdaAutocomplete.as_view(), name="autocomplete_cfda"),
    path("autocomplete/city/", CityAutocomplete.as_view(), name="autocomplete_city"),
    path("autocomplete/recipient/", RecipientAutocomplete.as_view(), name="autocomplete_recipient"),
]