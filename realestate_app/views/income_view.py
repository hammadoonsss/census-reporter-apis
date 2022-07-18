from django.db.models import Count, Min, Max, F, Q, Sum

from rest_framework.views import APIView
from rest_framework.response import Response


from realestate_app.models import (State, County, Income, IncomeError, IncomeEstimate,
                                   IncomeStateTotal)

from realestate_app.services import TotalPercentage


#   ------------------------------------------------------------------------------------
#   ------------ Populate Income_State_Total Data in the Respective Tables -------------


class IncomeStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state = State.objects.all()

            for data in state:
                income_id = Income.objects.all()

                for id in income_id:
                    # print("income_id", id)
                    # print("State_id", data)

                    income_total = IncomeEstimate.objects.filter(
                        county__state_id=data, income_id=id
                    ).aggregate(sum_income=Sum('income_estimate_value'))

                    # print("income_total", income_total)

                    state_total = County.objects.filter(
                        state_id=data).aggregate(sum_state=Sum('income_total'))

                    # print("state_total", state_total)

                    count = count + 1
                    print('count:------------------- ', count)

                    if income_total['sum_income'] and state_total['sum_state']:
                        print("In If --------->")
                        print('income_total: ', income_total['sum_income'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            ist_data = IncomeStateTotal.objects.get(
                                state=data, income=id)
                            print('IST-ist_db_data: try get: \n', ist_data)

                        except:
                            ist_db_data = IncomeStateTotal.objects.create(
                                state=data,
                                income=id,
                                state_total=state_total['sum_state'],
                                income_total=income_total['sum_income']
                            )
                            print('IST-ist_db_data: except create \n', ist_db_data)

                    else:
                        print("In ELSE::_____")
                        print('income_total: ', income_total['sum_income'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'IncomeStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in ISTD': f'{e}'})


#   ------------------------------------------------------------------------------
#   --------------------- Get Top_State Data of Income  --------------------------


class IncomeTotalTopStateData(APIView):

    def post(self, request):

        try:
            if request.data:
                income_id = request.data.get('Income_ID')
                # print('income_id: ', income_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)
                topic = "income"

                income_state, error = TotalPercentage.top_state_data(
                    IncomeStateTotal, topic, income_id, count, filter_type)

                # print('errorin Post method : ', error)
                # print('income_state: ', income_state)

                if error is not None:
                    print("Inside error----")
                    return Response({'error': error})

                income_top_state_list = []

                if income_state.exists():
                    for data in income_state:

                        state_perc_data = {}

                        state_perc_data['State_id'] = data.state_id
                        state_perc_data['State_name'] = data.state.state_name
                        state_perc_data['State_Total'] = data.state_total
                        state_perc_data['Income_id'] = data.income_id
                        state_perc_data['Income_Total'] = data.income_total
                        state_perc_data['Percentage'] = data.percent

                        income_top_state_list.append(state_perc_data)

                    return Response({'result': income_top_state_list})

                else:
                    return Response({'error': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ITTSD': f'{e}'})


#   ---------------------------------------------------------------------------------------
#   ---------------------- Get Top_Counties Data of Income --------------------------------


class IncomeTotalTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                income_id = request.data.get('Income_ID')
                # print('income_id: ', income_id)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)
                topic = "income"

                income_county, error = TotalPercentage.top_counties_data(
                    IncomeEstimate, topic, income_id, count, filter_type)

                # print('error:==> ', error)
                # print('income_county: ', income_county)

                if error is not None:
                    print("Inside error---->")
                    return Response({'error': error})

                income_top_county_list = []

                if income_county.exists():
                    for data in income_county:

                        county_perc_data = {}
                        county_perc_data['State_Id'] = data.county.state.state_id
                        county_perc_data['State_Name'] = data.county.state.state_name
                        county_perc_data['County_Id'] = data.county_id
                        county_perc_data['County_Name'] = data.county.county_name
                        county_perc_data['Income_Id'] = data.income_id
                        county_perc_data['Income_Total'] = data.county.income_total
                        county_perc_data['Income_Estimate_Value'] = data.income_estimate_value
                        county_perc_data['Percentage'] = data.percent

                        income_top_county_list.append(county_perc_data)

                    return Response({'result': income_top_county_list})
                else:
                    return Response({'error': "No Data Available"})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ITTCD:': f'{e}'})


#   ----------------------------------------------------------------------------
#   ---------------- Get State_Top_Counties Data of Income ---------------------


class IncomeStateTopCountiesData(APIView):

    def post(self, request):

        try:
            if request.data:
                income_id = request.data.get('Income_ID')
                # print('income_id: ', income_id)
                state = request.data.get('State')
                # print('state: ', state)
                count = request.data.get('Count')
                # print('count: ', count)
                filter_type = request.data.get('Type')
                # print('filter_type: ', filter_type)

                state_id = State.objects.get(state_name=state)
                # print('state_id: ', state_id)

                topic = "income"

                scounty_data, error = TotalPercentage.state_top_counties_data(
                    IncomeEstimate, topic, income_id, state_id, count, filter_type)

                # print('error: ', error)
                # print('scounty_data: ', scounty_data)

                if error is not None:
                    print("Inside error---->")
                    return Response({'error': error})

                income_state_top_counties_list = []

                if scounty_data.exists():
                    for data in scounty_data:

                        sc_perc_data = {}

                        sc_perc_data['State_Id'] = data.county.state.state_id
                        sc_perc_data['State_Name'] = data.county.state.state_name
                        sc_perc_data['County_Id'] = data.county_id
                        sc_perc_data['County_Name'] = data.county.county_name
                        sc_perc_data['Income_Id'] = data.income_id
                        sc_perc_data['Income_Total'] = data.county.income_total
                        sc_perc_data['Income_Estimate_Value'] = data.income_estimate_value
                        sc_perc_data['Percentage'] = data.percent

                        income_state_top_counties_list.append(sc_perc_data)

                    return Response({'result': income_state_top_counties_list})

                else:
                    return Response({'error': 'No Data Available!'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in ISTCD: ': f'{e}'})
