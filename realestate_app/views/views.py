import os
import json
import time
import ftplib
import requests

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import (County, Income, IncomeError, Race, State,
                                   RaceError, RaceEstimate,)

from realestate_app.paginations import CustomPagination

from realestate_app.serializers import (CountySerializer,  StateSerializer,
                                        RaceSerializer, RaceEstimateSerializer,
                                        IncomeSerializer, IncomeEstimate)

from realestate_app.utils import (convert_list_string, get_state_code,
                                  ftp_connect, get_file_ftp,  upload_file_ftp,
                                  json_file_read, json_file_write,)

from realestate_bot.settings import (FTP_HOST, FTP_PASS, FTP_USER,
                                     base_url, base_path)


def upload_file():
    """
        Function to Upload JSON file on the FTP Server
    """

    try:
        ftp = ftp_connect()
        filename = f"{base_path}/static/upload/racedata.json"
        ftp.set_pasv(False)

        with open(filename, "rb") as file:
            # data = file.read()
            # print('data: ', data)
            ftp.storbinary("STOR Housing_App_Unit/racestatedata01.json", file)
    except Exception as e:
        print("Error in UPF:", e)


def write_json_file(data):
    """
        Function to Write JSON File
    """

    try:
        file_path = f"{base_path}/static/upload/racedata.json"

        with open(file_path, "w") as f:
            f.write(data)
            f.close()
    except Exception as e:
        print("Error in WJF", e)


def read_json_file():

    try:
        file_path = f"{base_path}/static/download/racedata.json"

        with open(file_path, "r") as f:
            data = f.read()
            print('data in RJF:', type(data))
            f.close()

        data_dict = json.loads(data)
        print('data_dict in RJF:', type(data_dict))

        return data_dict

    except Exception as e:
        print("Error in RJF: ", e)

# DataBase APIs - To Populate Data in DB


