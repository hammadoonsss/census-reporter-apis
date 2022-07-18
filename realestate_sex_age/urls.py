from django.urls import path

from realestate_sex_age.views.views import (SexAgeCodeData,
                                      SexAgeEstimateErrorData,
                                      SexAgeStateTotalData)

from realestate_sex_age.views.sex_age_views import(
                                            SexAgeTopStateData,
                                            SexAgeTopCountitesData,
                                            SexAgeStateTopCountiesData)


urlpatterns = [

    # Sex_Age_Code Data
    path('code/data', SexAgeCodeData.as_view(), name="sex_age_code_data"),
    # Sex_Age_Estimate_Error Data
    path('estimate_error/data', SexAgeEstimateErrorData.as_view(),
         name="sex_age_estimate_error_data"),
    # Sex_Age_State_Total Data
    path('state_total/data', SexAgeStateTotalData.as_view(),
         name='sex_age_state_total_data'),
    
    # Sex_Age_Top_State_Data
    path('total/top_state/data', SexAgeTopStateData.as_view(),
        name='sex_age_top_state_data'),
    # Sex_Age_Top_Counties_Data
    path('total/top_countites/data', SexAgeTopCountitesData.as_view(),
        name='sex_age_top_counties_data'),
    # Sex_Age_State_Top_Counties_Data
    path('state/top_counties/data', SexAgeStateTopCountiesData.as_view(),
        name='sex_age_state_top_counties_data')

]
