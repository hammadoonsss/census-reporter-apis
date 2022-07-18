from django.urls import path


from realestate_poverty.views.views import (PovertyCodeData,
                                            PovertyEstimateErrorData,
                                            PovertyStateTotalData,)

from realestate_poverty.views.poverty_views import (
    PovertyTopStateData,
    PovertyTopCountiesData,
    PovertyStateTopCountiesData)


urlpatterns = [

    # Poverty Code Data
    path('code/data', PovertyCodeData.as_view(),
         name='poverty_code_data'),
    # Poverty Estimate/Error Data
    path('estimate_error/data', PovertyEstimateErrorData.as_view(),
         name='poverty_estimate_error_data'),
    # Poverty_State_Total Data
    path('state_total/data', PovertyStateTotalData.as_view(),
         name='poverty_state_total_data'),

    # Poverty_Top_State_Data
    path('total/top_state/data', PovertyTopStateData.as_view(),
         name='poverty_top_state_data'),
    # Poverty_Top_Counties_Data
    path('total/top_counties/data', PovertyTopCountiesData.as_view(),
         name='poverty_top_counties_data'),
    # Poverty_State_Top_Countites_Data
    path('state/top_counties/data', PovertyStateTopCountiesData.as_view(),
         name='poverty_state_top_counties_data')

]
