
from django.http import JsonResponse
from django.db.models import Count, Min, Max, F, Q


from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import County, Race, RaceError, RaceEstimate, State

from realestate_app.paginations import CustomPagination

from realestate_app.serializers import (
    CountySerializer, RaceEstimateSerializer, RaceSerializer, StateSerializer)


# Main APIs - To Fetch Data.


class StateRaceEstimateData(APIView, CustomPagination):

    def post(self, request):
        try:
            if request.data:

                symbol = request.data.get("Symbol")
                print('symbol: ', symbol)
                state = request.data.get("State")
                print('state: ', state)

                state_data = State.objects.get(state_name=state)
                print('state_data:--- ', state_data)

                state_county = County.objects.filter(
                    state_id=state_data).values_list('county_id', flat=True)
                print('state_county:--- ', state_county)

                race_estimate = RaceEstimate.objects.filter(
                    county_id__in=state_county)
                print('race_estimate: ----', race_estimate)

                county_race_list = []

                for data in race_estimate:

                    race_dict = {}

                    race_dict['State_id'] = data.county.state.state_id
                    # race_dict['State_name'] = data.county.state.state_name

                    race_dict['County_id'] = data.county_id
                    # race_dict['County_name'] = data.county.county_name

                    race_dict['Race_id'] = data.race_id
                    race_dict['Race_name'] = data.race.race_name
                    race_dict['Race_Estimate_value'] = data.race_estimate_value

                    county_race_list.append(race_dict)

                # # Pagination -1
                # result = self.paginate_queryset(race_estimate, request)
                # race_serializer = RaceEstimateSerializer(result, many=True)
                # print('result: ', result)
                # return self.get_paginated_response(race_serializer.data)

                # Serializer-DB_data
                # race_serializer = RaceEstimateSerializer(race_estimate, many=True)
                # return Response(race_serializer.data)

                # Dictionary-county_race_list
                return Response({'result': county_race_list})

                # Pagination -2
                # result = self.paginate_queryset(county_race_list, request)
                # # race_serializer = RaceEstimateSerializer(result, many=True)
                # print('result: ', result)
                # return self.get_paginated_response(result)

            else:
                return Response({'Error': "In valid request!!"})
        except Exception as e:
            print("Error in RSD-GET:", e)
            return Response({"In Exception": e})


class RaceFilterData(APIView):

    def post(self, request):
        
        print('request.data: ', request.data)

        perc_data = RaceEstimate.objects.annotate(percentage=F(
            'race_estimate_value')*100/F('county__race_total')).filter(percentage__gt=70, race_id='B02001003')
        print('perc_data:====> ', perc_data)

        for data in perc_data:
            print("data===", data.county_id,)
            print("data.race_id+", data.race_id)
            print(' data.race_estimate_value: ',  data.race_estimate_value)
            print('data.county.race_total', data.county.race_total)
            print(' data.percentage: ',  data.percentage)
            print("--------------------")
            
        return Response("Race_filter_data")
