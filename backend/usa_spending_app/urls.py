from django.urls import path
from .agency_views import AgencyOverview, AgencyAwards, AgencyNewAwardsCount, AgencyAwardsCount, BudgetFunction, BudgetFunctionCount, BudgetaryResources, FederalAccountList, FederalAccountCount, ObjectClassList, ObjectClassCount, ObligationsByAwardCategory, ProgramActivityList, ProgramActivityCount, SubAgencyList, SubAgencyCount, BureauFederalAccountList, SubcomponentList, TasObjectClassList, TasProgramActivityList

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
]