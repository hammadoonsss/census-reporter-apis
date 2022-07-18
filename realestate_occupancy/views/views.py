from django.shortcuts import render
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State,)

from realestate_occupancy.models import (
    Occupancy,
    OccupancyEstimate,
    OccupancyError,
    OccupancyStateTotal
)


# ---------------------------------------------------------------------------------------------------
# --------------------- Populate Occupancy Code Data in the Occupancy Table -------------------------


class OccupancyCodeData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('tables').get(
                    'B25002').get('columns')
                # print('data_value: ', data_value)

                for code in data_value:
                    sub_occ_id = code
                    sub_occ_name = data_value.get(sub_occ_id).get('name')
                    # print('sub_occ_id: ', sub_occ_id)
                    # print('sub_occ_name: ', sub_occ_name)

                    try:
                        occ_db = Occupancy.objects.get(
                            occupancy_id=sub_occ_id)
                        print('occ_db in TRY--->: ', occ_db)

                    except:
                        occdb_data = Occupancy.objects.create(
                            occupancy_id=sub_occ_id,
                            occupancy_name=sub_occ_name
                        )
                        print('occdb_data in EXCEPT===<: ', occdb_data)

                return Response({'msg': 'Occupancy DB Populated.'})

            else:
                return Response({'error': "Invalid request"})

        except Exception as e:
            return Response({'error in OCD': f'{e}'})


#   -----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Occupancy Error/Estimate Data in their Respective Tables ---------------------


class OccupancyEstimateErrorData(APIView):

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

                        occupancy_value = data_value.get(
                            county.county_id).get("B25002")
                        # print('occupancy_value: --->', occupancy_value)

                        occupancy_code = Occupancy.objects.all()
                        # print('occupancy_code: ', occupancy_code)

                        # For occupancy_total in County Table
                        occupancy_total = occupancy_value.get(
                            'estimate').get("B25002001")

                        if occupancy_total:
                            print("In occ_Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.occupancy_total = occupancy_total
                            county_obj.save()

                        else:
                            print("___NO occ_total___")

                        for occupancy in occupancy_code:
                            print('occupancy: ', occupancy)

                            # For Occupancy_Estimate
                            occupancy_estimate = occupancy_value.get(
                                'estimate').get(occupancy.occupancy_id)
                            # print('occupancy_estimate:---> ',
                            #       occupancy_estimate)

                            if occupancy_estimate:
                                print('In IF :: occupancy_estimate: ',
                                      occupancy_estimate)
                                try:
                                    occest_db = OccupancyEstimate.objects.get(
                                        county_id=county.county_id,
                                        occupancy_id=occupancy.occupancy_id
                                    )
                                    print('occest_db In TRY --->: ', occest_db)

                                except:
                                    occestdb_data = OccupancyEstimate.objects.create(
                                        occupancy_estimate_value=occupancy_estimate,
                                        county_id=county.county_id,
                                        occupancy_id=occupancy.occupancy_id
                                    )
                                    print('occestdb_data In EXCEPT ====<: ',
                                          occestdb_data)

                            else:
                                print('In else_occest :: No Value: ',
                                      occupancy_estimate)
                                pass

                            # For Occupancy_Error
                            occupancy_error = occupancy_value.get(
                                'error').get(occupancy.occupancy_id)
                            # print('occupancy_error:===< ', occupancy_error)

                            if occupancy_error:
                                print('In IF :: occupancy_error: ',
                                      occupancy_error)

                                try:
                                    occerr_db = OccupancyError.objects.get(
                                        county_id=county.county_id,
                                        occupancy_id=occupancy.occupancy_id
                                    )
                                    print('occerr_db In TRY -->: ', occerr_db)
                                except:
                                    occerrdb_data = OccupancyError.objects.create(
                                        occupancy_error_value=occupancy_error,
                                        county_id=county.county_id,
                                        occupancy_id=occupancy.occupancy_id
                                    )
                                    print('occerrdb_data In EXCEPT ==<": ',
                                          occerrdb_data)

                            else:
                                print('In else-occerr :: No Value: ',
                                      occupancy_error)
                                pass

                    else:
                        print("In Else OEED.")
                        pass

                return Response({'msg': 'OccupancyEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in OEED': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Occupancy_State_Total Data in the Respective Table --------------------------


class OccupancyStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                occ_data = Occupancy.objects.all()

                for occ_id in occ_data:
                    # print('s_id: ', s_id)
                    # print('occ_id: ', occ_id)

                    occ_total = OccupancyEstimate.objects.filter(
                        county__state_id=s_id, occupancy_id=occ_id
                    ).aggregate(sum_occ=Sum('occupancy_estimate_value'))

                    # print('occ_total:=== ', occ_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('occupancy_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if occ_total['sum_occ'] and state_total['sum_state']:
                        print("In If --------->")
                        print('occ_total: ', occ_total['sum_occ'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            occ_state_db = OccupancyStateTotal.objects.get(
                                state_id=s_id, occupancy_id=occ_id
                            )
                            print('occ_state_db: In TRY---> ', occ_state_db)

                        except:
                            occ_state_totaldb = OccupancyStateTotal.objects.create(
                                state_id=s_id,
                                occupancy_id=occ_id,
                                state_total=state_total['sum_state'],
                                occupancy_total=occ_total['sum_occ']
                            )
                            print('occ_state_totaldb: EXCEPT ===< ',
                                  occ_state_totaldb)
                    else:
                        print("In Else::______")
                        print('occ_total: ', occ_total['sum_occ'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'Occupancy_State_Total DB Populated.'})

        except Exception as e:
            return Response({'error in OSTD': f'{e}'})
