# Django Related Imports
from django.contrib import admin
from django.urls import path

# Census Views Import
from realestate_app.views.census_views import(AllCountiesData, AllStatesData, AmericanCommunitySurveyData,
                                              TabulationData, SingleTopicStateData,)

# Database Views Import
from realestate_app.views.views import(TopicCodeData, RaceStateData, RaceErrorEstimateData,
                                       StateCountyDetailData, TopicDetails, UpdateFTPFile,
                                       IncomeErrorEstimateData, )

# Race Views
from realestate_app.views.race_views import (RaceStateTotalData, RaceEstimateStateData,
                                             RaceTotalTopCountiesData, RaceTotalTopStateData,
                                             RaceStateTopCountiesData,
                                             RaceTotalTopStateDataTwo, RaceTotalTopCountiesDataTwo,
                                             RaceStateTopCountiesDataTwo)
# Income Views
from realestate_app.views.income_view import (IncomeStateTotalData,
                                              IncomeTotalTopStateData, IncomeTotalTopCountiesData,
                                              IncomeStateTopCountiesData)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Census_Reporter
    path("tabulation/data/", TabulationData.as_view(),
         name='tabulation_data'),
    path("all_counties/data/", AllCountiesData.as_view(),
         name='all_counties_data'),
    path("all_states/data/", AllStatesData.as_view(),
         name='all_states_data'),
    path("american_community_survey/data/", AmericanCommunitySurveyData.as_view(),
         name='american_community_survey_data'),
    path("single_topic/state_data/", SingleTopicStateData.as_view(),
         name='single_topic_state_data'),


    # Topic_Details
    path('topic/details/', TopicDetails.as_view(), name='topic_details'),
    # Update_FTP_File
    path('update/ftp/', UpdateFTPFile.as_view(), name='update_ftp_file'),
    # Topic_Code_data
    path("topic_code/data/", TopicCodeData.as_view(),
         name='topic_code_data'),


    # Race
    path("race/state/data/", RaceStateData.as_view(),
         name='race_state_data'),
    # State/County
    path("state/county_detail/data/", StateCountyDetailData.as_view(),
         name='state_county_detail_data'),
    # Race_Error/Estimate
    path("race/error_estimate/data/", RaceErrorEstimateData.as_view(),
         name='race_error_estimate_data'),


    # Race_Estimate_State_Data
    path("race_estimate/state/data", RaceEstimateStateData.as_view(),
         name='race_estimate_state_data'),
    # Race_State_Total
    path('race/state/total/data', RaceStateTotalData.as_view(),
         name='race_state_total_data'),
    # Race_Total_Top_State_Data
    path('race/total/top_state/data', RaceTotalTopStateData.as_view(),
         name='race_total_top_state_data'),
    # Race_Total_Top_Counties_Data
    path('race/total/top_counties/data', RaceTotalTopCountiesData.as_view(),
         name='race_total_top_counties_data'),
    # Race_State_Top_Countites_Data
    path('race/state/top_counties/data', RaceStateTopCountiesData.as_view(),
         name='race_state_top_counties_data'),

    # Race_Total_Top_State_Data_Two
    path('race/total/top_state2/data', RaceTotalTopStateDataTwo.as_view(),
         name='race_total_top_state_data2'),
    # Race_Total_Top_Counties_Data_Two
    path('race/total/top_counties2/data', RaceTotalTopCountiesDataTwo.as_view(),
         name='race_total_top_counties_data2'),
    # Race_State_Top_Countites_Data_Two
    path('race/state/top_counties2/data', RaceStateTopCountiesDataTwo.as_view(),
         name='race_state_top_counties_data'),


    # Income_Error/Estimate
    path('income/error_estimate/data', IncomeErrorEstimateData.as_view(),
         name='income_error_estimate_data'),
    # Income_State_Total_Data
    path('income/state/total/data', IncomeStateTotalData.as_view(),
         name='income_state_total/data'),
    # Income_Total_Top_State_Data
    path('income/total/top_state/data', IncomeTotalTopStateData.as_view(),
         name='income_total_top_state_data'),
    # Income_Total_Top_Counties_Data
    path('income/total/top_counties/data', IncomeTotalTopCountiesData.as_view(),
         name='income_total_top_counties_data'),
    # Income_State_Top_Countites_Data
    path('income/state/top_counties/data', IncomeStateTopCountiesData.as_view(),
         name='race_state_top_counties_data'),

]
