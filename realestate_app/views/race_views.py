
from django.http import JsonResponse
from django.db.models import Count, Min, Max, F, Q, Sum


from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (State, County, Race, RaceError, RaceEstimate,
                                   RaceStateTotal, )

from realestate_app.paginations import CustomPagination

from realestate_app.serializers import (
    CountySerializer, RaceEstimateSerializer, RaceSerializer, StateSerializer)

from realestate_app.services import TotalPercentage


# Main APIs - To Fetch Data.


class RaceEstimateStateData(APIView, CustomPagination):

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
                # return Response({'result': county_race_list})

                # Pagination -2
                result = self.paginate_queryset(county_race_list, request)
                # # race_serializer = RaceEstimateSerializer(result, many=True)
                # print('result: ', result)
                return self.get_paginated_response(result)

            else:
                return Response({'error': "In valid request!!"})

        except Exception as e:
            print("Error in RESD:", e)
            return Response({"In Error in RESD": f'{e}'})


class RaceTotalTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                race_county = RaceEstimate.objects.exclude(race_id="B02001001").annotate(
                    percentage=F('race_estimate_value') *
                    100/F('county__race_total')
                ).filter(race_id=race_id)

                if filter_type == 'Top':
                    race_county = race_county.order_by('-percentage')[:count]
                    print('race_county_top: ', race_county)

                elif filter_type == 'Bottom':
                    race_county = race_county.order_by('percentage')[:count]
                    print('race_county_bottom: ', race_county)

                else:
                    return Response({'msg': 'Invalid Filter Type'})

                print('perc_data:====> ', type(race_county))

                perc_list = []

                if race_county.exists():
                    for data in race_county:

                        perc_data = {}
                        perc_data['State_Id'] = data.county.state.state_id
                        perc_data['State_Name'] = data.county.state.state_name
                        perc_data['County_Id'] = data.county_id
                        perc_data['County_Name'] = data.county.county_name
                        perc_data['Race_Id'] = data.race_id
                        perc_data['Race_Total'] = data.county.race_total
                        perc_data['Race_Estimate_Value'] = data.race_estimate_value
                        perc_data['Percentage'] = data.percentage

                        perc_list.append(perc_data)

                    return Response({'result': perc_list})
                else:
                    return Response({'result': "No Data Available"})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RTTCD-POST: ", e)
            return Response({'Error in RTTCD-POST': f'{e}'})


class RaceStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state = State.objects.all()

            for data in state:
                race_id = Race.objects.all()

                for id in race_id:
                    print("race_id", id)
                    print("State_id", data)

                    race_total = RaceEstimate.objects.filter(
                        county__state_id=data, race_id=id
                    ).aggregate(sum_race=Sum('race_estimate_value'))

                    print("race_total", race_total)

                    state_total = County.objects.filter(
                        state_id=data).aggregate(sum_state=Sum('race_total'))

                    print("state_total", state_total)

                    count = count + 1
                    print("count", count)
                    print("---------------------------------------------\n")

                    try:
                        rst_data = RaceStateTotal.objects.get(
                            state=data, race=id)
                        print('RST-rst_db_data: try get: \n', rst_data)
                    except:
                        rst_db_data = RaceStateTotal.objects.create(
                            state=data,
                            race=id,
                            state_total=state_total['sum_state'],
                            race_total=race_total['sum_race']
                        )
                        print('RST-rst_db_data: except create \n', rst_db_data)

            return Response({'msg': 'Populated DB'})

        except Exception as e:
            print("Error in RSTD: ", e)
            return Response({'Error in RSTD': f'{e}'})


class RaceTotalTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                race_state = RaceStateTotal.objects.exclude(race="B02001001").annotate(
                    percent=(F('race_total')*100)/F('state_total')
                ).filter(race_id=race_id)

                if filter_type == "Top":
                    race_state = race_state.order_by('-percent')[:count]
                    # print('race_state_top: ', race_state)

                elif filter_type == "Bottom":
                    race_state = race_state.order_by('percent')[:count]
                    # print('race_state_bottom: ', race_state)

                else:
                    return Response({'msg': 'Invalid Filter Type'})

                race_top_state_list = []

                if race_state.exists():
                    for data in race_state:

                        state_perc_data = {}

                        state_perc_data['State_id'] = data.state_id
                        state_perc_data['State_name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Race_id'] = data.race_id
                        state_perc_data['Race_Total'] = data.race_total
                        state_perc_data['Percentage'] = data.percent

                        race_top_state_list.append(state_perc_data)

                    return Response({'result': race_top_state_list})

                else:
                    return Response({'result': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RTTSD-POST: ", e)
            return Response({'Error in RTTSD-POST': f'{e}'})


class RaceStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)
                print('state_id: ', state_id)

                county_data = RaceEstimate.objects.exclude(race_id='B02001001').annotate(
                    percent=F('race_estimate_value') *
                    100/F('county__race_total')
                ).filter(race_id=race_id, county__state_id=state_id)

                print('county_data: ', vars(county_data[0]))

                # return Response({'Check Terminal'})
                if filter_type == "Top":
                    county_data = county_data.order_by('-percent')[:count]
                    # print('county_data_top: ', county_data)

                elif filter_type == "Bottom":
                    county_data = county_data.order_by('percent')[:count]
                    # print('county_data_bottom: ', county_data)

                else:
                    return Response({'msg': 'Invalid Filter Type'})

                race_state_top_counties_list = []

                if county_data.exists():
                    for data in county_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Race_Id'] = data.race_id
                        sc_perc_data['Race_Total'] = data.county.race_total
                        sc_perc_data['Race_Estimate_Value'] = data.race_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        race_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': race_state_top_counties_list})

                else:
                    return Response({'result': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RSTCD-POST: ", e)
            return Response({'Error in RSTCD-POST': f'{e}'})


# ---------------------------------------------------------------------------------------------------
# -----------------------------Race Percentage API -Dyanamic- ---------------------------------------


class RaceTotalTopStateDataTwo(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)
                topic = "race"

                race_state = TotalPercentage.top_state_data(
                    RaceStateTotal, topic, race_id, count, filter_type)
                print('race_state: ', race_state)

                race_top_state_list = []

                if race_state.exists():
                    for data in race_state:

                        state_perc_data = {}

                        state_perc_data['State_id'] = data.state_id
                        state_perc_data['State_name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Race_id'] = data.race_id
                        state_perc_data['Race_Total'] = data.race_total
                        state_perc_data['Percentage'] = data.percent

                        race_top_state_list.append(state_perc_data)

                    return Response({'result': race_top_state_list})

                else:
                    return Response({'result': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RTTSD-POST: ", e)
            return Response({'Error in RTTSD-POST': f'{e}'})


class RaceTotalTopCountiesDataTwo(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)
                topic = "race"

                race_county = TotalPercentage.top_counties_data(
                    RaceEstimate, topic, race_id, count, filter_type)

                print('perc_data:====> ', type(race_county))

                perc_list = []

                if race_county.exists():
                    for data in race_county:

                        perc_data = {}
                        perc_data['State_Id'] = data.county.state.state_id
                        perc_data['State_Name'] = data.county.state.state_name
                        perc_data['County_Id'] = data.county_id
                        perc_data['County_Name'] = data.county.county_name
                        perc_data['Race_Id'] = data.race_id
                        perc_data['Race_Total'] = data.county.race_total
                        perc_data['Race_Estimate_Value'] = data.race_estimate_value
                        perc_data['Percentage'] = data.percent

                        perc_list.append(perc_data)

                    return Response({'result': perc_list})
                else:
                    return Response({'result': "No Data Available"})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RTTCD-POST: ", e)
            return Response({'Error in RTTCD-POST': f'{e}'})


class RaceStateTopCountiesDataTwo(APIView):

    def post(self, request):

        try:
            if request.data:
                race_id = request.data.get('Race_ID')
                # print('race_id: ', race_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state = State.objects.get(state_name=state)
                # print('state_id: ', state_id)

                topic = "race"

                county_data = TotalPercentage.state_top_counties_data(
                    RaceEstimate, topic, race_id, state, count, filter_type)

                race_state_top_counties_list = []

                if county_data.exists():
                    for data in county_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Race_Id'] = data.race_id
                        sc_perc_data['Race_Total'] = data.county.race_total
                        sc_perc_data['Race_Estimate_Value'] = data.race_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        race_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': race_state_top_counties_list})

                else:
                    return Response({'result': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            print("Error in RSTCD-POST: ", e)
            return Response({'Error in RSTCD-POST': f'{e}'})
