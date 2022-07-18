from django.shortcuts import render
from django.db.models import Count, Min, Max, F, Q, Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State)

from realestate_sex_age.models import (
    SexAge,
    SexAgeEstimate, SexAgeError,
    SexAgeStateTotal,
)


#   --------------------------------------------------------------------------------------------------------
#   ------------------------- Populate Sex_Age Code Data in the Respective Table ---------------------------


class SexAgeCodeData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get("File_Name")
                # print('file_name: ', file_name)

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('tables').get(
                    'B01001').get('columns')

                # print('data_value: ', data_value)

                for code in data_value:
                    sub_sa_id = code
                    sub_sa_name = data_value.get(sub_sa_id).get('name')

                    # print('sub_sa_id: ', sub_sa_id)
                    # print('sub_sa_name: ', sub_sa_name)

                    try:
                        sa_db = SexAge.objects.get(sex_age_id=sub_sa_id)
                        print('sa_db in TRY--->: ', sa_db)

                    except:
                        sadb_data = SexAge.objects.create(
                            sex_age_id=sub_sa_id,
                            sex_age_name=sub_sa_name
                        )
                        print('sadb_data in EXCEPT===<:: ', sadb_data)

                return Response({'msg': 'Sex_Age DB Polpulated.'})

            else:
                return Response({'error': "Invalid request"})

        except Exception as e:
            return Response({'error in SACD': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   --------------------- Populate Sex_Age Error/Estimate Data in their Respective Tables --------------------


class SexAgeEstimateErrorData(APIView):

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

                        sex_age_value = data_value.get(
                            county.county_id).get("B01001")
                        # print('sex_age_value: --->', sex_age_value)

                        sex_age_code = SexAge.objects.all()
                        # print('sex_age_code: ', sex_age_code)

                        # For sex_age_total in County Table
                        sex_age_total = sex_age_value.get(
                            'estimate').get("B01001001")

                        if sex_age_total:
                            print("In sa Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.sex_age_total = sex_age_total
                            county_obj.save()

                        else:
                            print("___NO sa_total___")

                        for sex_age in sex_age_code:
                            print('sex_age: ', sex_age)

                            # For Sex_Age Estimate
                            sex_age_estimate = sex_age_value.get(
                                'estimate').get(sex_age.sex_age_id)
                            # print('sex_age_estimate: ', sex_age_estimate)

                            if sex_age_estimate:
                                print('In IF :: sex_age_estimate: ',
                                      sex_age_estimate)
                                try:
                                    saest_db = SexAgeEstimate.objects.get(
                                        county_id=county.county_id,
                                        sex_age_id=sex_age.sex_age_id
                                    )
                                    print('saest_db In TRY --->: ', saest_db)

                                except:
                                    saestdb_data = SexAgeEstimate.objects.create(
                                        sex_age_estimate_value=sex_age_estimate,
                                        county_id=county.county_id,
                                        sex_age_id=sex_age.sex_age_id
                                    )
                                    print('saestdb_data In EXCEPT ====<: ',
                                          saestdb_data)

                            else:
                                print('In Else_saest :: No Value: ',
                                      sex_age_estimate)
                                pass

                            # For Sex_age Error
                            sex_age_error = sex_age_value.get(
                                'error').get(sex_age.sex_age_id)
                            # print('sex_age_error: ', sex_age_error)

                            if sex_age_error:
                                print('In IF :: sex_age_error: ', sex_age_error)

                                try:
                                    saerr_db = SexAgeError.objects.get(
                                        county_id=county.county_id,
                                        sex_age_id=sex_age.sex_age_id
                                    )
                                    print('saerr_db In TRY -->: ', saerr_db)

                                except:
                                    saerrdb_data = SexAgeError.objects.create(
                                        sex_age_error_value=sex_age_error,
                                        county_id=county.county_id,
                                        sex_age_id=sex_age.sex_age_id
                                    )
                                    print('saerrdb_data In EXCEPT ==<": ',
                                          saerrdb_data)

                            else:
                                print('In Else-saerr :: No Value: ',
                                      sex_age_error)

                    else:
                        print("In Else SAEED.")
                        pass

                return Response({'msg': 'SexAgeEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in SAEED': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Sex_Age_State_Total Data in the Respective Tables--------------------------


class SexAgeStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                sa_data = SexAge.objects.all()

                for sa_id in sa_data:
                    # print('s_id: ', s_id)
                    # print('sa_id: ', sa_id)

                    sa_total = SexAgeEstimate.objects.filter(
                        county__state_id=s_id, sex_age_id=sa_id
                    ).aggregate(sum_sa=Sum('sex_age_estimate_value'))

                    # print('sa_total:=== ', sa_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('sex_age_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if sa_total['sum_sa'] and state_total['sum_state']:
                        print("In IF -------->")
                        print('sa_total: ', sa_total['sum_sa'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            sa_state_db = SexAgeStateTotal.objects.get(
                                state_id=s_id, sex_age_id=sa_id
                            )
                            print('sa_state_db: In TRY---> ', sa_state_db)

                        except:
                            sa_state_totaldb = SexAgeStateTotal.objects.create(
                                state_id=s_id,
                                sex_age_id=sa_id,
                                state_total=state_total['sum_state'],
                                sex_age_total=sa_total['sum_sa']
                            )
                            print('sa_state_totaldb: EXCEPT===< ',
                                  sa_state_totaldb)

                    else:
                        print("In ELSE::_________")
                        print('sa_total: ', sa_total['sum_sa'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'SexAgeStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in SASTD': f'{e}'})
