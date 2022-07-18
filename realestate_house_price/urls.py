from django.urls import path


from realestate_house_price.views.views import (
                                        HousePriceCodeData,
                                        HousePriceEstimateErrorData,
                                        HousePriceStateTotalData,
)

from realestate_house_price.views.house_price_views import(
                                        HousePriceTopStateData,
                                        HousePriceTopCountitesData,
                                        HousePriceStateTopCountiesData,
)


urlpatterns = [

    # House_Price Code Data
    path('code/data', HousePriceCodeData.as_view(), name='house_price_code_data'),
    # House_Price Estimate/Error Data
    path('estimate_error/data', HousePriceEstimateErrorData.as_view(),
        name='house_price_estimate_error_data'),
    # House_Price_State_Total Data
    path('state_total/data', HousePriceStateTotalData.as_view(),
        name='house_price_state_total_data'),

    # House_Price_Top_State_Data
    path('total/top_state/data', HousePriceTopStateData.as_view(),
        name='house_price_top_state_data'),
    # House_Price_Top_Counties_Data
    path('total/top_countites/data', HousePriceTopCountitesData.as_view(),
        name='house_price_top_counties_data'),
    # House_Price_State_Top_Counties_Data
    path('state/top_counties/data', HousePriceStateTopCountiesData.as_view(),
        name='house_price_state_top_counties_data')

]
