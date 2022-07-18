from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_education.models import (EducationEstimate,
                                         EducationStateTotal)


#   ----------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Education  ------------------------------------------


class EducationTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                edu_id = request.data.get('Education_ID')
                # print('edu_id: ', edu_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'education'

                edu_state, error = TotalPercentage.top_state_data(
                    EducationStateTotal, topic, edu_id, count, filter_type
                )
                # print('error: ', error)
                # print('edu_state: ', edu_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                edu_top_state_list = []

                if edu_state.exists():
                    for data in edu_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Education_Id'] = data.education_id
                        state_perc_data['Education_Total'] = data.education_total
                        state_perc_data['Percentage'] = data.percent

                        edu_top_state_list.append(state_perc_data)

                    return Response({'result': edu_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ETSD': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Education  ---------------------------------------


class EducationTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                edu_id = request.data.get('Education_ID')
                # print('edu_id: ', edu_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'education'

                edu_counties_data, error = TotalPercentage.top_counties_data(
                    EducationEstimate, topic, edu_id, count, filter_type)

                # print('error: ', error)
                # print('edu_counties_data: ', edu_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                edu_top_counties_list = []

                if edu_counties_data.exists():

                    for data in edu_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Education_Id'] = data.education_id
                        county_perc_data['Education_Total'] = data.county.education_total
                        county_perc_data['Education_Estimate_Value'] = data.education_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        edu_top_counties_list.append(county_perc_data)

                    return Response({'result': edu_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ETCD': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Education  ----------------------------------


class EducationStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                edu_id = request.data.get('Education_ID')
                # print('edu_id: ', edu_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)

                topic = 'education'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    EducationEstimate, topic, edu_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                edu_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Education_Id'] = data.education_id
                        sc_perc_data['Education_Total'] = data.county.education_total
                        sc_perc_data['Education_Estimate_Value'] = data.education_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        edu_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': edu_state_top_counties_list})

                else:
                    return Response({'error': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ESTCD': f'{e}'})
