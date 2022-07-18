from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_tenure.models import (TenureEstimate,
                                    TenureStateTotal)


#   ---------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Tenure  --------------------------------------


class TenureTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                te_id = request.data.get('Tenure_ID')
                print('te_id: ', te_id)
                count = request.data.get('Count')
                print('count: ', count)
                filter_type = request.data.get('Type')
                print('filter_type: ', filter_type)

                topic = 'tenure'

                te_state, error = TotalPercentage.top_state_data(
                    TenureStateTotal, topic, te_id, count, filter_type
                )
                # print('error: ', error)
                # print('te_state: ', te_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                te_top_state_list = []

                if te_state.exists():
                    for data in te_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Tenure_Id'] = data.tenure_id
                        state_perc_data['Tenure_Total'] = data.tenure_total
                        state_perc_data['Percentage'] = data.percent

                        te_top_state_list.append(state_perc_data)

                    return Response({'result': te_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in TeTSD': f'{e}'})


#   ---------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Tenure  -----------------------------------


class TenureTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                te_id = request.data.get('Tenure_ID')
                print('te_id: ', te_id)
                count = request.data.get('Count')
                print('count: ', count)
                filter_type = request.data.get('Type')
                print('filter_type: ', filter_type)

                topic = 'tenure'

                te_counties_data, error = TotalPercentage.top_counties_data(
                    TenureEstimate, topic, te_id, count, filter_type)

                # print('error: ', error)
                # print('te_counties_data: ', te_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                te_top_counties_list = []

                if te_counties_data.exists():

                    for data in te_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Tenure_Id'] = data.tenure_id
                        county_perc_data['Tenure_Total'] = data.county.tenure_total
                        county_perc_data['Tenure_Estimate_Value'] = data.tenure_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        te_top_counties_list.append(county_perc_data)

                    return Response({'result': te_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in TeTCD': f'{e}'})


#   -------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Tenure  ----------------------------------


class TenureStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                te_id = request.data.get('Tenure_ID')
                print('te_id: ', te_id)
                state = request.data.get('State')
                print('state: ', state)
                count = request.data.get('Count')
                print('count: ', count)
                filter_type = request.data.get('Type')
                print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)
                print('state_id: ', state_id)

                topic = 'tenure'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    TenureEstimate, topic, te_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                te_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Tenure_Id'] = data.tenure_id
                        sc_perc_data['Tenure_Total'] = data.county.tenure_total
                        sc_perc_data['Tenure_Estimate_Value'] = data.tenure_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        te_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': te_state_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in TeSTCD': f'{e}'})