class RaceStateData(APIView):

    def get_server_file(self):
        """
            Funtion to get JSON file from the FTP Server
        """

        try:
            ftp = ftp_connect()
            filename = f"{base_path}/static/download/racedata.json"
            ftp.set_pasv(False)

            with open(filename, 'wb') as file:
                ftp.retrbinary(
                    "RETR Housing_App_Unit/racestatedata01.json", file.write)

        except Exception as e:
            print("Error in GTF: ", e)

    def get(self, request):

        try:
            print("---before get a file")
            self.get_server_file()
            print("---after get a file")
            return Response({'msg': "File Downloded"})

        except Exception as e:
            print("Error in ftp_get inside::", e)
            return Response({'Error in RSD-G': f'{e}'})

    def post(self, request):

        try:
            print('request.data: ', request.data)

            symbol_list = request.data.get('Symbol')
            multi_symbol = convert_list_string(symbol_list)

            state_list = request.data.get('State')
            state_code_list = get_state_code(state_list)
            multi_state = convert_list_string(state_code_list)

            response = requests.get(
                f"{base_url}/1.0/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

            race_data = response.json()
            print('race_data============: \n', type(race_data))

            store_data = json.dumps(race_data)
            print('s===========: \n', type(store_data))

            write_json_file(store_data)

            print("Before Ts json file write.")
            time.sleep(2)
            print("After Ts json file write.")

            # sftpExamp()
            try:
                upload_file()

                ftp = ftp_connect()
                ftp.set_pasv(False)
                ftp.dir("Housing_App_Unit/")

            except Exception as e:
                print("Error in ftp_upload inside:::", e)

                ftp.quit()

            return Response(race_data)

        except Exception as e:
            return Response({"Error in RSD-P":  f"{e}"})


# class RaceCodeData(APIView):

#     def get_and_create_race_data(self, data_dict):
#         """
#             Function to get Race Code Data from dictionary
#             and populate Race Table
#         """

#         try:
#             print("try in GCRD: ", type(data_dict))
#             race_values = data_dict['tables'].get('B02001').get('columns')
#             print('values: ', race_values)

#             for data in race_values:
#                 race_id = data
#                 race_name = race_values.get(race_id).get("name")

#                 try:
#                     race_data = Race.objects.get(race_id=race_id)
#                     print('GCRD-race_data: try get: \n', race_data)
#                 except:
#                     racedb_data = Race.objects.create(
#                         race_id=race_id,
#                         race_name=race_name
#                     )
#                     print('GCRD-racedb_data: except create \n', racedb_data)

#         except Exception as e:
#             print("Error in GRD:", e)

#     def get(self, request):

#         try:
#             race_data = Race.objects.all()
#             if race_data.exists():
#                 print("Inside if --")
#                 race_serializer = RaceSerializer(race_data, many=True)
#                 return Response(race_serializer.data)
#             else:
#                 print("inside else --")
#                 return Response("No Data Available")

#         except Exception as e:
#             print("Error in RCD-GET: ", e)
#             return Response({'Error in RCD-G': e})

#     def post(self, request):

#         try:
#             data_dict = read_json_file()
#             # print('data_dict:======= ', data_dict)

#             self.get_and_create_race_data(data_dict)

#             return Response(data_dict)

#         except Exception as e:
#             print("Error in RCD-POST: ", e)
#             return Response({'Error in RCD-P': e})


class StateCountyDetailData(APIView):

    def get_and_create_state_county_data(self, data_dict):
        """
            Function to get State/County Data from dictionary 
            and populate State/County Table 
        """

        try:
            print("try in GCCD: ", type(data_dict))
            data_value = data_dict['geography']
            # print('data_value: ', data_value)

            for i in data_value:

                code_initial = i
                code_name = data_value.get(code_initial).get("name")

                # Checking and Insert State's Detail
                if code_initial[0:5] == '04000':
                    print("Getting State", code_initial[5:9])

                    state_id = code_initial[5:9]
                    state_name = code_name
                    state_ref_id = code_initial

                    try:
                        state_data = State.objects.get(state_id=state_id)
                        print('GCCD-state_data: try get \n', state_data)
                    except:
                        statedb_data = State.objects.create(
                            state_id=state_id,
                            state_name=state_name,
                            state_ref_id=state_ref_id
                        )
                        print('GCCD-statedb_data: except create', statedb_data)

                # Checking and Insert County's Detail
                elif code_initial[0:5] == '05000':

                    county_id = code_initial
                    county_name = code_name.split(',')[0]
                    state_id = code_initial[5:9]

                    state_data = State.objects.get(state_id=state_id)

                    try:

                        county_data = County.objects.get(county_id=county_id)
                        print('GCCD-county_data: try get \n', county_data)
                    except:
                        county_data = County.objects.create(
                            county_id=county_id,
                            county_name=county_name,
                            state=state_data
                        )
                        print('GCCD-county_data: except create \n', county_data)

                else:
                    print("NOT Relevent Data")

        except Exception as e:
            print("Error in GCCD: ", e)

    def get(self, request):

        try:
            state_data = State.objects.all()
            county_data = County.objects.all()

            new_dict = {}

            if state_data.exists() and county_data.exists():
                print("Inside If --")
                state_serializer = StateSerializer(state_data, many=True)
                print('state_serializer: ', type(state_serializer))
                county_serializer = CountySerializer(county_data, many=True)

                new_dict['State'] = list(state_serializer.data)
                new_dict['County'] = list(county_serializer.data)

                state_county_data = json.dumps(new_dict)
                print('state_county_data: ', type(state_county_data))

                return Response(state_county_data)

            else:
                print("Inside else--")
                return Response("No Data Available")

        except Exception as e:
            print("Error in CD-GET: ", e)

    def post(self, request):

        try:
            data_dict = read_json_file()
            print('data_dict in CD : ', type(data_dict))

            self.get_and_create_state_county_data(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in CD-POST: ", e)


class RaceErrorEstimateData(APIView):
    """
        To get Race Error/Estimate Data from dictionary 
        and populate Race_Error/Race_Estimate Table 
    """

    def get_and_create_race_error_estimate(self, data_dict):

        try:
            print("In GCREE: ", type(data_dict))
            data_value = data_dict['data']
            # print('data_value: ', data_value)

            county_data = County.objects.all()

            for county in county_data:

                if county.county_id in data_value:
                    print('county.county_id: ', county.county_id)

                    race_value = data_value.get(county.county_id).get("B02001")
                    print('race_value: ', race_value)

                    race_code = Race.objects.all()

                    race_total = race_value.get('estimate').get('B02001001')

                    county_obj = County.objects.get(county_id=county.county_id)
                    county_obj.race_total = race_total
                    county_obj.save()

                    for race in race_code:

                        # For Race_Estimate
                        race_estimate = race_value.get(
                            'estimate').get(race.race_id)
                        print('race_estimate: -->', race_estimate)

                        try:
                            race_estimate_detail = RaceEstimate.objects.get(
                                county_id=county.county_id, race_id=race.race_id)
                            print('race_estimate_detail: In TRY=== ',
                                  race_estimate_detail)
                        except:
                            race_estimate_detail = RaceEstimate.objects.create(
                                race_estimate_value=race_estimate,
                                county_id=county.county_id,
                                race_id=race.race_id
                            )
                            print('race_estimate_detail: In EXCEPT=== ',
                                  race_estimate_detail)

                        # For Race_Error
                        race_error = race_value.get('error').get(race.race_id)
                        print('race_error: ==<', race_error)

                        try:
                            race_error_detail = RaceError.objects.get(
                                county_id=county.county_id, race_id=race.race_id)
                            print('race_error_detail: In TRY---',
                                  race_error_detail)
                        except:
                            race_error_detail = RaceError.objects.create(
                                race_error_value=race_error,
                                county_id=county.county_id,
                                race_id=race.race_id
                            )
                            print('race_error_detail: In EXCEPT--',
                                  race_error_detail)

        except Exception as e:
            print('Error in GCREE: ', e)

    def get(self, request):

        try:
            return Response("IN REED")
        except Exception as e:
            print("Error in REED-GET:", e)
            return Response({'Error': f'{e}'})

    def post(self, request):

        try:
            data_dict = read_json_file()
            print('data_dict in REED: ', type(data_dict))

            self.get_and_create_race_error_estimate(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in REED-POST:", e)
            return Response({'Error': f'{e}'})

# ------------------------------------------------------------------
# ---------------------Topic Details---------------------------------------


class TopicDetails(APIView):
    """
        To get data about particular Topic from Census Reporter API
        and create JSON file of Topic_data
    """

    def post(self, request):

        try:
            if request.data:
                symbol_list = request.data.get('Symbol')
                multi_symbol = convert_list_string(symbol_list)

                state_list = request.data.get('State')
                state_code_list = get_state_code(state_list)
                multi_state = convert_list_string(state_code_list)

                response = requests.get(
                    f"{base_url}/1.0/data/show/latest?table_ids={multi_symbol}&geo_ids={multi_state}")

                data_values = response.json()
                print('data_values---------: \n', type(data_values))

                store_data = json.dumps(data_values)
                print('sd----: \n', type(store_data))

                file_name = request.data.get('File_Name')
                print('file_name: =----', file_name)

                json_file_write(store_data, file_name)

                return Response(data_values)
            else:
                print("In Else part:NO Request")

        except Exception as e:
            print("Error in ToS-POST", e)
            return Response({'msg': f'{e}'})


class UpdateFTPFile(APIView):

    def get(self, request):
        try:
            if request.data:
                file_name = request.data.get('File_Name')
                print('file_name: ', file_name)
                get_file_ftp(file_name)

                return Response({"Msg": f"{file_name} downloaded from server."})
            else:
                print("UFTPF In Else-GET")
        except Exception as e:
            print("Error in UFTPF-GET:", e)
            return Response({'msg': f'{e}'})

    def post(self, request):
        try:
            if request.data:
                file_name = request.data.get('File_Name')
                print('file_name: ', file_name)
                upload_file_ftp(file_name)
                ftp = ftp_connect()
                ftp.set_pasv(False)
                ftp.dir("Housing_App_Unit/")
                return Response({"Msg": f"{file_name} uploaded on server."})
            else:
                print("UFTPF In Else-POST")
        except Exception as e:
            print("Error in UFTPF-POST:", e)
            return Response({'msg': f'{e}'})

# ---------------------------------------------------------------------------
# --------------------------Topic Code Data----------------------------------


class TopicCodeData(APIView):

    def post(self, request):

        try:
            if request.data:

                file_name = request.data.get('File_Name')
                print('file_name: ', file_name)

                topic_id = request.data.get('Topic_ID')

                data_dict = json_file_read(file_name)
                print('data_dict:======= ', type(data_dict))

                # self.get_and_create_income_code(data_dict, topic_id)
                #  print("try in GCID: ", type(data_dict))

                topic_code = data_dict['tables'].get(topic_id).get('columns')
                print('topic_code: ', topic_code)

                for data in topic_code:
                    sub_topic_id = data
                    sub_topic_name = topic_code.get(sub_topic_id).get("name")

                    print("Sub_topic_id", sub_topic_id)
                    print("Sub_topic_name", sub_topic_name)

                    if topic_id == 'B19001':

                        print("Inside Income")

                        try:
                            income_data = Income.objects.get(
                                income_id=sub_topic_id)
                            print('GCID-income_data: try get: \n', income_data)
                        except:
                            incomedb_data = Income.objects.create(
                                income_id=sub_topic_id,
                                income_name=sub_topic_name
                            )
                            print('GCID-incomedb_data: except create \n',
                                  incomedb_data)

                    elif topic_id == 'B02001':

                        print('Inside Race')

                        try:
                            race_data = Race.objects.get(race_id=sub_topic_id)
                            print('GCRD-race_data: try get: \n', race_data)
                        except:
                            racedb_data = Race.objects.create(
                                race_id=sub_topic_id,
                                race_name=sub_topic_name
                            )
                            print('GCRD-racedb_data: except create \n', racedb_data)

                    else:
                        return Response({'msg': 'NOT Valid Inputs'})

                return Response(data_dict)

        except Exception as e:
            print("Error in ICD-POST: ", e)
            return Response({'Error in ICD-P': f'{e}'})

#   ------------------------------------------------------------------------------------
#   ------------------------------Income-----------------------------------------------


class IncomeErrorEstimateData(APIView):

    def post(self, request):

        try:
            file_name = request.data.get('File_Name')
            print('file_name: ', file_name)
            # topic_id = request.data.get('Topic_ID')
            # print('topic_id: ', topic_id)

            data_dict = json_file_read(file_name)
            print('data_dict in TEED: ', type(data_dict))

            # self.get_and_create_income_error_estimate(data_dict)

            data_value = data_dict['data']
            print('data_value: ', data_value)

            county_data = County.objects.all()

            for county in county_data:

                if county.county_id in data_value:
                    print('county.county_id: ', county.county_id)

                    income_value = data_value.get(
                        county.county_id).get("B19001")
                    print('income_value: ', income_value)

                    income_code = Income.objects.all()

                    income_total = income_value.get(
                        'estimate').get('B19001001')

                    county_obj = County.objects.get(county_id=county.county_id)
                    county_obj.income_total = income_total
                    county_obj.save()

                    for income in income_code:

                        # For Income_Estimate
                        income_estimate = income_value.get(
                            'estimate').get(income.income_id)
                        print('income_estimate: -->', income_estimate)

                        try:
                            income_estimate_detail = IncomeEstimate.objects.get(
                                county_id=county.county_id, income_id=income.income_id)
                            print('income_estimate_detail: In TRY=== ',
                                  income_estimate_detail)
                        except:
                            income_estimate_detail = IncomeEstimate.objects.create(
                                income_estimate_value=income_estimate,
                                county_id=county.county_id,
                                income_id=income.income_id
                            )
                            print('income_estimate_detail: In EXCEPT=== ',
                                  income_estimate_detail)

                        # For Income_Error
                        income_error = income_value.get(
                            'error').get(income.income_id)
                        print('income_error: ==<', income_error)

                        try:
                            income_error_detail = IncomeError.objects.get(
                                county_id=county.county_id, income_id=income.income_id)
                            print('income_error_detail: In TRY---',
                                  income_error_detail)
                        except:
                            income_error_detail = IncomeError.objects.create(
                                income_error_value=income_error,
                                county_id=county.county_id,
                                income_id=income.income_id
                            )
                            print('income_error_detail: In EXCEPT--',
                                  income_error_detail)

            return Response(data_dict)

        except Exception as e:
            print("Error in REED-POST:", e)
            return Response({'Error': f'{e}'})
