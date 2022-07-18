from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State)

from realestate_poverty.models import (
    Poverty,
    PovertyEstimate,
    PovertyError,
    PovertyStateTotal
)


# -----------------------------------------------------------------------------------------------
# --------------------- Populate Poverty Code Data in the Poverty Table -------------------------


class PovertyCodeData(APIView):

    def post(self, request):
        try:
            if request.data:

                file_name = request.data.get('File_Name')
                # print('file name ------>>>>', file_name)
                data_dict = json_file_read(file_name)

                poverty_code = data_dict['tables'].get('B17001').get('columns')

                for data in poverty_code:

                    sub_poverty_id = data
                    sub_poverty_name = poverty_code.get(
                        sub_poverty_id).get("name")

                    # print("Sub_poverty_id", sub_poverty_id)
                    # print("Sub_poverty_name", sub_poverty_name)

                    if (
                        sub_poverty_id == 'B17001001'
                        or sub_poverty_id == 'B17001002'
                        or sub_poverty_id == 'B17001031'
                    ):
                        print("Inside Poverty---------------/>", sub_poverty_id)

                        try:
                            poverty_db = Poverty.objects.get(
                                poverty_id=sub_poverty_id)
                            print('poverty_db in TRY---->: ', poverty_db)

                        except:
                            povertydb_data = Poverty.objects.create(
                                poverty_id=sub_poverty_id,
                                poverty_name=sub_poverty_name)

                            print('povertydb_data in EXCEPT===<: ',
                                  povertydb_data)
                    else:
                        print("In else")
                        pass

                return Response({'msg': 'Poverty DB Populated.'})

            else:
                return Response({'error': "Invalid Request."})

        except Exception as e:
            return Response({'error in PCD': f'{e}'})


#   ---------------------------------------------------------------------------------------------------------
#   ------------------- Populate Poverty Error/Estimate Data in their Respective Tables ---------------------


class PovertyEstimateErrorData(APIView):

    def post(self, request):

        try:
            if request.data:

                file_name = request.data.get("File_Name")
                data_dict = json_file_read(file_name)
                # print('data_dict---->: ', type(data_dict))

                data_value = data_dict['data']
                # print('data_value:----> ', data_value)

                county_data = County.objects.all()

                for county in county_data:

                    if county.county_id in data_value:
                        print('county.county_id: ', county.county_id)

                        poverty_value = data_value.get(
                            county.county_id).get('B17001')

                        poverty_code = Poverty.objects.all()

                        # For poverty_total in County Table
                        poverty_total = poverty_value.get(
                            'estimate').get('B17001001')

                        if poverty_total:
                            print("In pov_Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.poverty_total = poverty_total
                            county_obj.save()

                        else:
                            print("__NO pov_total___")

                        for code in poverty_code:
                            print('poverty: ', code.poverty_id)

                            # For Poverty Estimate Data
                            poverty_estimate_data = poverty_value.get(
                                'estimate').get(code.poverty_id)
                            # print('poverty_data:---> ', poverty_estimate_data)

                            if poverty_estimate_data:
                                print('In IF :: poverty_estimate_data: ',
                                      poverty_estimate_data)

                                try:
                                    poverty_est_db = PovertyEstimate.objects.get(
                                        poverty_id=code.poverty_id,
                                        county_id=county.county_id
                                    )
                                    print('poverty_est_db IN TRY --->:',
                                          poverty_est_db)

                                except:
                                    povertydb_data = PovertyEstimate.objects.create(
                                        poverty_estimate_value=poverty_estimate_data,
                                        poverty_id=code.poverty_id,
                                        county_id=county.county_id
                                    )
                                    print('povertydb_data In EXCEPT: ====< ',
                                          povertydb_data)

                            else:
                                print('In else_povest :: No Value',
                                      poverty_estimate_data)
                                pass

                            # For Poverty Error Data
                            poverty_error_data = poverty_value.get(
                                'error').get(code.poverty_id)
                            # print('poverty_error_data:===< ',
                            #       poverty_error_data)

                            if poverty_error_data:
                                print('In IF :: poverty_error_data: ',
                                      poverty_error_data)

                                try:
                                    poverty_err_db = PovertyError.objects.get(
                                        poverty_id=code.poverty_id,
                                        county_id=county.county_id
                                    )
                                    print('poverty_err_db: In TRY -->',
                                          poverty_err_db)
                                except:
                                    povertydb_data = PovertyError.objects.create(
                                        poverty_error_value=poverty_error_data,
                                        poverty_id=code.poverty_id,
                                        county_id=county.county_id
                                    )
                                    print('povertydb_data: In EXCEPT ==<',
                                          povertydb_data)
                            else:
                                print('In else-poverr :: No Value',
                                      poverty_error_data)
                                pass

                    else:
                        print('In Else PEED')
                        pass

                return Response({'msg': 'PovertyEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in PEED': f'{e}'})


#   -------------------------------------------------------------------------------------------------------
#   ------------------- Populate Poverty_State_Total Data in the Respective Table -------------------------


class PovertyStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for state_id in state_data:
                poverty_data = Poverty.objects.all()

                for poverty_id in poverty_data:
                    # print('state_id: ', state_id)
                    # print("poverty_id:", poverty_id)

                    poverty_total = PovertyEstimate.objects.filter(
                        county__state_id=state_id, 
                        poverty_id=poverty_id
                    ).aggregate(pov_sum=Sum('poverty_estimate_value'))

                    # print('poverty_total: ', poverty_total)

                    state_total = County.objects.filter(
                        state_id=state_id).aggregate(state_sum=Sum('poverty_total'))
                    # print('state_total: ', state_total)

                    count = count+1
                    print('count-----------------------', count)

                    if poverty_total['pov_sum'] and state_total['state_sum']:
                        print("In If ------>")
                        print('poverty_total: ',  poverty_total['pov_sum'])
                        print('state_total: ', state_total['state_sum'])

                        try:
                            poverty_state_db_data = PovertyStateTotal.objects.get(
                                poverty_id=poverty_id,
                                state_id=state_id
                            )
                            print('poverty_state_db_data: In TRY--->',
                                  poverty_state_db_data)
                        except:
                            poverty_state_db = PovertyStateTotal.objects.create(
                                state_total=state_total['state_sum'],
                                poverty_total=poverty_total['pov_sum'],
                                poverty_id=poverty_id,
                                state_id=state_id
                            )
                            print('poverty_state_db: EXCEPT===<',
                                  poverty_state_db)

                    else:
                        print("In ELSE::______")
                        print('poverty_total: ',  poverty_total['pov_sum'])
                        print('state_total: ', state_total['state_sum'])

            return Response({'msg': 'PovertyStateTotal DB Populated.'})

        except Exception as e:
            print("in except")
            return Response({'error in PSTD': f'{e}'})
