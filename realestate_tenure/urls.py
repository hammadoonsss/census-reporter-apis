from django.urls import path

from realestate_tenure.views.views import (
    TenureCodeData,
    TenureEstimateErrorData,
    TenureStateTotalData
)

from realestate_tenure.views.tenure_views import (
    TenureTopStateData,
    TenureTopCountitesData,
    TenureStateTopCountiesData
)


urlpatterns = [

    # Tenure_Code Data
    path('code/data', TenureCodeData.as_view(), name="tenure_code_data"),
    # Tenure_Estimate_Error Data
    path('estimate_error/data', TenureEstimateErrorData.as_view(),
         name="tenure_estimate_error_data"),
    # Tenure_State_Total Data
    path('state_total/data', TenureStateTotalData.as_view(),
         name='tenure_state_total_data'),

    # Tenure_Top_State_Data
    path('total/top_state/data', TenureTopStateData.as_view(),
        name='tenure_top_state_data'),
    # Tenure_Top_Counties_Data
    path('total/top_countites/data', TenureTopCountitesData.as_view(),
        name='tenure_top_counties_data'),
    # Tenure_State_Top_Counties_Data
    path('state/top_counties/data', TenureStateTopCountiesData.as_view(),
        name='tenure_state_top_counties_data')

]
