from django.shortcuts import render
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State,)

from realestate_mobility.models import (
    Mobility,
    MobilityEstimate, MobilityError,
    MobilityStateTotal,
)


# -------------------------------------------------------------------------------------------------
# --------------------- Populate Mobility Code Data in the Mobility Table -------------------------


class MobilityCodeData(APIView):

    def post(self, request):
        try:
            if request.data:

                file_name = request.data.get('File_Name')
                # print('file name ------>>>>', file_name)
                data_dict = json_file_read(file_name)

                mobility_code = data_dict['tables'].get(
                    'B07003').get('columns')

                for data in mobility_code:

                    sub_mobility_id = data
                    sub_mobility_name = mobility_code.get(
                        sub_mobility_id).get("name")

                    # print('sub_mobility_id: ', sub_mobility_id)
                    # print('sub_mobility_name: ', sub_mobility_name)

                    if (
                        sub_mobility_id == 'B07003001'
                        or sub_mobility_id == 'B07003004'
                        or sub_mobility_id == 'B07003007'
                        or sub_mobility_id == 'B07003010'
                        or sub_mobility_id == 'B07003013'
                        or sub_mobility_id == 'B07003016'
                    ):

                        print("Inside mobility------------/>", sub_mobility_id)

                        try:
                            mobility_db = Mobility.objects.get(
                                mobility_id=sub_mobility_id)
                            print('mobility_db in TRY---->: ', mobility_db)

                        except:
                            mobilitydb_data = Mobility.objects.create(
                                mobility_id=sub_mobility_id,
                                mobility_name=sub_mobility_name)

                            print('mobilitydb_data in EXCEPT===<: ',
                                  mobilitydb_data)

                    else:
                        print("In else")
                        pass

                return Response({'msg': 'Mobility DB Populated.'})

            else:
                return Response({'error': "Invalid Request."})

        except Exception as e:
            return Response({'error in MCD': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Mobility Error/Estimate Data in their Respective Tables ---------------------


class MobilityEstimateErrorData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('data')

                county_data = County.objects.all()

                for county in county_data:

                    if county.county_id in data_value:
                        print('county.county_id: ', county.county_id)

                        mobility_value = data_value.get(
                            county.county_id).get("B07003")
                        # print('mobility_value: --->', mobility_value)

                        mobility_code = Mobility.objects.all()
                        # print('mobility_code: ', mobility_code)

                        # For mobility_total in County Table
                        mobility_total = mobility_value.get(
                            'estimate').get("B07003001")

                        if mobility_total:
                            print("In mob_Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.mobility_total = mobility_total
                            county_obj.save()

                        else:
                            print("___NO mob_total___")

                        for mobility in mobility_code:
                            print('mobility: ', mobility)

                            # For Mobility Estimate
                            mobility_estimate = mobility_value.get(
                                'estimate').get(mobility.mobility_id)
                            print('mobility_estimate:---> ',
                                  mobility_estimate)

                            if mobility_estimate:
                                print('In IF :: mobility_estimate: ',
                                      mobility_estimate)

                                try:
                                    movest_db = MobilityEstimate.objects.get(
                                        county_id=county.county_id,
                                        mobility_id=mobility.mobility_id
                                    )
                                    print('movest_db In TRY --->: ', movest_db)

                                except:
                                    movestdb_data = MobilityEstimate.objects.create(
                                        mobility_estimate_value=mobility_estimate,
                                        county_id=county.county_id,
                                        mobility_id=mobility.mobility_id
                                    )
                                    print('movestdb_data In EXCEPT ====<: ',
                                          movestdb_data)
                            else:
                                print("In else_mobest :: No Value",
                                      mobility_estimate)
                                pass

                            # For Mobility Error
                            mobility_error = mobility_value.get(
                                'error').get(mobility.mobility_id)
                            print('mobility_error:===< ', mobility_error)

                            if mobility_error:
                                print('In IF :: mobility_error: ',
                                      mobility_error)

                                try:
                                    moverr_db = MobilityError.objects.get(
                                        county_id=county.county_id,
                                        mobility_id=mobility.mobility_id
                                    )
                                    print('moverr_db In TRY -->: ', moverr_db)

                                except:
                                    moverrdb_data = MobilityError.objects.create(
                                        mobility_error_value=mobility_error,
                                        county_id=county.county_id,
                                        mobility_id=mobility.mobility_id
                                    )
                                    print('moverrdb_data In EXCEPT ==<": ',
                                          moverrdb_data)

                            else:
                                print("In else-moberr :: No Value",
                                      mobility_estimate)
                                pass

                    else:
                        print("In Else MEED.")
                        pass

                return Response({'msg': 'MobilityEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in MEED': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Mobility_State_Total Data in the Respective Tables--------------------------


class MobilityStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                mob_data = Mobility.objects.all()

                for mob_id in mob_data:
                    # print('s_id: ', s_id)
                    # print('mob_id: ', mob_id)

                    mob_total = MobilityEstimate.objects.filter(
                        county__state_id=s_id, mobility_id=mob_id
                    ).aggregate(sum_mob=Sum('mobility_estimate_value'))

                    # print('mob_total:=== ', mob_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('mobility_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if mob_total['sum_mob'] and state_total['sum_state']:
                        print("In If --------->")
                        print('mob_total: ', mob_total['sum_mob'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            mob_state_db = MobilityStateTotal.objects.get(
                                state_id=s_id, mobility_id=mob_id
                            )
                            print('mob_state_db: In TRY---> ', mob_state_db)

                        except:
                            mob_state_totaldb = MobilityStateTotal.objects.create(
                                state_id=s_id,
                                mobility_id=mob_id,
                                state_total=state_total['sum_state'],
                                mobility_total=mob_total['sum_mob']
                            )
                            print('mob_state_totaldb: EXCEPT===< ',
                                  mob_state_totaldb)

                    else:
                        print("In ELSE::______")
                        print('mob_total:: ', mob_total['sum_mob'])
                        print('state_total:: ', state_total['sum_state'])

            return Response({'msg': 'MobilityStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in MSTD': f'{e}'})
