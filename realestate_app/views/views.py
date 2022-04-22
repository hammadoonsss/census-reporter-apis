import os
import json
import time
import ftplib
import requests

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from realestate_app.models import County, Race, RaceError, RaceEstimate, State

from realestate_app.paginations import CustomPagination

from realestate_app.serializers import (
    CountySerializer, RaceEstimateSerializer, RaceSerializer, StateSerializer)

from realestate_app.utils import convert_list_string,get_state_code

from realestate_bot.settings import (FTP_HOST, FTP_PASS, FTP_USER,
                                    base_url,base_path)


def ftp_connect():
    """
        Function for making Connection to FTP Server
    """
    try:
        # print("___--___", FTP_HOST, FTP_USER, FTP_PASS)

        # Connect to FTP Server
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        print('ftp:--- ', ftp)

        # force utf-8 encoding
        ftp.encoding = "utf-8"
        return ftp

    except Exception as e:
        print("Error in ftp: \n", e)


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


class RaceCodeData(APIView):

    def get_and_create_race_data(self, data_dict):
        """
            Function to get Race Code Data from dictionary
            and populate Race Table 
        """

        try:
            print("try in GCRD: ", type(data_dict))
            data_value = data_dict['tables'].get('B02001').get('columns')
            print('values: ', data_value)

            for i in data_value:
                race_id = i
                race_name = data_value.get(i).get("name")

                try:
                    race_data = Race.objects.get(race_id=race_id)
                    print('GCRD-race_data: try get: \n', race_data)
                except:
                    racedb_data = Race.objects.create(
                        race_id=race_id,
                        race_name=race_name
                    )
                    print('GCRD-racedb_data: except create \n', racedb_data)

        except Exception as e:
            print("Error in GRD:", e)

    def get(self, request):

        try:
            race_data = Race.objects.all()
            if race_data.exists():
                print("Inside if --")
                race_serializer = RaceSerializer(race_data, many=True)
                return Response(race_serializer.data)
            else:
                print("inside else --")
                return Response("No Data Available")

        except Exception as e:
            print("Error in RCD-GET: ", e)
            return Response({'Error in RCD-G': e})

    def post(self, request):

        try:
            data_dict = read_json_file()
            # print('data_dict:======= ', data_dict)

            self.get_and_create_race_data(data_dict)

            return Response(data_dict)

        except Exception as e:
            print("Error in RCD-POST: ", e)
            return Response({'Error in RCD-P': e})


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

    def get_and_create_race_error_estimate(self, data_dict):

        try:
            print("In GCREE: ", type(data_dict))
            data_value = data_dict['data']
            print('data_value: ', data_value)

            county_data = County.objects.all()

            for county in county_data:

                if county.county_id in data_value:
                    print('county.county_id: ', county.county_id)

                    race_value = data_value.get(county.county_id).get("B02001")
                    print('race_value: ', race_value)

                    race_code = Race.objects.all()

                    for race in race_code:

                        # Race_Estimate
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

                        # Race_Error
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


# Main APIs - To Fetch Data.


class StateRaceEstimateData(APIView, CustomPagination):

    def get(self, request):
        try:
            if request.data:  

                symbol = request.data.get("Symbol")
                print('symbol: ', symbol)
                state = request.data.get("State")
                print('state: ', state)

                state_data = State.objects.get(state_name=state)
                print('state_data:--- ', state_data)

                state_county = County.objects.filter(
                    state_id=state_data).values_list('county_id', flat=True)
                print('state_county:--- ', state_county)

                race_estimate = RaceEstimate.objects.filter(
                    county_id__in=state_county)
                print('race_estimate: ----', race_estimate)

                county_race_list = []

                for data in race_estimate:

                    race_dict = {}

                    race_dict['State_id'] = data.county.state.state_id
                    # race_dict['State_name'] = data.county.state.state_name

                    race_dict['County_id'] = data.county_id
                    # race_dict['County_name'] = data.county.county_name

                    race_dict['Race_id'] = data.race_id
                    race_dict['Race_name'] = data.race.race_name
                    race_dict['Race_Estimate_value'] = data.race_estimate_value

                    county_race_list.append(race_dict)

                # # Pagination -1
                # result = self.paginate_queryset(race_estimate, request)
                # race_serializer = RaceEstimateSerializer(result, many=True)
                # print('result: ', result)
                # return self.get_paginated_response(race_serializer.data)

                # Serializer-DB_data
                # race_serializer = RaceEstimateSerializer(race_estimate, many=True)
                # return Response(race_serializer.data)

                # Dictionary-county_race_list
                # return Response({'data': county_race_list})

                # Pagination -2
                result = self.paginate_queryset(county_race_list, request)
                # race_serializer = RaceEstimateSerializer(result, many=True)
                print('result: ', result)
                return self.get_paginated_response(result)

            else:
                return Response({'Error': "In valid request!!"})
        except Exception as e:
            print("Error in RSD-GET:", e)
            return Response({"In Exception": e})
