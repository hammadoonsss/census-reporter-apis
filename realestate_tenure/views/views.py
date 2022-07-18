from django.shortcuts import render
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State)

from realestate_tenure.models import (
    Tenure,
    TenureEstimate, TenureError,
    TenureStateTotal
)


#   -------------------------------------------------------------------------------------------------------
#   ------------------------- Populate Tenure Code Data in the Respective Table ---------------------------


class TenureCodeData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get("File_Name")
                # print('file_name: ', file_name)

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('tables').get(
                    'B25003').get('columns')

                # print('data_value: ', data_value)

                for code in data_value:
                    sub_te_id = code
                    sub_te_name = data_value.get(sub_te_id).get('name')

                    # print('sub_te_id: ', sub_te_id)
                    # print('sub_te_name: ', sub_te_name)

                    try:
                        te_db = Tenure.objects.get(tenure_id=sub_te_id)
                        print('te_db in TRY--->: ', te_db)

                    except:
                        tedb_data = Tenure.objects.create(
                            tenure_id=sub_te_id,
                            tenure_name=sub_te_name
                        )
                        print('tedb_data in EXCEPT===<:: ', tedb_data)

                return Response({'msg': 'Tenure DB Polpulated.'})

            else:
                return Response({'error': "Invalid request"})

        except Exception as e:
            return Response({'error in TCD': f'{e}'})


#   ---------------------------------------------------------------------------------------------------------
#   --------------------- Populate Tenure Error/Estimate Data in their Respective Tables --------------------


class TenureEstimateErrorData(APIView):

    def post(self, request):

        try:
            if request.data:

                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                print('data_dict: ', type(data_dict))

                data_value = data_dict.get('data')

                county_data = County.objects.all()

                for county in county_data:

                    if county.county_id in data_value:
                        print('county.county_id: ', county.county_id)

                        tenure_value = data_value.get(
                            county.county_id).get("B25003")
                        # print('tenure_value: --->', tenure_value)

                        tenure_code = Tenure.objects.all()
                        # print('tenure_code: ', tenure_code)

                        # For tenure_total in County Table
                        tenure_total = tenure_value.get(
                            'estimate').get("B25003001")

                        if tenure_total:
                            print("In te Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.tenure_total = tenure_total
                            county_obj.save()

                        else:
                            print("___NO te_total___")

                        for tenure in tenure_code:
                            print('tenure: ', tenure)

                            # For Tenure Estimate
                            tenure_estimate = tenure_value.get(
                                'estimate').get(tenure.tenure_id)
                            # print('tenure_estimate: ', tenure_estimate)

                            if tenure_estimate:
                                print('In IF :: tenure_estimate: ',
                                      tenure_estimate)
                                try:
                                    teest_db = TenureEstimate.objects.get(
                                        county_id=county.county_id,
                                        tenure_id=tenure.tenure_id
                                    )
                                    print('teest_db In TRY --->: ', teest_db)

                                except:
                                    teestdb_data = TenureEstimate.objects.create(
                                        tenure_estimate_value=tenure_estimate,
                                        county_id=county.county_id,
                                        tenure_id=tenure.tenure_id
                                    )
                                    print('teestdb_data In EXCEPT ====<: ',
                                          teestdb_data)

                            else:
                                print('In Else_teest :: No Value: ',
                                      tenure_estimate)
                                pass

                            # For Tenure Error
                            tenure_error = tenure_value.get(
                                'error').get(tenure.tenure_id)
                            # print('tenure_error: ', tenure_error)

                            if tenure_error:
                                print('In IF :: tenure_error: ', tenure_error)

                                try:
                                    teerr_db = TenureError.objects.get(
                                        county_id=county.county_id,
                                        tenure_id=tenure.tenure_id
                                    )
                                    print('teerr_db In TRY -->: ', teerr_db)

                                except:
                                    teerrdb_data = TenureError.objects.create(
                                        tenure_error_value=tenure_error,
                                        county_id=county.county_id,
                                        tenure_id=tenure.tenure_id
                                    )
                                    print('teerrdb_data In EXCEPT ==<": ',
                                          teerrdb_data)

                            else:
                                print('In Else-teerr :: No Value: ',
                                      tenure_error)

                    else:
                        print("In Else TEED.")
                        pass

                return Response({'msg': 'TenureEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in TEED': f'{e}'})


#   ------------------------------------------------------------------------------------------------------
#   ------------------- Populate Tenure_State_Total Data in the Respective Table -------------------------


class TenureStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                te_data = Tenure.objects.all()

                for te_id in te_data:
                    # print('s_id: ', s_id)
                    # print('te_id: ', te_id)

                    te_total = TenureEstimate.objects.filter(
                        county__state_id=s_id, tenure_id=te_id
                    ).aggregate(sum_te=Sum('tenure_estimate_value'))

                    # print('te_total:=== ', te_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('tenure_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if te_total['sum_te'] and state_total['sum_state']:
                        print("In IF -------->")
                        print('te_total: ', te_total['sum_te'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            te_state_db = TenureStateTotal.objects.get(
                                state_id=s_id, tenure_id=te_id
                            )
                            print('te_state_db: In TRY---> ', te_state_db)

                        except:
                            te_state_totaldb = TenureStateTotal.objects.create(
                                state_id=s_id,
                                tenure_id=te_id,
                                state_total=state_total['sum_state'],
                                tenure_total=te_total['sum_te']
                            )
                            print('te_state_totaldb: EXCEPT===< ',
                                  te_state_totaldb)

                    else:
                        print("In ELSE::_________")
                        print('te_total: ', te_total['sum_te'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'TenureStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in TSTD': f'{e}'})
