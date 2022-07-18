from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.services import TotalPercentage

from realestate_app.models import (State,)

from realestate_house_price.models import (
    HousePriceEstimate,
    HousePriceStateTotal
)


#   --------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_State Data of House_Price  --------------------------------------


class HousePriceTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                hp_id = request.data.get('House_Price_ID')
                # print('hp_id: ', hp_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'house_price'

                hp_state, error = TotalPercentage.top_state_data(
                    HousePriceStateTotal, topic, hp_id, count, filter_type
                )
                # print('error: ', error)
                # print('hp_state: ', hp_state)

                if error is not None:
                    print("Inside Error")
                    return Response({'error': f'{error}'})

                hp_top_state_list = []

                if hp_state.exists():
                    for data in hp_state:

                        state_perc_data = {}

                        state_perc_data['State_Id'] = data.state_id
                        state_perc_data['State_Name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['House_Price_Id'] = data.house_price_id
                        state_perc_data['House_Price_Total'] = data.house_price_total
                        state_perc_data['Percentage'] = data.percent

                        hp_top_state_list.append(state_perc_data)

                    return Response({'result': hp_top_state_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in HPTSD': f'{e}'})


#   --------------------------------------------------------------------------------------------------------
#   ------------------------------ Get Top_Counties Data of House_Price  -----------------------------------


class HousePriceTopCountitesData(APIView):

    def post(self, request):

        try:
            if request.data:
                hp_id = request.data.get('House_Price_ID')
                # print('hp_id: ', hp_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                topic = 'house_price'

                hp_counties_data, error = TotalPercentage.top_counties_data(
                    HousePriceEstimate, topic, hp_id, count, filter_type)

                # print('error: ', error)
                # print('hp_counties_data: ', hp_counties_data)

                if error is not None:
                    print("Inside error")
                    return Response({'error': f'{error}'})

                hp_top_counties_list = []

                if hp_counties_data.exists():

                    for data in hp_counties_data:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['House_Price_Id'] = data.house_price_id
                        county_perc_data['House_Price_Total'] = data.county.house_price_total
                        county_perc_data['House_Price_Estimate_Value'] = data.house_price_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        hp_top_counties_list.append(county_perc_data)

                    return Response({'result': hp_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in HPTCD': f'{e}'})


#   ------------------------------------------------------------------------------------------------------------
#   ----------------------------- Get State_Top_Counties Data of House_Price  ----------------------------------


class HousePriceStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                hp_id = request.data.get('House_Price_ID')
                # print('hp_id: ', hp_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)

                topic = 'house_price'

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    HousePriceEstimate, topic, hp_id, state_id, count, filter_type
                )

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside Error----")
                    return Response({'error': f'{error}'})

                hp_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['House_Price_Id'] = data.house_price_id
                        sc_perc_data['House_Price_Total'] = data.county.house_price_total
                        sc_perc_data['House_Price_Estimate_Value'] = data.house_price_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        hp_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': hp_state_top_counties_list})

                else:
                    return Response({'error': 'NO Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in HPSTCD': f'{e}'})
