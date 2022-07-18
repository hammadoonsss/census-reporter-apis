from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_mobility.models import (MobilityEstimate,
                                        MobilityStateTotal)


#   -----------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Mobility  --------------------------------------


class MobilityTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                mob_id = request.data.get('Mobility_ID')
                # print('mob_id: ', mob_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'mobility'

                mob_state, error = TotalPercentage.top_state_data(
                    MobilityStateTotal, topic, mob_id, count, filter_type
                )
                # print('error: ', error)
                # print('mob_state: ', mob_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                mob_top_state_list = []

                if mob_state.exists():
                    for data in mob_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Mobility_Id'] = data.mobility_id
                        state_perc_data['Mobility_Total'] = data.mobility_total
                        state_perc_data['Percentage'] = data.percent

                        mob_top_state_list.append(state_perc_data)

                    return Response({'result': mob_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in MTSD': f'{e}'})


#   -----------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Mobility  -----------------------------------


class MobilityTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                mob_id = request.data.get('Mobility_ID')
                # print('mob_id: ', mob_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'mobility'

                mob_counties_data, error = TotalPercentage.top_counties_data(
                    MobilityEstimate, topic, mob_id, count, filter_type)

                # print('error: ', error)
                # print('mob_counties_data: ', mob_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                mob_top_counties_list = []

                if mob_counties_data.exists():

                    for data in mob_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Mobility_Id'] = data.mobility_id
                        county_perc_data['Mobility_Total'] = data.county.mobility_total
                        county_perc_data['Mobility_Estimate_Value'] = data.mobility_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        mob_top_counties_list.append(county_perc_data)

                    return Response({'result': mob_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in MTCD': f'{e}'})


#   ---------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Mobility  ----------------------------------


class MobilityStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                mob_id = request.data.get('Mobility_ID')
                # print('mob_id: ', mob_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)
                # print('state_id: ', state_id)

                topic = 'mobility'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    MobilityEstimate, topic, mob_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                mob_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Mobility_Id'] = data.mobility_id
                        sc_perc_data['Mobility_Total'] = data.county.mobility_total
                        sc_perc_data['Mobility_Estimate_Value'] = data.mobility_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        mob_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': mob_state_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in MSTCD': f'{e}'})
