from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_sex_age.models import (SexAgeEstimate,
                                       SexAgeStateTotal)


#   --------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Sex_Age  ------------------------------------------


class SexAgeTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                sa_id = request.data.get('Sex_Age_ID')
                # print('sa_id: ', sa_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'sex_age'

                sa_state, error = TotalPercentage.top_state_data(
                    SexAgeStateTotal, topic, sa_id, count, filter_type
                )
                # print('error: ', error)
                # print('sa_state: ', sa_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                sa_top_state_list = []

                if sa_state.exists():
                    for data in sa_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Sex_Age_Id'] = data.sex_age_id
                        state_perc_data['Sex_Age_Total'] = data.sex_age_total
                        state_perc_data['Percentage'] = data.percent

                        sa_top_state_list.append(state_perc_data)

                    return Response({'result': sa_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in SATSD': f'{e}'})


#   --------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Sex_Age  ---------------------------------------


class SexAgeTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                sa_id = request.data.get('Sex_Age_ID')
                # print('sa_id: ', sa_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'sex_age'

                sa_counties_data, error = TotalPercentage.top_counties_data(
                    SexAgeEstimate, topic, sa_id, count, filter_type)

                # print('error: ', error)
                # print('sa_counties_data: ', sa_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                sa_top_counties_list = []

                if sa_counties_data.exists():

                    for data in sa_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Sex_Age_Id'] = data.sex_age_id
                        county_perc_data['Sex_Age_Total'] = data.county.sex_age_total
                        county_perc_data['Sex_Age_Estimate_Value'] = data.sex_age_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        sa_top_counties_list.append(county_perc_data)

                    return Response({'result': sa_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in SATCD': f'{e}'})


#   --------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Sex_Age  ----------------------------------


class SexAgeStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                sa_id = request.data.get('Sex_Age_ID')
                # print('sa_id: ', sa_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)

                topic = 'sex_age'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    SexAgeEstimate, topic, sa_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                sa_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Sex_Age_Id'] = data.sex_age_id
                        sc_perc_data['Sex_Age_Total'] = data.county.sex_age_total
                        sc_perc_data['Sex_Age_Estimate_Value'] = data.sex_age_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        sa_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': sa_state_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in SASTCD': f'{e}'})
