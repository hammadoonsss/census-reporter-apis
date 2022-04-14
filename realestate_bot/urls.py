"""realestate_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from realestate_app.views import(AllCountiesData, AllStatesData, AmericanCommunitySurveyData, TabulationData,
                                 RaceMultipleStateData, RaceStateData, RaceCodeData)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("tabulation/data/", TabulationData.as_view(),
         name='tabulation_data'),
    path("all_counties/data/", AllCountiesData.as_view(),
         name='all_counties_data'),
    path("all_states/data/", AllStatesData.as_view(),
         name='all_states_data'),
    path("american_community_survey/data/", AmericanCommunitySurveyData.as_view(),
         name='american_community_survey_data'),

    # Race
    path("race/state/data/", RaceStateData.as_view(),
         name='race_state_data'),

    path("race_multiple_state/data/", RaceMultipleStateData.as_view(),
         name='race_single_state_data'),

    path("race_code/data/", RaceCodeData.as_view(),
         name='race_code_data'),
]
