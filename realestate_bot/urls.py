# Django Related Imports
from django.contrib import admin
from django.urls import path

# Census Views Import
from realestate_app.views.census_views import(AllCountiesData, AllStatesData, AmericanCommunitySurveyData,
                                              TabulationData, SingleTopicStateData,)

# Database Views Import
from realestate_app.views.views import(IncomeCodeData, RaceStateData, RaceCodeData, RaceErrorEstimateData,
                                       StateCountyDetailData, TopicDetails, UpdateFTPFile)

# Race Views
from realestate_app.views.race_views import (StateRaceEstimateData,
                                             RaceFilterData)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Census Reporter
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

    # TopicDetails
    path('topic/details/', TopicDetails.as_view(), name='topic_details'),
    # UpdateFTPFile
    path('update/ftp/', UpdateFTPFile.as_view(), name='update_ftp_file'),

    # Race
    path("race/state/data/", RaceStateData.as_view(),
         name='race_state_data'),
    # Race Code
    path("race_code/data/", RaceCodeData.as_view(),
         name='race_code_data'),
    # State/County
    path("state/county_detail/data/", StateCountyDetailData.as_view(),
         name='state_county_detail_data'),
    # Race Error/Estimate
    path("race/error_estimate/data/", RaceErrorEstimateData.as_view(),
         name='race_error_estimate_data'),
     
     #Income Code
     path("income_code/data/", IncomeCodeData.as_view(),
         name='income_code_data'),

    # State Race Estimate Data
    path("state/race_estimate/data", StateRaceEstimateData.as_view(),
         name='state_race_estimate_data'),
    # Race Filter Data
    path('race/filter/data/', RaceFilterData.as_view(), name='race_filter_data'),


]
