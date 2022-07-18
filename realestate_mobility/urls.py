from django.urls import path

from realestate_mobility.views.views import (
    MobilityCodeData,
    MobilityEstimateErrorData,
    MobilityStateTotalData,
)

from realestate_mobility.views.mobility_views import (
    MobilityTopStateData,
    MobilityTopCountitesData,
    MobilityStateTopCountiesData
)


urlpatterns = [

    # Mobility Code Data
    path('code/data', MobilityCodeData.as_view(), name='mobility_code_data'),
    # Mobility Estimate/Error Data
    path('estimate_error/data', MobilityEstimateErrorData.as_view(),
         name='mobility_estimate_error_data'),
    # Mobility_State_Total Data
    path('state_total/data', MobilityStateTotalData.as_view(),
         name='mobility_state_total_data'),

    # Mobility_Top_State_Data
    path('total/top_state/data', MobilityTopStateData.as_view(),
         name='mobility_top_state_data'),
    # Mobility_Top_Counties_Data
    path('total/top_countites/data', MobilityTopCountitesData.as_view(),
        name='mobility_top_counties_data'),
    # Mobility_State_Top_Counties_Data
    path('state/top_counties/data', MobilityStateTopCountiesData.as_view(),
        name='mobility_state_top_counties_data')
]
