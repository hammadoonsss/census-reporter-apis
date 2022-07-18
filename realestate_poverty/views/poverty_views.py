from django.db.models import F

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_poverty.models import *


#   --------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of Poverty  ------------------------------------------


class PovertyTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                pov_id = request.data.get('Poverty_ID')
                # print('poverty_id: ', pov_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                poverty_state_top = PovertyStateTotal.objects.exclude(
                    poverty_id='B17001001').annotate(
                        percent=F('poverty_total')*100/F('state_total')
                ).filter(poverty_id=pov_id)

                # print('poverty_state_top: ', poverty_state_top)

                if filter_type == "Top":
                    poverty_state_top = poverty_state_top.order_by(
                        '-percent')[:count]
                    print('poverty_state_top: ', poverty_state_top)

                elif filter_type == "Bottom":
                    poverty_state_top = poverty_state_top.order_by(
                        'percent')[:count]
                    print('poverty_state_top: ', poverty_state_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_top_list = []

                if poverty_state_top.exists():

                    for data in poverty_state_top:
                        pov_st_data = {}

                        pov_st_data['State_Id'] = data.state_id
                        pov_st_data['State_Name'] = data.state.state_name
                        pov_st_data['State_Total'] = data.state_total
                        pov_st_data['Poverty_Id'] = data.poverty_id
                        pov_st_data['Poverty_Total'] = data.poverty_total
                        pov_st_data['Percentage'] = data.percent

                        poverty_top_list.append(pov_st_data)

                    return Response({"result": poverty_top_list})

                else:
                    return Response({"error": 'No Data Available'})

            else:
                return Response({'error': 'Invalid Request'})

        except Exception as e:
            print("in except")
            return Response({"error in PTSD": f'{e}'})


#   -------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of Poverty ---------------------------------------


class PovertyTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                poverty_id = request.data.get('Poverty_ID')
                # print('poverty_id: ', poverty_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                poverty_county_top = PovertyEstimate.objects.exclude(
                    poverty_id='B17001001').annotate(
                        percent=F('poverty_estimate_value') *
                        100/F('county__poverty_total')
                ).filter(poverty_id=poverty_id)

                # print('poverty_county_top:-------->>> ', poverty_county_top)

                if filter_type == "Top":
                    poverty_county_top = poverty_county_top.order_by(
                        '-percent')[:count]
                    print('poverty_county_top:---TOP ', poverty_county_top)

                elif filter_type == "Bottom":
                    poverty_county_top = poverty_county_top.order_by('percent')[
                        :count]
                    print('poverty_county_top:---BOTTOM ', poverty_county_top)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_top_list = []

                if poverty_county_top.exists():

                    for data in poverty_county_top:
                        pov_coun_data = {}

                        pov_coun_data['State_Id'] = data.county.state.state_id
                        pov_coun_data['State_Name'] = data.county.state.state_name
                        pov_coun_data['County_Id'] = data.county_id
                        pov_coun_data['County_Name'] = data.county.county_name
                        pov_coun_data['Poverty_Id'] = data.poverty_id
                        pov_coun_data['Poverty_Total'] = data.county.poverty_total
                        pov_coun_data['Poverty_Estimate_Value'] = data.poverty_estimate_value
                        pov_coun_data['Percentage'] = data.percent

                        poverty_top_list.append(pov_coun_data)

                    return Response({"result": poverty_top_list})
                else:
                    return Response({"error": 'No Data Available'})
            else:
                return Response({"error": 'Invalid Request'})

        except Exception as e:
            return Response({"error in PTCD": f'{e}'})


#   --------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of Sex_Age  ----------------------------------


class PovertyStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                poverty_id = request.data.get('Poverty_ID')
                # print('poverty_id: ', poverty_id)
                count = request.data.get('Count')
                # print('county: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)
                state = request.data.get('State')
                # print('state: ', state)

                state_id = State.objects.get(state_name=state)
                # print('state_id: ', state_id)

                poverty_top_state_county = PovertyEstimate.objects.exclude(
                    poverty_id='B17001001').annotate(
                        percent=F('poverty_estimate_value') *
                        100/F('county__poverty_total')
                ).filter(
                        county__state_id=state_id,
                        poverty_id=poverty_id
                )

                # print('poverty_top_state_county: ', poverty_top_state_county)

                if filter_type == "Top":
                    poverty_top_state_county = poverty_top_state_county.order_by(
                        '-percent')[:count]
                    print('poverty_top_state_county:----TOP',
                          poverty_top_state_county)

                elif filter_type == "Bottom":
                    poverty_top_state_county = poverty_top_state_county.order_by(
                        'percent')[:count]
                    print('poverty_top_state_county:---Bottom',
                          poverty_top_state_county)

                else:
                    return Response({'error': 'Invalid Filter Type'})

                poverty_top_state_county_list = []

                if poverty_top_state_county.exists():

                    for data in poverty_top_state_county:
                        pov_st_coun_data = {}

                        pov_st_coun_data['State_Id'] = data.county.state.state_id
                        pov_st_coun_data['State_Name'] = data.county.state.state_name
                        pov_st_coun_data['County_Id'] = data.county_id
                        pov_st_coun_data['Coutny_Name'] = data.county.county_name
                        pov_st_coun_data['Poverty_Id'] = data.poverty_id
                        pov_st_coun_data['Poverty_Total'] = data.county.poverty_total
                        pov_st_coun_data['Poverty_Estimate_Value'] = data.poverty_estimate_value
                        pov_st_coun_data['Percentage'] = data.percent

                        poverty_top_state_county_list.append(pov_st_coun_data)

                    return Response({"result": poverty_top_state_county_list})

                else:
                    return Response({"error": 'No Data Available'})

            else:
                return Response({"error": "Invalid Request"})

        except Exception as e:
            return Response({'error in PSTCD': f'{e}'})
