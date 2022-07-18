from django.urls import path


from realestate_occupancy.views.views import (
    OccupancyCodeData,
    OccupancyEstimateErrorData,
    OccupancyStateTotalData
)


from realestate_occupancy.views.occupancy_views import (
    OccupancyTopStateData,
    OccupancyTopCountitesData,
    OccupancyStateTopCountiesData
)

urlpatterns = [

    # Occupancy Code Data
    path('code/data', OccupancyCodeData.as_view(), name='occupancy_code_data'),
    # Occupancy Estimate/Error Data
    path('estimate_error/data', OccupancyEstimateErrorData.as_view(),
         name='occupancy_estimate_error_data'),
    # Occupancy_State_Total Data
    path('state_total/data', OccupancyStateTotalData.as_view(),
         name='occupancy_state_total_data'),

    # Occupancy_Top_State_Data
    path('total/top_state/data', OccupancyTopStateData.as_view(),
         name='occupancy_top_state_data'),
    # Occupancy_Top_Counties_Data
    path('total/top_countites/data', OccupancyTopCountitesData.as_view(),
         name='occupancy_top_counties_data'),
    # Occupancy_State_Top_Counties_Data
    path('state/top_counties/data', OccupancyStateTopCountiesData.as_view(),
         name='occupancy_state_top_counties_data')

]
