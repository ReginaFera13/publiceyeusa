from django.urls import path
from .agency_views import AgencyOverview, AgencyAwards, AgencyNewAwardsCount, AgencyAwardsCount, BudgetFunction, BudgetFunctionCount, BudgetaryResources, FederalAccountList, FederalAccountCount, ObjectClassList, ObjectClassCount, ObligationsByAwardCategory, ProgramActivityList, ProgramActivityCount, SubAgencyList, SubAgencyCount, BureauFederalAccountList, SubcomponentList, TasObjectClassList, TasProgramActivityList
from .autocomplete_views import TasAutocompleteA, TasAutocompleteAid,TasAutocompleteAta, TasAutocompleteBpoa, TasAutocompleteEpoa, TasAutocompleteMain, TasAutocompleteSub, AwardingAgencyAutocomplete, AwardingAgencyOfficeAutocomplete, FundingAgencyOfficeAutocomplete, CfdaAutocomplete, CityAutocomplete, RecipientAutocomplete, FundingAgencyAutocomplete, GlossaryAutocomplete, NaicsAutocomplete, PscAutocomplete, LocationAutocomplete
from .award_views import RecipientAwardSpending, AwardRetrieve, AwardAccounts, FederalAccountCount, SubawardCount, TransactionCount, AwardFunding, AwardFundingRollup, AwardLastUpdated
from .budget_functions_views import ListBudgetFunction, ListBudgetSubfunction
from .bulk_download_views import BulkAwardDownload, DownloadListAgencies, ListMonthlyDownloads, DownloadStatus
from .disaster_views import DisasterAgencyCount, DisasterLoansByAgency, DisasterSpendingByAgency, DisasterAwardAmount, DisasterAwardCount, DisasterCfdaCount, DisasterCfdaLoans, DisasterCfdaSpending, DefCodeCount, DisasterFederalAccountCount, DisasterFederalAccountLoans,DisasterFederalAccountSpending, DisasterObjectClassCount, DisasterObjectClassLoans, DisasterObjectClassSpending, DisasterRecipientCount, DisasterRecipientLoans, DisasterRecipientSpending, DisasterSpendingByGeography

# USASpending app urls 
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
    path("autocomplete/funding_agency/", FundingAgencyAutocomplete.as_view(), name="autocomplete_funding_agency"),
    path("autocomplete/glossary/", GlossaryAutocomplete.as_view(), name="autocomplete_glossary"),
    path("autocomplete/naics/", NaicsAutocomplete.as_view(), name="autocomplete_naics"),
    path("autocomplete/psc/", PscAutocomplete.as_view(), name="autocomplete_psc"),
    path("autocomplete/location/", LocationAutocomplete.as_view(), name="autocomplete_location"),

    # Award URLs:
    path("award_spending/recipient/", RecipientAwardSpending.as_view(), name="recipient_award_spending"),
    path("awards/<str:award_id>/", AwardRetrieve.as_view(), name="award_retrieve"),
    path("award/accounts/", AwardAccounts.as_view(), name="award_accounts"),
    path("award/count/federal_account/<str:award_id>/", FederalAccountCount.as_view(), name="federal_account_count"),
    path("award/count/subaward/<str:award_id>/", SubawardCount.as_view(), name="subaward_count"),
    path("award/count/transaction/<str:award_id>/", TransactionCount.as_view(), name="transaction_count"),
    path("award/funding/", AwardFunding.as_view(), name="award_funding"),
    path("award/funding_rollup/", AwardFundingRollup.as_view(), name="award_funding_rollup"),
    path("award/last_updated/", AwardLastUpdated.as_view(), name="award_last_updated"),

    # Budget Function URLs:
    path("budget_functions/list_budget_functions/", ListBudgetFunction.as_view(), name="list_budget_functions"),
    path("budget_functions/list_budget_subfunctions/", ListBudgetSubfunction.as_view(), name="list_budget_subfunctions"),

    # Bulk Download URLs:
    path("bulk_download/awards/", BulkAwardDownload.as_view(), name="bulk_download_awards"),
    path("bulk_download/list_agencies/", DownloadListAgencies.as_view(), name="bulk_download_list_agencies"),
    path("bulk_download/list_monthly_files/", ListMonthlyDownloads.as_view(), name="bulk_download_list_monthly_files"),
    path("bulk_download/status/", DownloadStatus.as_view(), name="bulk_download_status"),

    # Disaster URLs:
    path("disaster/agency/count/", DisasterAgencyCount.as_view(), name="disaster_agency_count"),
    path("disaster/agency/loans/", DisasterLoansByAgency.as_view(), name="disaster_agency_loans"),
    path("disaster/agency/spending/", DisasterSpendingByAgency.as_view(), name="disaster_agency_spending"),
    path("disaster/award/amount/", DisasterAwardAmount.as_view(), name="disaster_award_amount"),
    path("disaster/award/count/", DisasterAwardCount.as_view(), name="disaster_award_count"),
    path("disaster/cfda/count/", DisasterCfdaCount.as_view(), name="disaster_cfda_count"),
    path("disaster/cfda/loans/", DisasterCfdaLoans.as_view(), name="disaster_cfda_loans"),
    path("disaster/cfda/spending/", DisasterCfdaSpending.as_view(), name="disaster_cfda_spending"),
    path("disaster/def_code/count/", DefCodeCount.as_view(), name="def_code_count"),
    path("disaster/federal_account/count/", DisasterFederalAccountCount.as_view(), name="disaster_federal_account_count"),
    path("disaster/federal_account/loans/", DisasterFederalAccountLoans.as_view(), name="disaster_federal_account_loans"),
    path("disaster/federal_account/spending/", DisasterFederalAccountSpending.as_view(), name="disaster_federal_account_spending"),
    path("disaster/object_class/count/", DisasterObjectClassCount.as_view(), name="disaster_object_class_count"),
    path("disaster/object_class/loans/", DisasterObjectClassLoans.as_view(), name="disaster_object_class_loans"),
    path("disaster/object_class/spending/", DisasterObjectClassSpending.as_view(), name="disaster_object_class_spending"),
    path("disaster/recipient/count/", DisasterRecipientCount.as_view(), name="disaster_recipient_count"),
    path("disaster/recipient/loans/", DisasterRecipientLoans.as_view(), name="disaster_recipient_loans"),
    path("disaster/recipient/spending/", DisasterRecipientSpending.as_view(), name="disaster_recipient_spending"),
    path("disaster/spending_by_geography/", DisasterSpendingByGeography.as_view(), name="disaster_spending_by_geography"),
]