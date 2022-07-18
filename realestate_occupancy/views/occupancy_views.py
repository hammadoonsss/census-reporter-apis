from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_occupancy.models import (OccupancyEstimate,
                                         OccupancyStateTotal)


#   ------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Occupancy  --------------------------------------


class OccupancyTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                occ_id = request.data.get('Occupancy_ID')
                # print('occ_id: ', occ_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'occupancy'

                occ_state, error = TotalPercentage.top_state_data(
                    OccupancyStateTotal, topic, occ_id, count, filter_type
                )
                # print('error: ', error)
                # print('occ_state: ', occ_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                occ_top_state_list = []

                if occ_state.exists():
                    for data in occ_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Occupancy_Id'] = data.occupancy_id
                        state_perc_data['Occupancy_Total'] = data.occupancy_total
                        state_perc_data['Percentage'] = data.percent

                        occ_top_state_list.append(state_perc_data)

                    return Response({'result': occ_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in OTSD': f'{e}'})


#   ------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Occupancy  -----------------------------------


class OccupancyTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                occ_id = request.data.get('Occupancy_ID')
                # print('occ_id: ', occ_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'occupancy'

                occ_counties_data, error = TotalPercentage.top_counties_data(
                    OccupancyEstimate, topic, occ_id, count, filter_type)

                # print('error: ', error)
                # print('occ_counties_data: ', occ_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                occ_top_counties_list = []

                if occ_counties_data.exists():

                    for data in occ_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Occupancy_Id'] = data.occupancy_id
                        county_perc_data['Occupancy_Total'] = data.county.occupancy_total
                        county_perc_data['Occupancy_Estimate_Value'] = data.occupancy_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        occ_top_counties_list.append(county_perc_data)

                    return Response({'result': occ_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in OTCD': f'{e}'})


#   ------------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Occupancy  ----------------------------------


class OccupancyStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                occ_id = request.data.get('Occupancy_ID')
                # print('occ_id: ', occ_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)

                topic = 'occupancy'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    OccupancyEstimate, topic, occ_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                occ_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Occupancy_Id'] = data.occupancy_id
                        sc_perc_data['Occupancy_Total'] = data.county.occupancy_total
                        sc_perc_data['Occupancy_Estimate_Value'] = data.occupancy_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        occ_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': occ_state_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in OSTCD': f'{e}'})
