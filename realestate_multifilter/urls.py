from django.urls import path

#  Multi-Filter View (Static)
from realestate_multifilter.views.views import(
    TopicTopState, TopicTopCounty, TopicTopStateCounty
)

# Multi-Filter Topic View (Static)
from .views.static_state_multifilter_views import (
    TopicStaticState
)
from .views.static_county_multifilter_views import (
     TopicStaticCounty
)
from .views.static_state_county_multifilter_views import (
    TopicStaticStateCounty
)

# Multi-Filter View (Second)
from .views.multi_filter_state_views import (
    StateMultiFilter,
)
from .views.multi_filter_counties_views import (
    CountiesMultiFilter
)
from .views.multi_filter_state_counties_views import (
    StateCountiesMultiFilter
)


urlpatterns = [

    # Multi-Filter Code Data (Static)
    path('top/state/data', TopicTopState.as_view(),
         name='topic_top_state_data'),
    path('top/county/data', TopicTopCounty.as_view(),
         name='topic_top_county_data'),
    path('top/state/county/data', TopicTopStateCounty.as_view(),
         name='topic_top_state_county_data'),

    # Multi-Filter Topic Code (Static)
    # TopicStatic State
    path('static/state/data', TopicStaticState.as_view(),
         name='topic_static_state'),
    # TopicStaticStateCounty
    path('static/state/county/data', TopicStaticStateCounty.as_view(),
         name='topic_static_state_county'),
    # TopicStatic County
    path('static/county/data', TopicStaticCounty.as_view(),
         name='topic_static_county'),

    # Multi-Filter Code Data (Second)
    # States
    path('multi_filter/state/data', StateMultiFilter.as_view(),
         name='topic_multi_filter_state_data'),
    # Countites
    path('multi_filter/counties/data', CountiesMultiFilter.as_view(),
         name='topic_multi_filter_counties_data'),
    # State/Countites
    path('multi_filter/state/counties/data', StateCountiesMultiFilter.as_view(),
         name='topic_multi_filter_state_counties_data'),
]
