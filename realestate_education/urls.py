from django.urls import path


from realestate_education.views.views import (EductionCodeData,
                                        EducationEstimateErrorData,
                                        EducationStateTotalData,)

from realestate_education.views.education_views import (EducationTopStateData,
                                                        EducationTopCountitesData,
                                                        EducationStateTopCountiesData)

urlpatterns = [

    # Education Code Data
    path('code/data', EductionCodeData.as_view(), name='education_code_data'),
    # Education Estimate/Error Data
    path('estimate_error/data', EducationEstimateErrorData.as_view(),
        name='education_estimate_error_data'),
    # Education_State_Total Data
    path('state_total/data', EducationStateTotalData.as_view(),
        name='education_state_total_data'),

    # Education_Top_State_Data
    path('total/top_state/data', EducationTopStateData.as_view(),
        name='education_top_state_data'),
    # Education_Top_Counties_Data
    path('total/top_countites/data', EducationTopCountitesData.as_view(),
        name='education_top_counties_data'),
    # Education_State_Top_Counties_Data
    path('state/top_counties/data', EducationStateTopCountiesData.as_view(),
        name='education_state_top_counties_data')

]
