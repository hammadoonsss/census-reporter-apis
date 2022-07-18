from django.shortcuts import render
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.utils import json_file_read

from realestate_app.models import (County, State,)

from realestate_education.models import (
    Education,
    EducationEstimate,
    EducationError,
    EducationStateTotal
)


# ---------------------------------------------------------------------------------------------------
# --------------------- Populate Education Code Data in the Education Table -------------------------


class EductionCodeData(APIView):

    def post(self, request):

        try:
            if request.data:
                file_name = request.data.get('File_Name')

                data_dict = json_file_read(file_name)
                # print('data_dict: ', type(data_dict))

                data_value = data_dict.get('tables').get(
                    'B15003').get('columns')
                # print('data_value: ', data_value)

                for code in data_value:
                    sub_edu_id = code
                    sub_edu_name = data_value.get(sub_edu_id).get('name')
                    # print('sub_edu_id: ', sub_edu_id)
                    # print('sub_edu_name: ', sub_edu_name)

                    try:
                        edu_db = Education.objects.get(education_id=sub_edu_id)
                        print('edu_db in TRY--->: ', edu_db)

                    except:
                        edudb_data = Education.objects.create(
                            education_id=sub_edu_id,
                            education_name=sub_edu_name
                        )
                        print('edudb_data in EXCEPT===<: ', edudb_data)

                return Response({'msg': 'Education DB Populated.'})

            else:
                return Response({'error': "Invalid request"})

        except Exception as e:
            return Response({'error in ECD': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Education Error/Estimate Data in their Respective Tables---------------------


class EducationEstimateErrorData(APIView):

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

                        education_value = data_value.get(
                            county.county_id).get("B15003")
                        # print('education_value: --->', education_value)

                        education_code = Education.objects.all()
                        # print('education_code: ', education_code)

                        # For education_total in County Table
                        education_total = education_value.get(
                            'estimate').get("B15003001")

                        if education_total:
                            print("In edu_Total=====")

                            county_obj = County.objects.get(
                                county_id=county.county_id)
                            county_obj.education_total = education_total
                            county_obj.save()

                        else:
                            print("___NO edu_total___")

                        for education in education_code:
                            print('education: ', education)

                            # For Education Estimate
                            education_estimate = education_value.get(
                                'estimate').get(education.education_id)
                            # print('education_estimate:---> ',
                            #       education_estimate)

                            if education_estimate:
                                print('In IF :: education_estimate: ',
                                      education_estimate)

                                try:
                                    eduest_db = EducationEstimate.objects.get(
                                        county_id=county.county_id,
                                        education_id=education.education_id
                                    )
                                    print('eduest_db In TRY --->: ', eduest_db)

                                except:
                                    eduestdb_data = EducationEstimate.objects.create(
                                        education_estimate_value=education_estimate,
                                        county_id=county.county_id,
                                        education_id=education.education_id
                                    )
                                    print('eduestdb_data In EXCEPT ====<: ',
                                          eduestdb_data)

                            else:
                                print('In else_eduest :: No Value',
                                      education_estimate)
                                pass

                            # For Education Error
                            education_error = education_value.get(
                                'error').get(education.education_id)
                            # print('education_error:===< ', education_error)

                            if education_error:
                                print('In IF :: education_error: ',
                                      education_error)
                                try:
                                    eduerr_db = EducationError.objects.get(
                                        county_id=county.county_id,
                                        education_id=education.education_id
                                    )
                                    print('eduerr_db In TRY -->: ', eduerr_db)
                                except:
                                    eduerrdb_data = EducationError.objects.create(
                                        education_error_value=education_error,
                                        county_id=county.county_id,
                                        education_id=education.education_id
                                    )
                                    print('eduerrdb_data In EXCEPT ==<": ',
                                          eduerrdb_data)

                            else:
                                print('In else-eduerr:: No Value',
                                      education_error)
                                pass

                    else:
                        print("In Else EEED.")
                        pass

                return Response({'msg': 'EducationEstimateError DB Populated.'})

            else:
                return Response({'error': 'Invalid request'})

        except Exception as e:
            return Response({'error in EEED': f'{e}'})


#   ----------------------------------------------------------------------------------------------------------
#   ------------------- Populate Education_State_Total Data in the Respective Tables--------------------------

class EducationStateTotalData(APIView):

    def post(self, request):

        try:
            count = 0
            state_data = State.objects.all()

            for s_id in state_data:
                edu_data = Education.objects.all()

                for edu_id in edu_data:
                    # print('s_id: ', s_id)
                    # print('edu_id: ', edu_id)

                    edu_total = EducationEstimate.objects.filter(
                        county__state_id=s_id, education_id=edu_id
                    ).aggregate(sum_edu=Sum('education_estimate_value'))

                    # print('edu_total:=== ', edu_total)

                    state_total = County.objects.filter(state_id=s_id).aggregate(
                        sum_state=Sum('education_total'))

                    # print('state_total: ===', state_total)

                    count += 1
                    print('count:------------------- ', count)

                    if edu_total['sum_edu'] and state_total['sum_state']:
                        print("In If---------->")
                        print('edu_total: ', edu_total['sum_edu'])
                        print('state_total: ', state_total['sum_state'])

                        try:
                            edu_state_db = EducationStateTotal.objects.get(
                                state_id=s_id, education_id=edu_id
                            )
                            print('edu_state_db: In TRY---> ', edu_state_db)

                        except:
                            edu_state_totaldb = EducationStateTotal.objects.create(
                                state_id=s_id,
                                education_id=edu_id,
                                state_total=state_total['sum_state'],
                                education_total=edu_total['sum_edu']
                            )
                            print('edu_state_totaldb: ===< ', edu_state_totaldb)
                    else:
                        print("In ELSE::______")
                        print('edu_total: ', edu_total['sum_edu'])
                        print('state_total: ', state_total['sum_state'])

            return Response({'msg': 'EducationStateTotal DB Populated.'})

        except Exception as e:
            return Response({'error in ESTD': f'{e}'})
